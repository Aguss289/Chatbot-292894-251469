/**
 * API para conectar con el backend RAG (FastAPI)
 * El proxy de Vite redirige /api/query -> http://localhost:8000/query
 */

export async function askBot(question) {
  try {
    const response = await fetch('/api/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data; // { answer: "...", sources: [...] }
  } catch (error) {
    console.error('Error al consultar el backend:', error);
    throw error;
  }
}

