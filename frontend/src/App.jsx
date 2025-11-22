import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';
import { askBot } from './api/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSendMessage = async (text) => {
    const userMessage = {
      id: Date.now(),
      text: text,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);

    setIsTyping(true);

    try {
      const response = await askBot(text);

      const botMessage = {
        id: Date.now() + 1,
        text: response.answer,
        isUser: false,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error al obtener respuesta:', error);

      const errorMessage = {
        id: Date.now() + 1,
        text: 'Lo siento, hubo un error al procesar tu pregunta. Por favor intenta de nuevo.',
        isUser: false,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-grid">
      {/* Header principal */}
      <header className="chat-header border-b border-white/20">
        <div className="chat-header-inner py-4 px-4">
          <div className="flex items-center gap-3">
            <div className="bot-orb">
              {/* Icono minimalista de chatbot */}
              <svg
                className="h-5 w-5 text-sky-300"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <rect
                  x="4"
                  y="5"
                  width="16"
                  height="12"
                  rx="5"
                  stroke="currentColor"
                  strokeWidth="1.6"
                />
                <circle cx="10" cy="11" r="1.2" fill="currentColor" />
                <circle cx="14" cy="11" r="1.2" fill="currentColor" />
                <path
                  d="M9 15c.6.6 1.4 1 2.99 1C13.6 16 14.4 15.6 15 15"
                  stroke="currentColor"
                  strokeWidth="1.3"
                  strokeLinecap="round"
                />
                <path
                  d="M7 7V4.8C7 4.35817 7.35817 4 7.8 4H9"
                  stroke="currentColor"
                  strokeWidth="1.4"
                  strokeLinecap="round"
                />
              </svg>
            </div>
            <div>
              <h1 className="chat-header-title">
                Chatbot Inteligente
              </h1>
              <p className="text-xs md:text-sm text-slate-300/90 mt-0.5">
                Asistente para explorar tus datos de ventas con respuestas claras y accionables.
              </p>
            </div>
          </div>
          <div className="hidden sm:block">
            <span className="chat-header-pill">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              Disponible ahora
            </span>
          </div>
        </div>
      </header>

      {/* Contenedor principal del chat */}
      <main className="flex-1 flex items-center justify-center px-3 py-5 sm:px-4 sm:py-8">
        <section className="chat-shell animate-shell-in">
          <ChatWindow messages={messages} isTyping={isTyping} />
          <MessageInput onSend={handleSendMessage} disabled={isTyping} />
        </section>
      </main>

      {/* Footer */}
      <footer className="text-center text-slate-400 text-[11px] pb-3 px-3">
        <p className="backdrop-blur-sm inline-flex items-center gap-2 rounded-full border border-slate-700/60 bg-slate-900/60 px-3 py-1 shadow-md shadow-slate-950/60">
          <span className="h-1.5 w-1.5 rounded-full bg-sky-400" />
          React · Vite · Tailwind CSS
        </p>
      </footer>
    </div>
  );
}

export default App;

