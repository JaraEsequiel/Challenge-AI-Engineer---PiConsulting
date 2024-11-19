import React from 'react';
import { Message } from '../types/chat';

interface MessageListProps {
  messages: Message[];
}

export function MessageList({ messages }: MessageListProps) {
  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className="flex flex-col bg-white rounded-lg shadow-sm p-4 max-w-[80%] ml-auto"
        >
          <div className="flex items-center justify-between mb-2">
            <span className="font-medium text-gray-800">{msg.user_name}</span>
            <span className="text-xs text-gray-500">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </span>
          </div>
          <p className="text-gray-700">{msg.question}</p>
        </div>
      ))}
    </div>
  );
}