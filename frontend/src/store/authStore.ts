import { create } from 'zustand'
import type { User, LoginRequest } from '@/types'
import { authApi, usersApi } from '@/services/api'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  login: (credentials: LoginRequest) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (credentials: LoginRequest) => {
    set({ isLoading: true, error: null })
    try {
      const tokenData = await authApi.login(credentials)
      localStorage.setItem('access_token', tokenData.access_token)

      // Fetch user info
      const user = await usersApi.getCurrentUser()
      set({ user, isAuthenticated: true, isLoading: false })
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Login fehlgeschlagen'
      set({ error: errorMessage, isLoading: false })
      throw error
    }
  },

  logout: () => {
    localStorage.removeItem('access_token')
    set({ user: null, isAuthenticated: false, error: null })
  },

  checkAuth: async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      set({ isAuthenticated: false, user: null })
      return
    }

    set({ isLoading: true })
    try {
      const user = await usersApi.getCurrentUser()
      set({ user, isAuthenticated: true, isLoading: false })
    } catch (error) {
      localStorage.removeItem('access_token')
      set({ user: null, isAuthenticated: false, isLoading: false })
    }
  },
}))
