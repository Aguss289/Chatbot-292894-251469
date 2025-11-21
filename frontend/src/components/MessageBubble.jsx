import React from 'react';

const MessageBubble = ({ message, isUser, isTyping }) => {
  // Función para formatear el timestamp
  const formatTime = (date) => {
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
  };

  return (
    <div className={`flex mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[70%] ${isUser ? 'order-2' : 'order-1'}`}>
        <div
          className={`rounded-lg px-4 py-3 shadow-md ${
            isUser
              ? 'bg-blue-600 text-white rounded-br-none'
              : 'bg-gray-200 text-gray-800 rounded-bl-none'
          }`}
        >
          {isTyping ? (
            <div className="flex space-x-2 items-center">
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          ) : (
            <p className="text-sm md:text-base whitespace-pre-wrap break-words">
              {message.text}
            </p>
          )}
        </div>
        {!isTyping && (
          <p
            className={`text-xs text-gray-500 mt-1 ${
              isUser ? 'text-right' : 'text-left'
            }`}
          >
            {formatTime(message.timestamp)}
          </p>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;

