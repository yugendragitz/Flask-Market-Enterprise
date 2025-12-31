import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import api from '../services/api'

const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Login action
      login: async (email, password) => {
        set({ isLoading: true, error: null })
        try {
          const response = await api.post('/auth/login', { username: email, password })
          const { user, access_token, refresh_token } = response.data.data

          set({
            user,
            accessToken: access_token,
            refreshToken: refresh_token,
            isAuthenticated: true,
            isLoading: false,
          })

          // Set token in API instance
          api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

          return { success: true }
        } catch (error) {
          const message = error.response?.data?.message || 'Login failed'
          set({ error: message, isLoading: false })
          return { success: false, error: message }
        }
      },

      // Register action
      register: async (userData) => {
        set({ isLoading: true, error: null })
        try {
          const response = await api.post('/auth/register', userData)
          const { user, access_token, refresh_token } = response.data.data

          set({
            user,
            accessToken: access_token,
            refreshToken: refresh_token,
            isAuthenticated: true,
            isLoading: false,
          })

          api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

          return { success: true }
        } catch (error) {
          const message = error.response?.data?.message || 'Registration failed'
          set({ error: message, isLoading: false })
          return { success: false, error: message }
        }
      },

      // Logout action
      logout: async () => {
        try {
          await api.post('/auth/logout')
        } catch (error) {
          console.error('Logout error:', error)
        } finally {
          set({
            user: null,
            accessToken: null,
            refreshToken: null,
            isAuthenticated: false,
          })
          delete api.defaults.headers.common['Authorization']
        }
      },

      // Refresh token
      refreshAccessToken: async () => {
        const { refreshToken } = get()
        if (!refreshToken) return false

        try {
          const response = await api.post('/auth/refresh', {}, {
            headers: { Authorization: `Bearer ${refreshToken}` }
          })
          
          const { access_token } = response.data
          set({ accessToken: access_token })
          api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
          
          return true
        } catch (error) {
          get().logout()
          return false
        }
      },

      // Update user profile
      updateProfile: async (userData) => {
        set({ isLoading: true, error: null })
        try {
          const response = await api.put('/users/profile', userData)
          set({ user: response.data.user, isLoading: false })
          return { success: true }
        } catch (error) {
          const message = error.response?.data?.message || 'Update failed'
          set({ error: message, isLoading: false })
          return { success: false, error: message }
        }
      },

      // Clear error
      clearError: () => set({ error: null }),

      // Check if token exists on app load
      initAuth: () => {
        const { accessToken } = get()
        if (accessToken) {
          api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

export default useAuthStore
