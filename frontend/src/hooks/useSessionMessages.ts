import { useState, useEffect } from 'react';
import { Message } from '../types/chat';

const STORAGE_KEY = 'chat_messages';

export function useSessionMessages() {
  const [messages, setMessages] = useState<Message[]>(() => {
    const stored = sessionStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  });

  useEffect(() => {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
  }, [messages]);

  const clearMessages = () => {
    setMessages([]);
    sessionStorage.removeItem(STORAGE_KEY);
  };

  useEffect(() => {
    window.addEventListener('beforeunload', clearMessages);
    return () => {
      window.removeEventListener('beforeunload', clearMessages);
    };
  }, []);

  return { messages, setMessages, clearMessages };
}