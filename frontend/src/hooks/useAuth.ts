/**
 * Authentication hook for user registration, login, and logout.
 */

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api, setToken, removeToken } from "@/lib/api";

export function useAuth() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const register = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.register(email, password);
      setToken(response.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.login(email, password);
      setToken(response.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    removeToken();
    router.push("/login");
  };

  return {
    register,
    login,
    logout,
    isLoading,
    error,
  };
}
