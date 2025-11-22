import React from 'react';

const MessageBubble = ({ message, isUser, isTyping }) => {
  const formatTime = (date) => {
    const d = date instanceof Date ? date : new Date(date);
    const hours = d.getHours().toString().padStart(2, '0');
    const minutes = d.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
  };

  const bubbleAnimationClass = isUser
    ? 'animate-message-in-user'
    : 'animate-message-in-bot';

  const bubbleColorClass = isUser
    ? 'bg-sky-600 text-slate-50 rounded-br-none border border-sky-500/70 shadow-[0_14px_40px_rgba(15,23,42,0.95)]'
    : 'bg-slate-900/95 text-slate-100 rounded-bl-none border border-slate-700/80 shadow-[0_16px_45px_rgba(15,23,42,0.95)]';

  return (
    <div
      className={`flex mb-3 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div
        className={`max-w-[76%] md:max-w-[68%] ${
          isUser ? 'order-2' : 'order-1'
        }`}
      >
        <div
          className={`rounded-2xl px-4 py-3 text-sm md:text-[15px] leading-relaxed transition-transform duration-150 hover:-translate-y-0.5 hover:shadow-2xl ${bubbleAnimationClass} ${bubbleColorClass}`}
        >
          {isTyping ? (
            <div className="flex space-x-2 items-center">
              <div
                className="w-2 h-2 bg-slate-300 rounded-full animate-bounce"
                style={{ animationDelay: '0ms' }}
              ></div>
              <div
                className="w-2 h-2 bg-slate-300 rounded-full animate-bounce"
                style={{ animationDelay: '150ms' }}
              ></div>
              <div
                className="w-2 h-2 bg-slate-300 rounded-full animate-bounce"
                style={{ animationDelay: '300ms' }}
              ></div>
            </div>
          ) : (
            <p className="whitespace-pre-wrap break-words">
              {message?.text}
            </p>
          )}
        </div>
        {!isTyping && message?.timestamp && (
          <p
            className={`text-[11px] text-slate-500 mt-1 ${
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

