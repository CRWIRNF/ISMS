import axios, { AxiosError } from 'axios'
import type { User, LoginRequest, Token, Requirement, Measure } from '@/types'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  login: async (credentials: LoginRequest): Promise<Token> => {
    const response = await api.post<Token>('/auth/login', credentials)
    return response.data
  },
}

// Users API
export const usersApi = {
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/users/me')
    return response.data
  },
  listUsers: async (): Promise<User[]> => {
    const response = await api.get<User[]>('/users/')
    return response.data
  },
}

// Requirements API
export const requirementsApi = {
  list: async (params?: {
    category?: string
    is_mandatory?: boolean
  }): Promise<Requirement[]> => {
    const response = await api.get<Requirement[]>('/requirements/', { params })
    return response.data
  },
  get: async (id: number): Promise<Requirement> => {
    const response = await api.get<Requirement>(`/requirements/${id}`)
    return response.data
  },
  getCategories: async (): Promise<string[]> => {
    const response = await api.get<string[]>('/requirements/categories')
    return response.data
  },
}

// Measures API
export const measuresApi = {
  list: async (params?: {
    requirement_id?: number
    status?: string
  }): Promise<Measure[]> => {
    const response = await api.get<Measure[]>('/measures/', { params })
    return response.data
  },
  get: async (id: number): Promise<Measure> => {
    const response = await api.get<Measure>(`/measures/${id}`)
    return response.data
  },
  myMeasures: async (): Promise<Measure[]> => {
    const response = await api.get<Measure[]>('/measures/my-measures')
    return response.data
  },
}

export default api
