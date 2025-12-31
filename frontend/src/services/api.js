import axios from 'axios'

// API base URL - uses environment variable in production, proxy in development
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Get token from storage
    const authStorage = localStorage.getItem('auth-storage')
    if (authStorage) {
      const { state } = JSON.parse(authStorage)
      if (state?.accessToken) {
        config.headers.Authorization = `Bearer ${state.accessToken}`
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Handle 401 errors (unauthorized)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      // Try to refresh token
      const authStorage = localStorage.getItem('auth-storage')
      if (authStorage) {
        const { state } = JSON.parse(authStorage)
        if (state?.refreshToken) {
          try {
            const response = await axios.post('/api/v1/auth/refresh', {}, {
              headers: { Authorization: `Bearer ${state.refreshToken}` }
            })

            const { access_token } = response.data

            // Update token in storage
            const newState = {
              ...state,
              accessToken: access_token,
            }
            localStorage.setItem('auth-storage', JSON.stringify({ state: newState }))

            // Retry original request
            originalRequest.headers.Authorization = `Bearer ${access_token}`
            return api(originalRequest)
          } catch (refreshError) {
            // Refresh failed, clear auth
            localStorage.removeItem('auth-storage')
            window.location.href = '/login'
          }
        }
      }
    }

    return Promise.reject(error)
  }
)

export default api

// API endpoints helper functions
export const authAPI = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  logout: () => api.post('/auth/logout'),
  refresh: () => api.post('/auth/refresh'),
  me: () => api.get('/auth/me'),
}

export const productsAPI = {
  getAll: (params) => api.get('/products', { params }),
  getOne: (slug) => api.get(`/products/slug/${slug}`),
  getById: (id) => api.get(`/products/${id}`),
  getByCategory: (category, params) => api.get(`/products/category/${category}`, { params }),
  search: (query) => api.get('/products/search', { params: { q: query } }),
  getFeatured: () => api.get('/products/featured'),
  getReviews: (productId) => api.get(`/products/${productId}/reviews`),
  addReview: (productId, data) => api.post(`/products/${productId}/reviews`, data),
}

export const categoriesAPI = {
  getAll: () => api.get('/categories'),
  getOne: (slug) => api.get(`/categories/${slug}`),
}

export const cartAPI = {
  get: () => api.get('/cart'),
  addItem: (data) => api.post('/cart/items', data),
  updateItem: (productId, data) => api.put(`/cart/items/${productId}`, data),
  removeItem: (productId) => api.delete(`/cart/items/${productId}`),
  clear: () => api.delete('/cart'),
}

export const ordersAPI = {
  getAll: (params) => api.get('/orders', { params }),
  getOne: (id) => api.get(`/orders/${id}`),
  checkout: (data) => api.post('/orders/checkout', data),
  cancel: (id) => api.post(`/orders/${id}/cancel`),
  validateCoupon: (code) => api.post('/orders/validate-coupon', { code }),
}

export const usersAPI = {
  getProfile: () => api.get('/users/profile'),
  updateProfile: (data) => api.put('/users/profile', data),
  getWallet: () => api.get('/users/wallet'),
  addFunds: (amount) => api.post('/users/wallet/add', { amount }),
  getAddresses: () => api.get('/users/addresses'),
  addAddress: (data) => api.post('/users/addresses', data),
  updateAddress: (id, data) => api.put(`/users/addresses/${id}`, data),
  deleteAddress: (id) => api.delete(`/users/addresses/${id}`),
}

export const wishlistAPI = {
  getAll: () => api.get('/wishlist'),
  add: (productId) => api.post(`/wishlist/${productId}`),
  remove: (productId) => api.delete(`/wishlist/${productId}`),
}
