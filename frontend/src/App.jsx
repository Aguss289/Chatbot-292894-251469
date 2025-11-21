import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';
import { askBot } from './api/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSendMessage = async (text) => {
    // Crear mensaje del usuario
    const userMessage = {
      id: Date.now(),
      text: text,
      isUser: true,
      timestamp: new Date(),
    };

    // Agregar mensaje del usuario al chat
    setMessages((prev) => [...prev, userMessage]);

    // Mostrar indicador de "typing..."
    setIsTyping(true);

    try {
      // Llamar a la API (mock por ahora)
      const response = await askBot(text);

      // Crear mensaje del bot
      const botMessage = {
        id: Date.now() + 1,
        text: response.answer,
        isUser: false,
        timestamp: new Date(),
      };

      // Agregar respuesta del bot
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error al obtener respuesta:', error);

      // Mensaje de error
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Lo siento, hubo un error al procesar tu pregunta. Por favor intenta de nuevo.',
        isUser: false,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      // Ocultar indicador de "typing..."
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-blue-600 text-white p-4 shadow-lg">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-xl md:text-2xl font-bold">🤖 Chatbot - Consulta de Datos</h1>
          <p className="text-sm text-blue-100 mt-1">Pregúntame lo que necesites</p>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 flex flex-col max-w-4xl w-full mx-auto bg-white shadow-xl overflow-hidden">
        <ChatWindow messages={messages} isTyping={isTyping} />
        <MessageInput onSend={handleSendMessage} disabled={isTyping} />
      </div>

      {/* Footer */}
      <footer className="text-center text-gray-500 text-xs py-3">
        <p>Powered by React + Vite + Tailwind CSS</p>
      </footer>
    </div>
  );
}

export default App;

