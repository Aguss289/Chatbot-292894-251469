import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from data_loader import build_documents_from_excel
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()


def build_vectorstore():
    dataset_path = os.getenv("DATASET_PATH", "dataset.xlsx")
    output_dir = os.getenv("VECTORSTORE_DIR", "./vectorstore")

    print(f"[INFO] Cargando dataset desde: {dataset_path}")
    print(f"[INFO] Guardando vectorstore en: {output_dir}")

    # Si el archivo no existe en la ruta indicada, intentar búsqueda automática
    if not os.path.exists(dataset_path):
        print(f"[WARN] Dataset no encontrado en '{dataset_path}'. Buscando archivos .xlsx/.xls en el proyecto...")
        found = None
        for root, _, files in os.walk("."):
            for fname in files:
                if fname.lower().endswith((".xlsx", ".xls")):
                    found = os.path.join(root, fname)
                    break
            if found:
                break

        if found:
            dataset_path = found
            print(f"[INFO] Usando dataset encontrado: {dataset_path}")
        else:
            raise FileNotFoundError(
                f"Dataset no encontrado. Poner el archivo .xlsx en el proyecto o fijar la variable de entorno DATASET_PATH. Buscadas: '{os.getcwd()}'"
            )

    docs = build_documents_from_excel(dataset_path)
    print(f"[INFO] Documentos generados: {len(docs)}")

    # convertir dicts a Document de LangChain
    lc_docs = [Document(page_content=d.get("page_content", ""), metadata=d.get("metadata", {})) for d in docs]

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Crear FAISS correctamente a partir de Documents
    vectorstore = FAISS.from_documents(lc_docs, embeddings)

    # Guardar FAISS correctamente
    vectorstore.save_local(output_dir)

    print("[OK] Vectorstore generado correctamente.")


if __name__ == "__main__":
    build_vectorstore()
