import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import api from '../services/api'
import toast from 'react-hot-toast'

const useCartStore = create(
  persist(
    (set, get) => ({
      items: [],
      isLoading: false,
      isSyncing: false,

      // Add item to cart
      addItem: async (product, quantity = 1) => {
        const { items, isAuthenticated } = get()
        
        // Check if item already exists
        const existingIndex = items.findIndex(item => item.product_id === product.id)
        
        let newItems
        if (existingIndex >= 0) {
          // Update quantity
          newItems = items.map((item, index) =>
            index === existingIndex
              ? { ...item, quantity: item.quantity + quantity }
              : item
          )
        } else {
          // Add new item
          newItems = [...items, {
            product_id: product.id,
            product,
            quantity,
            price: product.price,
          }]
        }
        
        set({ items: newItems })
        toast.success(`${product.name} added to cart!`)

        // Sync with server if authenticated
        if (isAuthenticated()) {
          try {
            await api.post('/cart/items', {
              product_id: product.id,
              quantity,
            })
          } catch (error) {
            console.error('Failed to sync cart:', error)
          }
        }
      },

      // Update item quantity
      updateQuantity: async (productId, quantity) => {
        const { items, isAuthenticated } = get()
        
        if (quantity <= 0) {
          get().removeItem(productId)
          return
        }

        const newItems = items.map(item =>
          item.product_id === productId
            ? { ...item, quantity }
            : item
        )
        
        set({ items: newItems })

        if (isAuthenticated()) {
          try {
            await api.put(`/cart/items/${productId}`, { quantity })
          } catch (error) {
            console.error('Failed to update cart:', error)
          }
        }
      },

      // Remove item from cart
      removeItem: async (productId) => {
        const { items, isAuthenticated } = get()
        const item = items.find(i => i.product_id === productId)
        
        const newItems = items.filter(item => item.product_id !== productId)
        set({ items: newItems })
        
        if (item) {
          toast.success(`${item.product.name} removed from cart`)
        }

        if (isAuthenticated()) {
          try {
            await api.delete(`/cart/items/${productId}`)
          } catch (error) {
            console.error('Failed to remove from cart:', error)
          }
        }
      },

      // Clear cart
      clearCart: async () => {
        const { isAuthenticated } = get()
        set({ items: [] })

        if (isAuthenticated()) {
          try {
            await api.delete('/cart')
          } catch (error) {
            console.error('Failed to clear cart:', error)
          }
        }
      },

      // Sync cart with server
      syncCart: async () => {
        set({ isSyncing: true })
        try {
          const response = await api.get('/cart')
          const serverItems = response.data.items.map(item => ({
            product_id: item.product_id,
            product: item.product,
            quantity: item.quantity,
            price: item.product.price,
          }))
          set({ items: serverItems, isSyncing: false })
        } catch (error) {
          console.error('Failed to sync cart:', error)
          set({ isSyncing: false })
        }
      },

      // Check if user is authenticated (helper)
      isAuthenticated: () => {
        const authStorage = localStorage.getItem('auth-storage')
        if (authStorage) {
          const { state } = JSON.parse(authStorage)
          return state?.isAuthenticated || false
        }
        return false
      },

      // Get cart totals
      getCartTotals: () => {
        const { items } = get()
        const subtotal = items.reduce(
          (sum, item) => sum + (item.price * item.quantity),
          0
        )
        const itemCount = items.reduce((sum, item) => sum + item.quantity, 0)
        
        return {
          subtotal,
          itemCount,
          shipping: subtotal > 100 ? 0 : 9.99,
          tax: subtotal * 0.08,
          total: subtotal + (subtotal > 100 ? 0 : 9.99) + (subtotal * 0.08),
        }
      },

      // Get item count
      getItemCount: () => {
        const { items } = get()
        return items.reduce((sum, item) => sum + item.quantity, 0)
      },
    }),
    {
      name: 'cart-storage',
      partialize: (state) => ({
        items: state.items,
      }),
    }
  )
)

export default useCartStore
