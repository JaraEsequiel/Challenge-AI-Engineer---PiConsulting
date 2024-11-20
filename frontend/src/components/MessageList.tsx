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
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingMessageId, setEditingMessageId] = useState<number | null>(null);
  const [editedAnswer, setEditedAnswer] = useState('');

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

  const handleEdit = async (messageId: number, question: string, originalAnswer: string) => {
    setEditingMessageId(messageId);
    setEditedAnswer(originalAnswer);
    setIsModalOpen(true);
  };

  const handleSubmitEdit = async () => {
    if (!editingMessageId) return;

    const question = messages.filter(m => m.user_name === username).pop()?.question;
    if (!question) return;

    try {
      const payload: ReactionPayload = {
        question,
        answer: editedAnswer,
      };

      const response = await fetch(`${API_URL}/rag/upload_qna`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error('Failed to update answer');

      setIsModalOpen(false);
      setEditingMessageId(null);
      setEditedAnswer('');
    } catch (error) {
      console.error('Error updating answer:', error);
    }
  };

  return (
    <>
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
              <div className="flex items-center gap-2">
                <MessageReactions
                  userReaction={msg.userReaction}
                  onReact={() => handleReaction(messages)}
                  isLoading={loadingReactions[msg.id] || false}
                />
                <button
                  onClick={() => handleEdit(msg.id, msg.question, msg.question)}
                  className="p-1 hover:bg-gray-600 rounded"
                >
                  ✏️
                </button>
              </div>
            )}
          </div>
        ))}
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg w-96">
            <h3 className="text-lg font-bold mb-4">Editar respuesta</h3>
            <textarea
              value={editedAnswer}
              onChange={(e) => setEditedAnswer(e.target.value)}
              className="w-full h-32 p-2 border rounded mb-4"
            />
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setIsModalOpen(false)}
                className="px-4 py-2 bg-gray-200 rounded"
              >
                Cancelar
              </button>
              <button
                onClick={handleSubmitEdit}
                className="px-4 py-2 bg-blue-500 text-white rounded"
              >
                Guardar
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}