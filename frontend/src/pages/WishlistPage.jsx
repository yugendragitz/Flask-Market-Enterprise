import { Link } from 'react-router-dom'
import { FiHeart, FiTrash2, FiShoppingCart } from 'react-icons/fi'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import useAuthStore from '../store/authStore'
import useCartStore from '../store/cartStore'
import { wishlistAPI } from '../services/api'
import toast from 'react-hot-toast'

const WishlistPage = () => {
  const { user, isAuthenticated } = useAuthStore()
  const addItem = useCartStore((state) => state.addItem)
  const queryClient = useQueryClient()

  // Fetch wishlist
  const { data: wishlistData, isLoading } = useQuery({
    queryKey: ['wishlist'],
    queryFn: async () => {
      const response = await wishlistAPI.getAll()
      return response.data.data?.wishlist || []
    },
    enabled: isAuthenticated,
  })

  // Remove from wishlist mutation
  const removeFromWishlistMutation = useMutation({
    mutationFn: (productId) => wishlistAPI.remove(productId),
    onSuccess: () => {
      queryClient.invalidateQueries(['wishlist'])
      toast.success('Removed from wishlist')
    },
    onError: () => {
      toast.error('Failed to remove from wishlist')
    },
  })

  // Handle add to cart
  const handleAddToCart = (product) => {
    addItem(product)
    toast.success('Added to cart!')
  }

  // Handle remove from wishlist
  const handleRemove = (productId) => {
    removeFromWishlistMutation.mutate(productId)
  }

  if (!user) {
    return (
      <div className="pt-32 pb-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Please login to view your wishlist</h1>
          <Link to="/login" className="btn btn-primary">Login</Link>
        </div>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="pt-32 pb-16">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-display font-bold text-gray-900 mb-8">My Wishlist</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="card p-4 animate-pulse">
                <div className="aspect-square bg-gray-200 rounded-lg mb-4" />
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
                <div className="h-4 bg-gray-200 rounded w-1/2" />
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  const wishlistItems = wishlistData || []

  return (
    <div className="pt-32 pb-16">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-display font-bold text-gray-900 mb-8">
          My Wishlist ({wishlistItems.length} items)
        </h1>
        
        {wishlistItems.length === 0 ? (
          <div className="card p-8 text-center">
            <FiHeart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Your wishlist is empty</h2>
            <p className="text-gray-500 mb-6">Save items you love to your wishlist and access them anytime.</p>
            <Link to="/products" className="btn btn-primary">Explore Products</Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {wishlistItems.map((item) => (
              <div key={item.id} className="card overflow-hidden group">
                <Link to={`/products/${item.product?.slug}`}>
                  <div className="aspect-square bg-gray-100 relative overflow-hidden">
                    <img
                      src={item.product?.thumbnail_url || 'https://via.placeholder.com/400'}
                      alt={item.product?.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    {item.product?.discount_percentage > 0 && (
                      <span className="absolute top-3 left-3 bg-danger-500 text-white text-xs font-bold px-2 py-1 rounded">
                        -{item.product.discount_percentage}%
                      </span>
                    )}
                  </div>
                </Link>
                <div className="p-4">
                  <Link to={`/products/${item.product?.slug}`}>
                    <h3 className="font-semibold text-gray-900 mb-1 hover:text-primary-600 transition-colors line-clamp-2">
                      {item.product?.name}
                    </h3>
                  </Link>
                  <p className="text-sm text-gray-500 mb-2">{item.product?.brand}</p>
                  <div className="flex items-baseline gap-2 mb-4">
                    <span className="text-lg font-bold text-gray-900">
                      ${item.product?.price?.toFixed(2)}
                    </span>
                    {item.product?.compare_price > item.product?.price && (
                      <span className="text-sm text-gray-400 line-through">
                        ${item.product?.compare_price?.toFixed(2)}
                      </span>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleAddToCart(item.product)}
                      className="flex-1 btn btn-primary btn-sm"
                    >
                      <FiShoppingCart className="w-4 h-4 mr-1" />
                      Add to Cart
                    </button>
                    <button
                      onClick={() => handleRemove(item.product?.id)}
                      disabled={removeFromWishlistMutation.isPending}
                      className="p-2 border border-gray-300 rounded-lg hover:bg-danger-50 hover:border-danger-300 hover:text-danger-500 transition-colors disabled:opacity-50"
                    >
                      <FiTrash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default WishlistPage
