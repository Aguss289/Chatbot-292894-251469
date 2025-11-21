# Chatbot-292894-251469

## Setup y ejecución (Windows - PowerShell)

Sigue estos pasos después de clonar el repositorio para levantar la aplicación localmente.

1. Clonar el repositorio

```powershell
git clone <URL_DEL_REPO>
cd Chatbot-292894-251469
```

2. Crear y activar el entorno virtual (venv)

```powershell
python -m venv venv
venv\Scripts\Activate
```

3. Instalar dependencias

```powershell
# Actualizar pip (opcional pero recomendado)
python -m pip install -U pip
# Instalar requerimientos del backend
pip install -r backend\requirements.txt
```

4. Configurar variables de entorno

Rellena el archivo `backend/env` con tus valores locales. Asegúrate de NO commitear ese archivo.

- Ejemplo mínimo (no compartir):

```text
DATASET_PATH=F:/ruta/a/tu/dataset.xlsx
VECTORSTORE_DIR=./vectorstore
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
HOST=0.0.0.0
PORT=8000
```

El proyecto ya incluye `.gitignore` que excluye `venv/` y `backend/env`.

5. Generar el vectorstore (si aún no existe)

Esto carga el Excel, crea documentos, calcula embeddings y guarda un FAISS local.

```powershell
# Desde la raíz del repo
venv\Scripts\Activate
python backend\embeddings_builder.py
```

6. Arrancar la API (uvicorn)

```powershell
venv\Scripts\Activate
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

7. Probar la API

- Abre la documentación interactiva en: `http://127.0.0.1:8000/docs`
- O envía una petición POST al endpoint `/query` con JSON:

```json
{ "question": "¿Qué es Retail360?" }
```

Notas y recomendaciones

- Si `backend/env` contiene claves sensibles que accidentalmente fueron commiteadas, rota esas claves inmediatamente.
- Si ves advertencias sobre `HuggingFaceEmbeddings` o `ChatOpenAI`, son avisos de deprecación: puedes actualizar las importaciones instalando `langchain-huggingface` o usando `ChatOpenAI` según convenga.
- Para reproducibilidad en deployment, considera generar un `requirements-frozen.txt` con `pip freeze > backend/requirements-frozen.txt` y pinnear versiones.

Soporte

- Si tienes errores durante el arranque, copia el traceback y pégalo en una nueva issue o compártelo aquí para que te guíe.
# Chatbot-292894-251469