// API client for backend communication with JWT authentication
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios'
import { authClient } from './auth-client'

// Create axios instance with base configuration
const api: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add JWT token to all requests
api.interceptors.request.use(
  async (config) => {
    try {
      // Get the current session from Better Auth
      // @ts-ignore
      const session = await authClient.getSession()

      // If session exists, add it to the Authorization header
      // Note: better-auth usually handles this via cookies, but if we need to pass a token manually:
      // This part depends on how better-auth exposes the token.
      // For now, let's assume cookie-based auth is primary, but if we have a token property:
      // @ts-ignore
      if (session?.data?.token) {
         // @ts-ignore
        config.headers.Authorization = `Bearer ${session.data.token}`
      }

      return config
    } catch (error) {
      console.error('Error adding auth token:', error)
      return config
    }
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - redirect to login
      if (typeof window !== 'undefined') {
        window.location.href = '/signin'
      }
    }
    return Promise.reject(error)
  }
)

export interface Task {
  id: number
  uuid: string
  title: string
  description: string | null
  completed: boolean
  user_id: string
  created_at: string
  updated_at: string
}

export interface TaskCreate {
  title: string
  description?: string
}

export interface TaskUpdate {
  title?: string
  description?: string
  completed?: boolean
}

export interface TaskListResponse {
  tasks: Task[]
  total: number
}

// Task API functions
export const taskAPI = {
  // List all tasks for the current user
  async list(userId: string, skip = 0, limit = 100): Promise<TaskListResponse> {
    const response = await api.get(`/api/${userId}/tasks`, {
      params: { skip, limit },
    })
    return response.data
  },

  // Create a new task
  async create(userId: string, data: TaskCreate): Promise<Task> {
    const response = await api.post(`/api/${userId}/tasks`, data)
    return response.data
  },

  // Get a specific task
  async get(userId: string, taskId: number): Promise<Task> {
    const response = await api.get(`/api/${userId}/tasks/${taskId}`)
    return response.data
  },

  // Update a task
  async update(userId: string, taskId: number, data: TaskUpdate): Promise<Task> {
    const response = await api.put(`/api/${userId}/tasks/${taskId}`, data)
    return response.data
  },

  // Delete a task
  async delete(userId: string, taskId: number): Promise<void> {
    await api.delete(`/api/${userId}/tasks/${taskId}`)
  },

  // Toggle task completion
  async toggleComplete(userId: string, taskId: number): Promise<Task> {
    const response = await api.patch(`/api/${userId}/tasks/${taskId}/complete`)
    return response.data
  },
}

export default api
