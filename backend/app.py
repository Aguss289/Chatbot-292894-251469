from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import os
import re
from dotenv import load_dotenv
from rag_pipeline import build_qa

# Cargar variables de entorno desde `backend/env` (si existe)
load_dotenv(os.path.join(os.path.dirname(__file__), "env"))



app = FastAPI(title="Retail360 RAG Chatbot")

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryIn(BaseModel):
	question: str


class QueryOut(BaseModel):
	answer: str
	sources: List[str] = Field(default_factory=list)


qa = None


def is_greeting(text: str) -> bool:
	text_clean = re.sub(r"[¡!¿?\.,;:]", "", text or "").strip().lower()
	if not text_clean:
		return False

	greetings = [
		"hola",
		"buen dia",
		"buen día",
		"buenas",
		"buenas tardes",
		"buenas noches",
		"hey",
		"hi",
		"hello",
	]

	# Coincidencia exacta o comienza con un saludo habitual
	return any(
		text_clean == g or text_clean.startswith(g + " ")
		for g in greetings
	)


@app.on_event("startup")
def startup_event():
	global qa
	qa = build_qa()


@app.post("/query", response_model=QueryOut)
def query(q: QueryIn):
	global qa

	# Respuesta especial para saludos sencillos (sin usar RAG ni datos del Excel)
	if is_greeting(q.question):
		return {
			"answer": (
				"¡Hola! Soy tu asistente de análisis de ventas. "
				"Puedes preguntarme cosas como \"¿Cuántas ventas hubo en 2023?\" "
				"o \"¿Cuál es el producto más vendido?\""
			),
			"sources": [],
		}

	if qa is None:
		raise HTTPException(status_code=500, detail="QA pipeline no inicializado")

	# Ejecutar retrieval + LLM
	try:
		res = qa.run(q.question)
		return {"answer": res, "sources": []}
	except Exception as e:
		print(f"[ERROR] Query failed: {str(e)}")
		raise HTTPException(status_code=500, detail=f"Error al procesar consulta: {str(e)[:200]}")



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