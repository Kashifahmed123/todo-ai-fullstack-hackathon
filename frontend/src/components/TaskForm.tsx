"use client";

import { useState } from "react";
import type { Task } from "@/lib/types";

interface TaskFormProps {
  onSubmit: (data: { title: string; description?: string }) => void;
  onCancel?: () => void;
  initialData?: Task;
  isLoading?: boolean;
}

export default function TaskForm({
  onSubmit,
  onCancel,
  initialData,
  isLoading,
}: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || "");
  const [description, setDescription] = useState(
    initialData?.description || ""
  );
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!title.trim()) {
      setError("Title is required");
      return;
    }

    onSubmit({
      title: title.trim(),
      description: description.trim() || undefined,
    });

    // Reset form if creating new task
    if (!initialData) {
      setTitle("");
      setDescription("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {error && (
        <div className="rounded-xl bg-red-900/50 p-4 border border-red-500/50 animate-fade-in-up backdrop-blur-sm">
          <div className="flex">
            <svg className="h-5 w-5 text-red-400 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="ml-3 text-sm text-red-300 font-medium">{error}</p>
          </div>
        </div>
      )}

      <div className="group">
        <label
          htmlFor="title"
          className="block text-sm font-medium text-gray-300 mb-2 group-focus-within:text-indigo-400 transition-colors"
        >
          Title *
        </label>
        <div className="relative">
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="appearance-none block w-full px-4 py-3 border border-gray-600 bg-gray-900/50 rounded-xl shadow-sm placeholder-gray-500 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all hover:border-gray-500"
            placeholder="Enter task title"
            maxLength={200}
            required
          />
          <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-indigo-500/0 to-purple-500/0 group-focus-within:from-indigo-500/10 group-focus-within:to-purple-500/10 pointer-events-none transition-all duration-300"></div>
        </div>
      </div>

      <div className="group">
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-300 mb-2 group-focus-within:text-indigo-400 transition-colors"
        >
          Description (optional)
        </label>
        <div className="relative">
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="appearance-none block w-full px-4 py-3 border border-gray-600 bg-gray-900/50 rounded-xl shadow-sm placeholder-gray-500 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none hover:border-gray-500"
            placeholder="Enter task description"
            maxLength={5000}
          />
          <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-indigo-500/0 to-purple-500/0 group-focus-within:from-indigo-500/10 group-focus-within:to-purple-500/10 pointer-events-none transition-all duration-300"></div>
        </div>
      </div>

      <div className="flex gap-3 pt-2">
        <button
          type="submit"
          disabled={isLoading}
          className="group flex-1 flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-semibold text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:shadow-lg hover:shadow-indigo-500/50 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 transition-all duration-200 relative overflow-hidden"
        >
          <span className="relative z-10">
            {isLoading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Saving...
              </span>
            ) : (
              initialData ? "Update Task" : "Add Task"
            )}
          </span>
          <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-6 py-3 border-2 border-gray-700 rounded-xl shadow-sm text-sm font-semibold text-gray-300 bg-gray-900/50 hover:bg-gray-800/50 hover:border-gray-600 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
