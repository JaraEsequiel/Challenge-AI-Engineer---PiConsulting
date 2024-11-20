import { ThumbsUp, ThumbsDown } from 'lucide-react';

interface MessageReactionsProps {
  userReaction: boolean;
  onReact: (type: 'like' | 'dislike') => Promise<void>;
  isLoading: boolean;
}

export function MessageReactions({
  userReaction,
  onReact,
  isLoading,
}: MessageReactionsProps) {
  const getReactionButtonClass = (type: 'like' | 'dislike') => {
    const baseClass = "flex items-center space-x-1 px-3 py-1.5 rounded-full transition-all duration-200";
    const activeClass = type === 'like'
      ? "bg-green-100 text-green-700"
      : "bg-red-100 text-red-700";
    const inactiveClass = "hover:bg-gray-100 text-gray-600";

    return `${baseClass} ${userReaction ? activeClass : inactiveClass} ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
      }`;
  };

  return (
    <div className="flex space-x-2 mt-2">
      <button
        onClick={() => !isLoading && onReact('like')}
        disabled={isLoading}
        className={getReactionButtonClass('like')}
      >
        <ThumbsUp className="w-4 h-4" />
      </button>
    </div >
  );
}