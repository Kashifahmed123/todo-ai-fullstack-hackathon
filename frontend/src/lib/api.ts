/**
 * API client for backend communication.
 *
 * Handles:
 * - JWT token management
 * - Request/response formatting
 * - Error handling
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Get JWT token from localStorage.
 */
function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

/**
 * Set JWT token in localStorage.
 */
export function setToken(token: string): void {
  localStorage.setItem("access_token", token);
}

/**
 * Remove JWT token from localStorage.
 */
export function removeToken(): void {
  localStorage.removeItem("access_token");
}

/**
 * Make authenticated API request.
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) {
      // Unauthorized - clear token and redirect to login
      removeToken();
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
    }

    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || "Request failed");
  }

  return response.json();
}

/**
 * API client methods.
 */
export const api = {
  // Authentication
  register: (email: string, password: string) =>
    apiRequest<{ access_token: string; token_type: string }>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  login: (email: string, password: string) =>
    apiRequest<{ access_token: string; token_type: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  getCurrentUser: () =>
    apiRequest<{ id: number; email: string; created_at: string }>("/auth/me"),

  // Tasks (to be implemented in Phase 4)
  getTasks: () => apiRequest<any[]>("/tasks"),
  createTask: (data: { title: string; description?: string }) =>
    apiRequest("/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  updateTask: (id: number, data: any) =>
    apiRequest(`/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  deleteTask: (id: number) =>
    apiRequest(`/tasks/${id}`, {
      method: "DELETE",
    }),
  toggleTask: (id: number) =>
    apiRequest(`/tasks/${id}/toggle`, {
      method: "POST",
    }),
};
