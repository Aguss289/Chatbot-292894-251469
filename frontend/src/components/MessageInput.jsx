import React, { useState } from 'react';

const MessageInput = ({ onSend, disabled }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput('');
    }
  };

  return (
    <div className="chat-input-shell">
      <form onSubmit={handleSubmit} className="flex gap-2 sm:gap-3 items-end">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribe tu pregunta aquí..."
          disabled={disabled}
          className="chat-input"
        />
        <button
          type="submit"
          disabled={disabled || !input.trim()}
          className="chat-send-btn"
        >
          <span className="hidden sm:inline">Enviar</span>
          <span className="sm:hidden">→</span>
        </button>
      </form>
    </div>
  );
};

export default MessageInput;

