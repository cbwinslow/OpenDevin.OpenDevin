import { useState } from 'react';

export default function ChatPage() {
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState('');

  const sendMessage = () => {
    if (!input) return;
    setMessages([...messages, input]);
    setInput('');
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <div className="border border-neutral-700 rounded p-4 h-64 overflow-y-auto mb-2">
        {messages.map((m, i) => (
          <div key={i} className="mb-1">
            {m}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 bg-neutral-800 rounded p-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message"
        />
        <button
          className="bg-blue-600 rounded px-4"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}
