export interface Message {
  id: number;
  user_name: string;
  question: string;
  timestamp: Date;
  userReaction: boolean;
}

export interface ReactionPayload {
  question: string;
  answer: string;
}
