import React, { useState } from 'react';
import { Send, LogOut } from 'lucide-react';
import { MessageList } from './MessageList';
import { useSessionMessages } from '../hooks/useSessionMessages';
import { Message } from '../types/chat';
import { API_URL } from '../utils/config';

interface ChatScreenProps {
  username: string;
  onLogout: () => void;
}

export function ChatScreen({ username, onLogout }: ChatScreenProps) {
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { messages, setMessages, clearMessages } = useSessionMessages();

  const handleLogout = () => {
    clearMessages();
    onLogout();
  };

  const handleMessageUpdate = (updatedMessage: Message) => {
    setMessages(messages.map(msg =>
      msg.id === updatedMessage.id ? updatedMessage : msg
    ));
  };

  const sendMessage = async (e: React.FormEvent) => {
    setMessage('');
    e.preventDefault();
    const input = message;
    const newMessage: Message = {
      id: Date.now(),
      user_name: username,
      question: input,
      timestamp: new Date(),
      userReaction: false,
    };
    setMessages([...messages, newMessage]);

    if (!message.trim()) return;

    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/llm/generate_message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_name: username,
          question: input,
        }),
      });

      if (!response.ok) throw new Error('Error al enviar el mensaje');

      const data = await response.json();
      const newResponseMessage: Message = {
        id: Date.now(),
        user_name: 'assistant',
        question: data.answer,
        timestamp: new Date(),
        userReaction: false,
      };

      setMessages([...messages, newMessage, newResponseMessage]);
      setMessage('');
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center">
            <span className="text-indigo-600 font-medium">
              {username.charAt(0).toUpperCase()}
            </span>
          </div>
          <span className="font-medium text-gray-700">{username}</span>
        </div>
        <button
          onClick={handleLogout}
          className="text-gray-600 hover:text-gray-800 flex items-center space-x-1"
        >
          <LogOut className="w-5 h-5" />
          <span>Salir</span>
        </button>
      </div>

      <MessageList
        messages={messages}
        username={username}
        onMessageUpdate={handleMessageUpdate}
      />

      {/* Message Input */}
      <form onSubmit={sendMessage} className="p-4 bg-white border-t">
        <div className="flex space-x-4">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Escribe tu mensaje..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading}
            className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors flex items-center space-x-2"
          >
            {isLoading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Cargando...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Enviar</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}