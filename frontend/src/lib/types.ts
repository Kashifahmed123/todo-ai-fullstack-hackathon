/**
 * TypeScript type definitions for API entities.
 */

export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface ErrorResponse {
  detail: string;
  type?: string;
  errors?: Array<{
    field: string;
    message: string;
  }>;
}
