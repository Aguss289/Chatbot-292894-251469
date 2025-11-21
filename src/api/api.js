/**
 * API mock para simular respuestas del chatbot
 * En el futuro, reemplazar con llamadas reales a backend RAG
 */

export async function askBot(question) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ answer: "Respuesta simulada: " + question });
    }, 700);
  });
}

