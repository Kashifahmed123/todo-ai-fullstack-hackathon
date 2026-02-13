/**
 * Custom hook for task management with TanStack Query.
 *
 * Provides:
 * - Task list fetching with caching
 * - Task mutations (create, update, delete, toggle)
 * - Optimistic updates
 * - Automatic refetching
 */

"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Task } from "@/lib/types";

export function useTasks() {
  const queryClient = useQueryClient();

  // Fetch tasks
  const {
    data: tasks = [],
    isLoading,
    error,
  } = useQuery<Task[]>({
    queryKey: ["tasks"],
    queryFn: () => api.getTasks(),
  });

  // Create task mutation
  const createTask = useMutation({
    mutationFn: (data: { title: string; description?: string }) =>
      api.createTask(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });

  // Update task mutation
  const updateTask = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      api.updateTask(id, data),
    onMutate: async ({ id, data }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ["tasks"] });

      // Snapshot previous value
      const previousTasks = queryClient.getQueryData<Task[]>(["tasks"]);

      // Optimistically update
      queryClient.setQueryData<Task[]>(["tasks"], (old) =>
        old?.map((task) =>
          task.id === id ? { ...task, ...data } : task
        ) || []
      );

      return { previousTasks };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previousTasks) {
        queryClient.setQueryData(["tasks"], context.previousTasks);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });

  // Delete task mutation
  const deleteTask = useMutation({
    mutationFn: (id: number) => api.deleteTask(id),
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: ["tasks"] });

      const previousTasks = queryClient.getQueryData<Task[]>(["tasks"]);

      queryClient.setQueryData<Task[]>(["tasks"], (old) =>
        old?.filter((task) => task.id !== id) || []
      );

      return { previousTasks };
    },
    onError: (err, variables, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(["tasks"], context.previousTasks);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });

  // Toggle task mutation
  const toggleTask = useMutation({
    mutationFn: (id: number) => api.toggleTask(id),
    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: ["tasks"] });

      const previousTasks = queryClient.getQueryData<Task[]>(["tasks"]);

      queryClient.setQueryData<Task[]>(["tasks"], (old) =>
        old?.map((task) =>
          task.id === id ? { ...task, completed: !task.completed } : task
        ) || []
      );

      return { previousTasks };
    },
    onError: (err, variables, context) => {
      if (context?.previousTasks) {
        queryClient.setQueryData(["tasks"], context.previousTasks);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });

  return {
    tasks,
    isLoading,
    error,
    createTask,
    updateTask,
    deleteTask,
    toggleTask,
  };
}
