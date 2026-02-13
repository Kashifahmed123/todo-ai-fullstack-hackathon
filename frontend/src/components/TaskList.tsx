"use client";

import type { Task } from "@/lib/types";
import TaskItem from "./TaskItem";

interface TaskListProps {
  tasks: Task[];
  isLoading: boolean;
  onToggle: (id: number) => void;
  onUpdate: (id: number, data: any) => void;
  onDelete: (id: number) => void;
}

export default function TaskList({
  tasks,
  isLoading,
  onToggle,
  onUpdate,
  onDelete,
}: TaskListProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-16">
        <div className="text-center">
          <div className="relative inline-block">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-solid border-indigo-500 border-r-transparent"></div>
            <div className="absolute inset-0 h-12 w-12 animate-spin rounded-full border-4 border-solid border-purple-500 border-l-transparent animation-delay-1000"></div>
          </div>
          <p className="mt-4 text-sm font-medium text-gray-400 animate-pulse">Loading your tasks...</p>
        </div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="bg-gray-800/30 backdrop-blur-sm rounded-2xl shadow-lg border border-gray-700/50 p-12 text-center animate-fade-in-up relative overflow-hidden">
        {/* Decorative Elements */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-32 h-32 bg-purple-500/10 rounded-full blur-3xl"></div>

        <div className="relative">
          <div className="w-20 h-20 bg-gradient-to-br from-indigo-900/50 to-purple-900/50 rounded-full flex items-center justify-center mx-auto mb-4 border border-indigo-500/30 shadow-lg shadow-indigo-500/20 animate-float">
            <svg className="w-10 h-10 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-white mb-2">
            No tasks yet
          </h3>
          <p className="text-gray-400 max-w-sm mx-auto">
            Start your productivity journey by creating your first task above!
          </p>
        </div>
      </div>
    );
  }

  const completedTasks = tasks.filter((t) => t.completed);
  const incompleteTasks = tasks.filter((t) => !t.completed);

  return (
    <div className="space-y-6">
      {/* Task Statistics */}
      <div className="bg-gray-800/30 backdrop-blur-sm rounded-xl shadow-sm border border-gray-700/50 p-4 relative overflow-hidden group hover:border-indigo-500/30 transition-all duration-300">
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/0 via-purple-500/0 to-pink-500/0 group-hover:from-indigo-500/5 group-hover:via-purple-500/5 group-hover:to-pink-500/5 transition-all duration-500"></div>

        <div className="relative flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2 group/item">
              <div className="w-3 h-3 bg-blue-500 rounded-full shadow-lg shadow-blue-500/50 group-hover/item:scale-125 transition-transform"></div>
              <span className="text-sm font-medium text-gray-300 group-hover/item:text-blue-400 transition-colors">
                {incompleteTasks.length} Active
              </span>
            </div>
            <div className="flex items-center space-x-2 group/item">
              <div className="w-3 h-3 bg-green-500 rounded-full shadow-lg shadow-green-500/50 group-hover/item:scale-125 transition-transform"></div>
              <span className="text-sm font-medium text-gray-300 group-hover/item:text-green-400 transition-colors">
                {completedTasks.length} Completed
              </span>
            </div>
          </div>
          <div className="text-sm font-semibold text-white bg-gradient-to-r from-indigo-500 to-purple-500 bg-clip-text text-transparent">
            {tasks.length} Total
          </div>
        </div>
      </div>

      {/* Active Tasks */}
      {incompleteTasks.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center space-x-2 group">
            <div className="w-1 h-6 bg-gradient-to-b from-blue-500 to-blue-600 rounded-full shadow-lg shadow-blue-500/50 group-hover:h-8 transition-all duration-300"></div>
            <h3 className="text-sm font-bold text-white uppercase tracking-wide group-hover:text-blue-400 transition-colors">
              Active Tasks
            </h3>
            <div className="flex-1 h-px bg-gradient-to-r from-blue-500/50 to-transparent"></div>
          </div>
          <div className="space-y-3">
            {incompleteTasks.map((task, index) => (
              <div
                key={task.id}
                className="animate-fade-in-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <TaskItem
                  task={task}
                  onToggle={onToggle}
                  onUpdate={onUpdate}
                  onDelete={onDelete}
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Completed Tasks */}
      {completedTasks.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center space-x-2 group">
            <div className="w-1 h-6 bg-gradient-to-b from-green-500 to-green-600 rounded-full shadow-lg shadow-green-500/50 group-hover:h-8 transition-all duration-300"></div>
            <h3 className="text-sm font-bold text-white uppercase tracking-wide group-hover:text-green-400 transition-colors">
              Completed Tasks
            </h3>
            <div className="flex-1 h-px bg-gradient-to-r from-green-500/50 to-transparent"></div>
          </div>
          <div className="space-y-3">
            {completedTasks.map((task, index) => (
              <div
                key={task.id}
                className="animate-fade-in-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <TaskItem
                  task={task}
                  onToggle={onToggle}
                  onUpdate={onUpdate}
                  onDelete={onDelete}
                />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
