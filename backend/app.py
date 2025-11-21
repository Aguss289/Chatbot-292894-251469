from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv
from backend.rag_pipeline import build_qa

# Cargar variables de entorno desde `backend/env` (si existe)
load_dotenv(os.path.join(os.path.dirname(__file__), "env"))



app = FastAPI(title="Retail360 RAG Chatbot")


class QueryIn(BaseModel):
	question: str


class QueryOut(BaseModel):
	answer: str
	sources: List[str] = Field(default_factory=list)


qa = None


@app.on_event("startup")
def startup_event():
	global qa
	qa = build_qa()


@app.post("/query", response_model=QueryOut)
def query(q: QueryIn):
	global qa
	if qa is None:
		raise HTTPException(status_code=500, detail="QA pipeline no inicializado")

	# Ejecutar retrieval + LLM
	# Nuestro simple RAG expone `run(question)` que devuelve texto
	res = qa.run(q.question)
	return {"answer": res, "sources": []}



@app.post("/reindex")
def reindex():
	# Endpoint sencillo para reconstruir el índice desde el Excel
	from data_loader import build_documents_from_excel
	from embeddings_builder import compute_embeddings, build_faiss_index

	path = os.getenv("DATASET_PATH", "F:/ORT/8vo Semestre/SISTEMA SOPORTE DECISION/Obligatorio IA/TrabajoFinalPowerBI_v2 (1).xlsx")
	docs = build_documents_from_excel(path)
	embs = compute_embeddings(docs)
	build_faiss_index(embs, docs, os.getenv("VECTORSTORE_DIR", "./vectorstore"))
	return {"status": "ok", "docs_indexed": len(docs)}