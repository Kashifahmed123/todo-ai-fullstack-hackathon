"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useTasks } from "@/hooks/useTasks";
import TaskForm from "@/components/TaskForm";
import TaskList from "@/components/TaskList";

export default function DashboardPage() {
  const router = useRouter();
  const [showForm, setShowForm] = useState(false);
  const { tasks, isLoading, createTask, updateTask, deleteTask, toggleTask } =
    useTasks();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/login");
    }
  }, [router]);

  const handleCreateTask = (data: { title: string; description?: string }) => {
    createTask.mutate(data, {
      onSuccess: () => {
        setShowForm(false);
      },
    });
  };

  const handleUpdateTask = (id: number, data: any) => {
    updateTask.mutate({ id, data });
  };

  const handleDeleteTask = (id: number) => {
    deleteTask.mutate(id);
  };

  const handleToggleTask = (id: number) => {
    toggleTask.mutate(id);
  };

  return (
    <div className="min-h-screen bg-gray-900 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Gradient Orbs */}
        <div className="absolute top-0 -left-4 w-96 h-96 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-0 -right-4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>

        {/* Grid Pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#4f4f4f12_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f12_1px,transparent_1px)] bg-[size:4rem_4rem]"></div>

        {/* Floating Particles */}
        <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-indigo-400 rounded-full animate-float"></div>
        <div className="absolute top-1/3 right-1/4 w-3 h-3 bg-purple-400 rounded-full animate-float animation-delay-1000"></div>
        <div className="absolute bottom-1/4 left-1/3 w-2 h-2 bg-pink-400 rounded-full animate-float animation-delay-2000"></div>
        <div className="absolute top-2/3 right-1/3 w-2 h-2 bg-blue-400 rounded-full animate-float animation-delay-3000"></div>
      </div>

      {/* Navigation */}
      <nav className="border-b border-gray-700/50 bg-gray-900/80 backdrop-blur-md sticky top-0 z-50 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-500/50">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                  TaskFlow
                </h1>
                <p className="text-xs text-gray-400">Dashboard</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="hidden sm:flex items-center space-x-2 px-3 py-1.5 bg-indigo-900/30 border border-indigo-500/30 rounded-lg backdrop-blur-sm">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-gray-300">
                  {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
                </span>
              </div>
              <button
                onClick={() => {
                  localStorage.removeItem("access_token");
                  router.push("/login");
                }}
                className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-800/50 rounded-lg transition-colors backdrop-blur-sm"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="relative max-w-5xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8 animate-fade-in-up">
          <h2 className="text-3xl font-bold text-white mb-2">
            My Tasks
          </h2>
          <p className="text-gray-400">
            Organize and track your daily tasks efficiently
          </p>
        </div>

        {/* Add Task Section */}
        <div className="mb-6 animate-fade-in-up animation-delay-200">
          {!showForm ? (
            <button
              onClick={() => setShowForm(true)}
              className="w-full group relative overflow-hidden px-6 py-4 bg-gray-800/30 backdrop-blur-sm border-2 border-dashed border-gray-700 rounded-2xl hover:border-indigo-500 hover:bg-gray-800/50 transition-all duration-200"
            >
              <div className="flex items-center justify-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center group-hover:scale-110 group-hover:rotate-6 transition-transform duration-300 shadow-lg shadow-indigo-500/50">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                </div>
                <span className="text-lg font-semibold text-gray-300 group-hover:text-indigo-400 transition-colors">
                  Add New Task
                </span>
              </div>
            </button>
          ) : (
            <div className="bg-gray-800/30 backdrop-blur-sm rounded-2xl shadow-xl p-6 border border-gray-700">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-white">
                  Create New Task
                </h3>
                <button
                  onClick={() => setShowForm(false)}
                  className="text-gray-400 hover:text-gray-300 transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <TaskForm
                onSubmit={handleCreateTask}
                onCancel={() => setShowForm(false)}
                isLoading={createTask.isPending}
              />
            </div>
          )}
        </div>

        {/* Task List */}
        <div className="animate-fade-in-up animation-delay-400">
          <TaskList
            tasks={tasks}
            isLoading={isLoading}
            onToggle={handleToggleTask}
            onUpdate={handleUpdateTask}
            onDelete={handleDeleteTask}
          />
        </div>
      </main>
    </div>
  );
}
