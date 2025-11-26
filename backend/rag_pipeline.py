import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama

# Cargar variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), "env"))


class SimpleRAG:
    """Pequeña implementación RAG: recupera documentos y consulta el LLM con el contexto.

    Soporta tanto un `retriever` (si el vectorstore expone uno) como un `vectorstore`
    directo (usa `similarity_search` como fallback).
    """
    def __init__(self, llm, retriever=None, vectorstore=None, k: int = 1):
        self.llm = llm
        self.retriever = retriever
        self.vectorstore = vectorstore
        self.k = k

    def _extract_texts(self, docs):
        parts = []
        for d in docs:
            if hasattr(d, "page_content"):
                parts.append(d.page_content)
            elif isinstance(d, dict) and "page_content" in d:
                parts.append(d["page_content"])
            else:
                # intentar str fallback
                parts.append(str(d))
        return parts

    def _retrieve(self, query: str):
        # Recuperación simple - solo los k documentos más relevantes
        if self.retriever is not None:
            for fn in ("get_relevant_documents", "get_relevant_results", "get_relevant_items"):
                if hasattr(self.retriever, fn):
                    try:
                        return getattr(self.retriever, fn)(query)
                    except TypeError:
                        return getattr(self.retriever, fn)(query, k=self.k)

        # Fallback: usar vectorstore directamente
        if self.vectorstore is not None:
            if hasattr(self.vectorstore, "similarity_search"):
                return self.vectorstore.similarity_search(query, k=self.k)
            if hasattr(self.vectorstore, "similarity_search_with_score"):
                pairs = self.vectorstore.similarity_search_with_score(query, k=self.k)
                return [p[0] for p in pairs]

        raise AttributeError("No hay método de recuperación disponible en retriever ni en vectorstore")

    def run(self, query: str) -> str:
        docs = self._retrieve(query)
        texts = self._extract_texts(docs)
        context = "\n\n".join(texts)

        # Prompt para respuestas muy breves (una sola oración) pero amigables.
        # El modelo debe apoyarse en las tablas; si no encuentra el dato exacto,
        # puede hacer una estimación razonable y decirlo explícitamente.
        prompt = f"""Eres un asistente de análisis de datos de ventas.

DATOS (tablas y resúmenes derivados del Excel):
{context}

PREGUNTA DEL USUARIO:
{query}

INSTRUCCIONES:
- Si ves el dato exacto en las tablas, responde en **UNA SOLA ORACIÓN**
  en español, clara y corta (por ejemplo: "En 2023 hubo 496 ventas.").
- Si no encuentras el dato exacto pero hay información relacionada,
  haz una estimación razonable y aclara en esa misma oración que es
  una estimación.
- Si en las tablas no existe la información necesaria (por ejemplo,
  una columna que no está en el Excel), responde con una sola oración
  amable explicando que no hay datos suficientes.
- NUNCA respondas solo con un número ni con más de una oración.

RESPUESTA (una única oración, tono cordial):"""

        # Llamar al LLM - ChatOpenAI usa invoke()
        try:
            response = self.llm.invoke(prompt)
            # ChatOpenAI devuelve un AIMessage, extraemos el contenido
            if hasattr(response, 'content'):
                return response.content
            return str(response)
        except Exception as e:
            # Si hay error con OpenAI, devolver contexto directamente (DEMO MODE)
            print(f"[WARN] Error LLM (usando modo demo): {str(e)[:100]}")
            return f"Basandome en los datos disponibles, encontre la siguiente informacion relevante:\n\n{context[:1000]}..."

def load_vectorstore(path: str):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Intentar cargar el índice permitiendo la deserialización peligrosa
    # (necesario si el vectorstore usa pickle para los metadatos).
    # Esto es seguro sólo si confías en el origen de `path` (p. ej. lo generaste tú).
    try:
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    except TypeError:
        # Versiones antiguas de la librería no aceptan ese argumento; caer
        # al comportamiento anterior (más estricto) y dejar que el error
        # posterior indique si es inseguro.
        return FAISS.load_local(path, embeddings)
    except ValueError as e:
        # Reenviar con mensaje más claro
        raise ValueError(
            str(e)
            + "\nSi confías en el origen del vectorstore, puedes permitir la deserialización estableciendo `allow_dangerous_deserialization=True`."
        )

def build_qa():
    # cargar vectorstore
    vectorstore = load_vectorstore(os.getenv("VECTORSTORE_DIR", "../vectorstore"))
    # Intentar generar un retriever; si falla, pasamos el vectorstore a SimpleRAG
    try:
        retriever = vectorstore.as_retriever(search_kwargs={"k": 1})  # Solo EL documento más relevante
    except Exception:
        retriever = None

    # Determinar qué proveedor de LLM usar
    llm_provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    
    if llm_provider == "ollama":
        # Usar Ollama (modelo local)
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", "llama3.2")
        
        print(f"[INFO] Usando Ollama con modelo: {model}")
        print(f"[INFO] URL del servidor Ollama: {base_url}")
        
        llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.1,  # Un poco de creatividad para mejor razonamiento
            num_ctx=4096      # Más contexto para procesar más datos
        )
    
    elif llm_provider == "openai":
        # Usar OpenAI (API externa)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Falta la variable OPENAI_API_KEY en el archivo env")
        
        print(f"[INFO] Usando OpenAI con modelo: {os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')}")
        
        llm = ChatOpenAI(
            temperature=0,
            openai_api_key=api_key,
            model_name=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        )
    
    else:
        raise ValueError(f"LLM_PROVIDER no válido: {llm_provider}. Usa 'ollama' o 'openai'")

    # Usar nuestra implementación simple RAG
    return SimpleRAG(llm=llm, retriever=retriever, vectorstore=vectorstore, k=1)
