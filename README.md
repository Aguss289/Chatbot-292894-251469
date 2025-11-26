# Chatbot RAG - Retail 360
## Consulta inteligente de datos de ventas

Chatbot basado en **RAG (Retrieval-Augmented Generation)** que permite consultar datos de ventas en lenguaje natural a partir de un archivo Excel.

**Stack tecnológico:**
- **Backend**: FastAPI + LangChain + FAISS + Ollama
- **Frontend**: React + Vite + TailwindCSS
- **Datos**: Excel con tablas de Ventas, Productos y Clientes

---

## 📋 Requisitos previos

Antes de ejecutar la aplicación, asegúrate de tener instalado:

| Requisito | Versión | Descarga |
|-----------|---------|----------|
| **Python** | 3.10+ | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org/) |
| **Ollama** | Última | [ollama.com](https://ollama.com) |

### Configuración de Ollama

Después de instalar Ollama, descarga el modelo (recomendado `llama3.2`):

```bash
ollama pull llama3.2
```

Verifica que Ollama esté corriendo en segundo plano (se inicia automáticamente después de la instalación).

---

## 🚀 Instalación (solo la primera vez)

### 1. Clonar el repositorio

```powershell
git clone <URL_DEL_REPO>
cd <nombre-del-proyecto>
```

### 2. Configurar el backend

```powershell
# Crear entorno virtual
cd backend
python -m venv ..\venv

# Activar entorno virtual
..\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia el archivo de ejemplo y configúralo:

```powershell
copy backend\env.example backend\env
```

Edita `backend/env` con tu configuración (valores por defecto ya están listos para Ollama):

```env
DATASET_PATH=../TrabajoFinalPowerBI_v2 (1).xlsx
VECTORSTORE_DIR=../vectorstore

LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

### 4. Generar el índice vectorial (vectorstore)

Este paso procesa el Excel y crea el índice FAISS:

```powershell
cd backend
..\venv\Scripts\activate
python embeddings_builder.py
```

Deberías ver:
```
[INFO] Generando documentos de resumen optimizados...
[INFO] Total de documentos: 1
[OK] Vectorstore generado correctamente.
```

### 5. Instalar dependencias del frontend

```powershell
cd frontend
npm install
```

---

## ▶️ Ejecutar la aplicación

### Método 1: Script automático

Desde la **raíz del proyecto**, ejecuta:

```powershell
.\start.bat
```

Esto abrirá **dos ventanas de terminal**:
- Una con el **backend** (FastAPI en puerto 8000)
- Otra con el **frontend** (Vite en puerto 5173)

**Luego abre tu navegador en:** `http://127.0.0.1:5173`

Para detener ambos servicios, simplemente cierra las ventanas de terminal.

---

### Método 2: Manual (dos terminales)

Si prefieres control total, abre dos terminales:

**Terminal 1 - Backend:**
```powershell
cd backend
..\venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

Luego abre `http://127.0.0.1:5173` en tu navegador.

---

## 💬 Uso del chatbot

Una vez que la aplicación esté corriendo, puedes hacer preguntas como:

### Ejemplos de consultas:

**Sobre ventas:**
- "¿Cuántas ventas hubo en 2023?"
- "¿Cuántas ventas hubo en marzo de 2023?"
- "¿Cuál fue el total de ingresos en 2024?"

**Sobre productos:**
- "¿Cuál es el producto más vendido?"
- "¿Qué categoría generó más ingresos?"
- "Muéstrame el top 3 de productos"

**Sobre clientes:**
- "¿Cuál es el cliente con más compras?"
- "¿Qué ciudad tiene más ventas?"
- "¿Cuántos clientes diferentes compraron?"

**Nota importante:** El dataset solo contiene información de **ventas**, **productos** (con categorías), **clientes** (con ciudades) y **fechas**. No incluye datos sobre vendedores, canales de venta, formas de pago ni locales específicos.

---

## 🔄 Actualizar datos

Si modificas el archivo Excel (`TrabajoFinalPowerBI_v2 (1).xlsx`), debes regenerar el vectorstore:

```powershell
cd backend
..\venv\Scripts\activate
python embeddings_builder.py
```

Luego reinicia el backend.

---

### 6. Notas

- El backend usa `data_loader.py` para generar un solo documento agregado (ventas por año, mes, producto, cliente, ciudad) y lo indexa en FAISS.
- El modelo (Ollama u OpenAI) responde siempre apoyándose en ese contexto; no hay respuestas hardcodeadas.
- Si cambias el Excel, vuelve a ejecutar `python embeddings_builder.py` antes de levantar el backend.

### Integrantes

- Santiago Chemello (251469)
- Agustin Garcia (292894)