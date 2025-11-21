## Chatbot RAG sobre Excel (React + FastAPI + Ollama)

Este proyecto implementa un chatbot de consulta de datos que:
- Lee el archivo `TrabajoFinalPowerBI_v2 (1).xlsx` (tablas de **Ventas**, **Clientes** y **Productos**),
- Lo transforma en texto/tablas agregadas,
- Indexa ese contenido en un vectorstore FAISS,
- Y responde preguntas usando un modelo local de **Ollama** (por defecto `llama3.2`).

La app tiene:
- **Backend** en `backend/` (FastAPI + LangChain),
- **Frontend** React en `src/` con Vite (raíz del proyecto).

---

### 1. Requisitos

- **Python** 3.10+  
- **Node.js** 18+  
- **Ollama** instalado y ejecutándose  
  - Descarga desde `https://ollama.com`  
  - En una terminal, descarga el modelo (recomendado):

  ```bash
  ollama pull llama3.2
  ```

---

### 2. Configurar backend (una sola vez)

Desde la raíz del proyecto:

```powershell
cd backend
python -m venv ..\venv     # si aún no existe
..\venv\Scripts\activate
pip install -r requirements.txt
```

Configura el archivo `backend/env` (si no existe, créalo) con al menos:

```text
DATASET_PATH=../TrabajoFinalPowerBI_v2 (1).xlsx
VECTORSTORE_DIR=../vectorstore

LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

HOST=0.0.0.0
PORT=8002
```

Genera el vectorstore FAISS a partir del Excel:

```powershell
cd backend
..\venv\Scripts\activate
python embeddings_builder.py
```

---

### 3. Levantar el backend (API FastAPI)

En una terminal:

```powershell
cd backend
..\venv\Scripts\activate
uvicorn app:app --host 0.0.0.0 --port 8002
```

La API queda en `http://localhost:8002` y carga el vectorstore generado más el modelo de Ollama.

---

### 4. Configurar y levantar el frontend (React + Vite)

Desde la **raíz** del proyecto:

```powershell
cd C:\Users\Chatbot-292894-251469   # o la ruta donde tengas el repo
npm install
npm run dev
```

Vite mostrará la URL local, por ejemplo:

```text
Local: http://localhost:5174/
```

El archivo `vite.config.js` ya está configurado para hacer proxy de todas las llamadas
`/api/...` al backend en `http://localhost:8002`.

Abre en el navegador la URL que indica Vite (p.ej. `http://localhost:5174`) y ya
puedes usar el chatbot.

---

### 5. Flujo de ejecución completo

1. **Terminal 1 – Backend**
   ```powershell
   cd backend
   ..\venv\Scripts\activate
   uvicorn app:app --host 0.0.0.0 --port 8002
   ```

2. **Terminal 2 – Frontend**
   ```powershell
   cd C:\Users\Chatbot-292894-251469   # raíz del proyecto
   npm run dev
   ```

3. Navega a la URL que muestre Vite (p.ej. `http://localhost:5174`) y haz preguntas
   como:
   - “¿Cuántas ventas hubo en 2023?”
   - “¿Cuál es el producto más vendido?”
   - “¿Cuántas ventas hubo en marzo de 2023?”

---

### 6. Notas

- El backend procesa el Excel con `data_loader.py`, genera un único documento con
  tablas agregadas (ventas por año, mes, producto, cliente, ciudad) y lo indexa en FAISS.  
- El modelo de Ollama responde **leyendo esas tablas**, no hay respuestas hardcodeadas.  
- Si cambias el Excel, debes volver a ejecutar `python embeddings_builder.py` para
  regenerar el vectorstore.


