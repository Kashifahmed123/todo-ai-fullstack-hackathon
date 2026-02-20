/**
 * Chat API client for backend communication.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

export interface ChatResponse {
  response: string;
  conversation_id: number;
}

export const chatApi = {
  sendMessage: async (
    message: string,
    conversationId?: number
  ): Promise<ChatResponse> => {
    const token = getToken();
    if (!token) {
      throw new Error("Not authenticated");
    }

    const response = await fetch(`${API_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Request failed" }));
      throw new Error(error.detail || "Failed to send message");
    }

    return response.json();
  },
};
