"use client"

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth-context'
import { AuthGuard } from '@/lib/auth-guard'
import { taskAPI, Task, TaskCreate } from '@/lib/api'
import { Plus, Check, X, Edit2, Trash2, Loader2, Mic, MicOff, Languages } from 'lucide-react'
import { useVoice } from '@/hooks/use-voice'
import { useLanguage } from '@/lib/language-context'

function DashboardContent() {
  const router = useRouter()
  const { user, signOut } = useAuth()
  const { t, language, setLanguage, dir } = useLanguage()

  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [newTaskTitle, setNewTaskTitle] = useState('')
  const [newTaskDescription, setNewTaskDescription] = useState('')
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [editTitle, setEditTitle] = useState('')
  const [editDescription, setEditDescription] = useState('')

  // Voice command handler
  const handleVoiceCommand = (command: string) => {
    const lowerCommand = command.toLowerCase()

    if (lowerCommand.startsWith('add task') || lowerCommand.startsWith('new task')) {
      const title = command.substring(9).trim()
      const cleanTitle = command.replace(/^(add|new) task /i, '').trim()
      if (cleanTitle) {
        setNewTaskTitle(cleanTitle)
      }
    } else if (lowerCommand.includes('sign out') || lowerCommand.includes('logout')) {
      handleSignOut()
    }
  }

  const { isListening, isSupported, startListening, stopListening, transcript } = useVoice({
    onCommand: handleVoiceCommand,
    lang: language === 'ur' ? 'ur-PK' : 'en-US'
  })

  // Fetch tasks on mount
  useEffect(() => {
    if (user) {
      loadTasks()
    }
  }, [user])

  const loadTasks = async () => {
    if (!user) return
    setLoading(true)
    try {
      const userId = user.id || user.email || 'default-user' // Fallback for user ID
      const response = await taskAPI.list(userId)
      setTasks(response.tasks)
    } catch (error) {
      console.error('Failed to load tasks:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!user || !newTaskTitle.trim()) return

    try {
      const userId = user.id || user.email || 'default-user'
      const newTask: TaskCreate = {
        title: newTaskTitle,
        description: newTaskDescription || undefined,
      }
      await taskAPI.create(userId, newTask)
      setNewTaskTitle('')
      setNewTaskDescription('')
      await loadTasks()
    } catch (error) {
      console.error('Failed to create task:', error)
      alert('Failed to create task. Please try again.')
    }
  }

  const handleToggleComplete = async (task: Task) => {
    if (!user) return
    try {
      const userId = user.id || user.email || 'default-user'
      await taskAPI.toggleComplete(userId, task.id)
      await loadTasks()
    } catch (error) {
      console.error('Failed to toggle task:', error)
      alert('Failed to update task. Please try again.')
    }
  }

  const handleDeleteTask = async (taskId: number) => {
    if (!user) return
    if (!confirm(t('confirmDelete'))) return

    try {
      const userId = user.id || user.email || 'default-user'
      await taskAPI.delete(userId, taskId)
      await loadTasks()
    } catch (error) {
      console.error('Failed to delete task:', error)
      alert('Failed to delete task. Please try again.')
    }
  }

  const startEditing = (task: Task) => {
    setEditingTask(task)
    setEditTitle(task.title)
    setEditDescription(task.description || '')
  }

  const saveEdit = async () => {
    if (!user || !editingTask || !editTitle.trim()) return

    try {
      const userId = user.id || user.email || 'default-user'
      await taskAPI.update(userId, editingTask.id, {
        title: editTitle,
        description: editDescription || undefined,
      })
      setEditingTask(null)
      await loadTasks()
    } catch (error) {
      console.error('Failed to update task:', error)
      alert('Failed to update task. Please try again.')
    }
  }

  const handleSignOut = async () => {
    try {
      await signOut()
      router.push('/')
    } catch (error) {
      console.error('Failed to sign out:', error)
    }
  }

  if (!user) {
    return (
      <AuthGuard>
        <div>{t('loading')}</div>
      </AuthGuard>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50" dir={dir}>
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-2xl font-bold text-gray-900">{t('title')}</h1>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setLanguage(language === 'en' ? 'ur' : 'en')}
                className="p-2 text-gray-600 hover:text-blue-600 rounded-full hover:bg-gray-100"
                title="Switch Language"
              >
                <Languages className="h-5 w-5" />
              </button>
              <span className="text-sm text-gray-600">
                {user?.email || 'User'}
              </span>
              <button
                onClick={handleSignOut}
                className="bg-red-600 text-white px-4 py-2 rounded-md text-sm hover:bg-red-700"
              >
                {t('signOut')}
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Add New Task Form */}
        <div className="bg-white rounded-lg shadow mb-8 p-6">
          <h2 className="text-lg font-semibold mb-4">{t('addNewTask')}</h2>
          <form onSubmit={handleAddTask} className="space-y-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                {t('taskTitle')} *
              </label>
              <div className="mt-1 flex rounded-md shadow-sm">
                <input
                  type="text"
                  id="title"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  className={`flex-1 block w-full px-3 py-2 border border-gray-300 ${language === 'ur' ? 'rounded-r-md' : 'rounded-l-md'} focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm`}
                  placeholder={t('enterTitle')}
                  required
                />
                {isSupported && (
                  <button
                    type="button"
                    onClick={isListening ? stopListening : startListening}
                    className={`inline-flex items-center px-3 ${language === 'ur' ? 'rounded-l-md border-r-0 border-l' : 'rounded-r-md border-l-0 border-r'} border-gray-300 bg-gray-50 text-gray-500 sm:text-sm ${
                      isListening ? 'bg-red-50 text-red-600 border-red-300' : 'hover:bg-gray-100'
                    }`}
                    title="Voice Command"
                  >
                    {isListening ? (
                      <MicOff className="h-5 w-5" />
                    ) : (
                      <Mic className="h-5 w-5" />
                    )}
                  </button>
                )}
              </div>
              {isListening && (
                <p className="mt-1 text-xs text-blue-600 animate-pulse">
                  {t('voiceListening')}
                </p>
              )}
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                {t('taskDescription')}
              </label>
              <textarea
                id="description"
                value={newTaskDescription}
                onChange={(e) => setNewTaskDescription(e.target.value)}
                rows={3}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder={t('enterDescription')}
              />
            </div>
            <button
              type="submit"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <Plus className={`h-4 w-4 ${language === 'ur' ? 'ml-2' : 'mr-2'}`} />
              {t('addTask')}
            </button>
          </form>
        </div>

        {/* Tasks List */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold">{t('myTasks')}</h2>
          </div>

          {loading ? (
            <div className="p-12 text-center">
              <Loader2 className="mx-auto h-8 w-8 animate-spin text-blue-600" />
              <p className="mt-2 text-gray-600">{t('loading')}</p>
            </div>
          ) : tasks.length === 0 ? (
            <div className="p-12 text-center text-gray-500">
              <p>{t('noTasks')}</p>
            </div>
          ) : (
            <ul className="divide-y divide-gray-200">
              {tasks.map((task) => (
                <li key={task.id} className="p-6 hover:bg-gray-50">
                  {editingTask?.id === task.id ? (
                    // Edit Mode
                    <div className="space-y-4">
                      <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                        autoFocus
                      />
                      <textarea
                        value={editDescription}
                        onChange={(e) => setEditDescription(e.target.value)}
                        rows={2}
                        className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                      <div className="flex space-x-2">
                        <button
                          onClick={saveEdit}
                          className="px-3 py-1 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700"
                        >
                          {t('save')}
                        </button>
                        <button
                          onClick={() => setEditingTask(null)}
                          className="px-3 py-1 bg-gray-300 text-gray-700 text-sm rounded-md hover:bg-gray-400"
                        >
                          {t('cancel')}
                        </button>
                      </div>
                    </div>
                  ) : (
                    // View Mode
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-3">
                        <div className="mt-1 flex-shrink-0">
                          <button
                            onClick={() => handleToggleComplete(task)}
                            className={`flex h-5 w-5 border-2 rounded items-center justify-center ${
                              task.completed
                                ? 'bg-green-600 border-green-600'
                                : 'border-gray-300 hover:border-gray-400'
                            }`}
                          >
                            {task.completed && <Check className="h-3 w-3 text-white" />}
                          </button>
                        </div>
                        <div className="flex-1">
                          <h3
                            className={`text-lg font-medium ${
                              task.completed ? 'text-gray-500 line-through' : 'text-gray-900'
                            }`}
                          >
                            {task.title}
                          </h3>
                          {task.description && (
                            <p className="mt-1 text-sm text-gray-600">{task.description}</p>
                          )}
                          <p className="mt-2 text-xs text-gray-400">
                            {t('created')} {new Date(task.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => startEditing(task)}
                          className="text-blue-600 hover:text-blue-800"
                        >
                          <Edit2 className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteTask(task.id)}
                          className="text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>
    </div>
  )
}

export default function DashboardPage() {
  return (
    <AuthGuard>
      <DashboardContent />
    </AuthGuard>
  )
}
