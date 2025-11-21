import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI


class SimpleRAG:
    """Pequeña implementación RAG: recupera documentos y consulta el LLM con el contexto.

    Soporta tanto un `retriever` (si el vectorstore expone uno) como un `vectorstore`
    directo (usa `similarity_search` como fallback).
    """
    def __init__(self, llm, retriever=None, vectorstore=None, k: int = 6):
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
        # Intentar usar retriever primero
        if self.retriever is not None:
            # varios wrappers pueden exponer distintos nombres
            for fn in ("get_relevant_documents", "get_relevant_results", "get_relevant_items"):
                if hasattr(self.retriever, fn):
                    try:
                        return getattr(self.retriever, fn)(query)
                    except TypeError:
                        # algunas implementaciones esperan kwargs
                        return getattr(self.retriever, fn)(query, k=self.k)

        # Fallback: usar vectorstore directamente
        if self.vectorstore is not None:
            if hasattr(self.vectorstore, "similarity_search"):
                return self.vectorstore.similarity_search(query, k=self.k)
            if hasattr(self.vectorstore, "similarity_search_with_score"):
                # devuelve tuplas (doc, score)
                pairs = self.vectorstore.similarity_search_with_score(query, k=self.k)
                return [p[0] for p in pairs]

        raise AttributeError("No hay método de recuperación disponible en retriever ni en vectorstore")

    def run(self, query: str) -> str:
        docs = self._retrieve(query)
        texts = self._extract_texts(docs)
        context = "\n\n".join(texts)

        prompt = f"Usa el siguiente contexto para responder de forma concisa:\n\n{context}\n\nPregunta: {query}\nRespuesta:"

        # Llamar al LLM - intentar varias APIs
        try:
            return self.llm(prompt)
        except TypeError:
            if hasattr(self.llm, "generate"):
                out = self.llm.generate([prompt])
                try:
                    return out.generations[0][0].text
                except Exception:
                    return str(out)
            if hasattr(self.llm, "predict"):
                return self.llm.predict(prompt)
            raise

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
    vectorstore = load_vectorstore(os.getenv("VECTORSTORE_DIR", "./vectorstore"))
    # Intentar generar un retriever; si falla, pasamos el vectorstore a SimpleRAG
    try:
        retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
    except Exception:
        retriever = None

    # cargar modelo LLM
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Falta la variable OPENAI_API_KEY en el archivo .env")

    llm = OpenAI(
        temperature=0,
        openai_api_key=api_key,
        model_name=os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )

    # Usar nuestra implementación simple RAG
    return SimpleRAG(llm=llm, retriever=retriever, vectorstore=vectorstore, k=6)
