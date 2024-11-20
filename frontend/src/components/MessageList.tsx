import { useState } from 'react';
import { Message, ReactionPayload } from '../types/chat';
import { MessageReactions } from './MessageReactions';
import { API_URL } from '../utils/config';

interface MessageListProps {
  messages: Message[];
  username: string;
  onMessageUpdate: (updatedMessage: Message) => void;
}

export function MessageList({ messages, username, onMessageUpdate }: MessageListProps) {
  const [loadingReactions, setLoadingReactions] = useState<Record<number, boolean>>({});

  const handleReaction = async (messages: Message[]) => {

    const question = messages.filter(m => m.user_name === username).pop()?.question;
    const answer = messages.filter(m => m.user_name === 'assistant').pop()?.question;
    if (!question || !answer) return;
    try {
      const payload: ReactionPayload = {
        question,
        answer,
      };

      const response = await fetch(`${API_URL}/rag/upload_qna`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error('Failed to update reaction');

      const updatedMessage = messages.filter(m => m.user_name === username).pop();
      if (!updatedMessage) return;

      if (updatedMessage.userReaction) {
        onMessageUpdate(updatedMessage);
      }

    } catch (error) {
      console.error('Error updating reaction:', error);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`flex flex-col rounded-lg shadow-sm p-4 max-w-[80%] 
            ${msg.user_name === 'assistant'
              ? 'mr-auto bg-gray-700'
              : 'ml-auto bg-white'
            }`}
        >
          <div className="flex items-center justify-between mb-2">
            <span className="font-medium">
              {msg.user_name}
            </span>
            <span className="text-xs">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </span>
          </div>
          <p>
            {msg.question}
          </p>
          {msg.user_name === 'assistant' && (
            <MessageReactions
              userReaction={msg.userReaction}
              onReact={() => handleReaction(messages)}
              isLoading={loadingReactions[msg.id] || false}
            />
          )}
        </div>
      ))}
    </div>
  );
}