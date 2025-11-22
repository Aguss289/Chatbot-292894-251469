import React, { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';

const ChatWindow = ({ messages, isTyping }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const hasMessages = messages.length > 0;

  return (
    <div className="chat-window">
      {!hasMessages ? (
        <div className="flex items-center justify-center h-full">
          <div className="text-center text-slate-300/90">
            <svg
              className="mx-auto h-12 w-12 text-slate-500/80 mb-4 drop-shadow-md"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
              />
            </svg>
            <h3 className="text-lg font-semibold mb-1">Bienvenido</h3>
            <p className="text-sm text-slate-400 max-w-xs mx-auto">
              Cuéntame qué necesitas analizar o qué duda tienes sobre tus datos.
            </p>
          </div>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
              isUser={message.isUser}
            />
          ))}
          {isTyping && <MessageBubble isTyping={true} isUser={false} />}
          <div ref={messagesEndRef} />
        </>
      )}
    </div>
  );
};

export default ChatWindow;

