## Chatbot RAG sobre Excel (React + FastAPI + Ollama)

Chatbot para consultar datos de ventas a partir del archivo de Excel `TrabajoFinalPowerBI_v2 (1).xlsx`.  
Usa un backend FastAPI con RAG basado en **LangChain** (FAISS + modelos LLM) y un frontend React con Vite.

Estructura principal:
- `backend/`: API FastAPI + RAG con LangChain (carga del Excel, generación y uso del vectorstore).
- `frontend/`: aplicación React (Vite + Tailwind).

---

### 1. Requisitos

- **Python** 3.10+  
- **Node.js** 18+  
- **Ollama** instalado y ejecutándose  
  - Descarga desde `https://ollama.com`  
  - Descargar modelo (recomendado):

  ```bash
  ollama pull llama3.2
  ```

---

### 2. Backend – instalación inicial

Desde la raíz del proyecto:

```powershell
cd backend
python -m venv ..\venv      # solo si aún no existe
..\venv\Scripts\activate
pip install -r requirements.txt
```

Configura el archivo `backend/env` (puedes copiar desde `backend/env.example`) con, al menos:

```text
DATASET_PATH=../TrabajoFinalPowerBI_v2 (1).xlsx
VECTORSTORE_DIR=../vectorstore

LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

Genera el vectorstore FAISS a partir del Excel (solo cuando cambie el dataset):

```powershell
cd backend
..\venv\Scripts\activate
python embeddings_builder.py
```

---

### 3. Backend – ejecutar la API

En una terminal:

```powershell
cd backend
..\venv\Scripts\activate
uvicorn app:app --host 127.0.0.1 --port 8000
```

La API quedará disponible en `http://127.0.0.1:8000`.

---

### 4. Frontend – instalación y ejecución

1. Instalar dependencias del frontend (solo la primera vez):

   ```powershell
   cd frontend
   npm install
   ```

2. Levantar el frontend (desde la raíz o desde `frontend`):

   - Opción A – desde la **raíz** del proyecto:

     ```powershell
     cd <ruta-del-proyecto>
     npm run dev
     ```

   - Opción B – directamente en `frontend`:

     ```powershell
     cd frontend
     npm run dev
     ```

   Vite se levanta normalmente en `http://127.0.0.1:5173/`.

El archivo `frontend/vite.config.js` ya está configurado para hacer proxy de `/api/*` al backend en `http://localhost:8000`.

---

### 5. Flujo completo recomendado

1. **Terminal 1 – Backend**
   ```powershell
   cd backend
   ..\venv\Scripts\activate
   uvicorn app:app --host 127.0.0.1 --port 8000
   ```

2. **Terminal 2 – Frontend**
   ```powershell
   cd <ruta-del-proyecto>
   npm run dev
   ```

3. Abrir en el navegador `http://127.0.0.1:5173` y hacer preguntas como:
   - `¿Cuántas ventas hubo en 2023?`
   - `¿Cuál es el producto más vendido?`
   - `¿Cuántas ventas hubo en marzo de 2023?`

---

### 6. Notas

- El backend usa `data_loader.py` para generar un solo documento agregado (ventas por año, mes, producto, cliente, ciudad) y lo indexa en FAISS.
- El modelo (Ollama u OpenAI) responde siempre apoyándose en ese contexto; no hay respuestas hardcodeadas.
- Si cambias el Excel, vuelve a ejecutar `python embeddings_builder.py` antes de levantar el backend.

### Integrantes

- Santiago Chemello (251469)
- Agustin Garcia (292894)