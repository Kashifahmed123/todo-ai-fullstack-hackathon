"use client";

import { useState } from "react";
import type { Task } from "@/lib/types";
import TaskForm from "./TaskForm";

interface TaskItemProps {
  task: Task;
  onToggle: (id: number) => void;
  onUpdate: (id: number, data: any) => void;
  onDelete: (id: number) => void;
}

export default function TaskItem({
  task,
  onToggle,
  onUpdate,
  onDelete,
}: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);

  const handleUpdate = (data: { title: string; description?: string }) => {
    onUpdate(task.id, data);
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className="bg-gray-800/30 backdrop-blur-sm rounded-2xl shadow-lg p-6 border border-gray-700 animate-fade-in-up">
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-lg font-bold text-white">Edit Task</h4>
          <button
            onClick={() => setIsEditing(false)}
            className="text-gray-400 hover:text-gray-300 hover:rotate-90 transition-all duration-300"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <TaskForm
          initialData={task}
          onSubmit={handleUpdate}
          onCancel={() => setIsEditing(false)}
        />
      </div>
    );
  }

  return (
    <div className={`group bg-gray-800/30 backdrop-blur-sm rounded-2xl shadow-sm hover:shadow-xl border transition-all duration-300 relative overflow-hidden ${
      task.completed ? 'border-gray-700/50 bg-gray-800/20' : 'border-gray-700/50 hover:border-indigo-500/50 hover:-translate-y-1'
    }`}>
      {/* Gradient Overlay on Hover */}
      <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/0 via-purple-500/0 to-pink-500/0 group-hover:from-indigo-500/5 group-hover:via-purple-500/5 group-hover:to-pink-500/5 transition-all duration-500"></div>

      <div className="relative p-5">
        <div className="flex items-start gap-4">
          {/* Custom Checkbox */}
          <button
            onClick={() => onToggle(task.id)}
            className={`flex-shrink-0 mt-0.5 w-6 h-6 rounded-lg border-2 transition-all duration-300 ${
              task.completed
                ? 'bg-gradient-to-br from-green-500 to-green-600 border-green-500 shadow-lg shadow-green-500/50 scale-110'
                : 'border-gray-600 hover:border-indigo-500 hover:bg-indigo-900/30 hover:scale-110 hover:rotate-12'
            }`}
          >
            {task.completed && (
              <svg className="w-full h-full text-white p-0.5 animate-fade-in-up" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>

          {/* Task Content */}
          <div className="flex-1 min-w-0">
            <h3
              className={`text-lg font-semibold transition-all duration-300 ${
                task.completed
                  ? "line-through text-gray-500"
                  : "text-white group-hover:text-indigo-300"
              }`}
            >
              {task.title}
            </h3>
            {task.description && (
              <p
                className={`mt-1.5 text-sm leading-relaxed transition-all duration-300 ${
                  task.completed ? "text-gray-500" : "text-gray-400 group-hover:text-gray-300"
                }`}
              >
                {task.description}
              </p>
            )}
            <div className="mt-3 flex items-center space-x-4 text-xs text-gray-500">
              <span className="flex items-center space-x-1 group-hover:text-indigo-400 transition-colors">
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>{new Date(task.created_at).toLocaleDateString()}</span>
              </span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex-shrink-0 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all duration-300">
            <button
              onClick={() => setIsEditing(true)}
              className="p-2 text-gray-400 hover:text-indigo-400 hover:bg-indigo-900/30 rounded-lg transition-all duration-300 hover:scale-110 hover:rotate-12"
              title="Edit task"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button
              onClick={() => {
                if (confirm("Are you sure you want to delete this task?")) {
                  onDelete(task.id);
                }
              }}
              className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-900/30 rounded-lg transition-all duration-300 hover:scale-110 hover:rotate-12"
              title="Delete task"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
