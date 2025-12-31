import { Link, useNavigate } from 'react-router-dom'
import { FiHeart, FiShoppingCart, FiStar } from 'react-icons/fi'
import { useRef, useEffect } from 'react'
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query'
import gsap from 'gsap'
import clsx from 'clsx'
import useCartStore from '../store/cartStore'
import useAuthStore from '../store/authStore'
import { wishlistAPI } from '../services/api'
import toast from 'react-hot-toast'

const ProductCard = ({ product, index = 0 }) => {
  const cardRef = useRef(null)
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const addItem = useCartStore((state) => state.addItem)
  const { isAuthenticated } = useAuthStore()

  // Fetch wishlist
  const { data: wishlistData } = useQuery({
    queryKey: ['wishlist'],
    queryFn: async () => {
      const response = await wishlistAPI.getAll()
      return response.data.data?.wishlist || []
    },
    enabled: isAuthenticated,
  })

  // Check if product is in wishlist
  const isInWishlist = wishlistData?.some(item => item.product?.id === product?.id)

  // Add to wishlist mutation
  const addToWishlistMutation = useMutation({
    mutationFn: (productId) => wishlistAPI.add(productId),
    onSuccess: () => {
      queryClient.invalidateQueries(['wishlist'])
      toast.success('Added to wishlist!')
    },
    onError: (error) => {
      if (error.response?.status === 401) {
        toast.error('Please login to add items to wishlist')
        navigate('/login')
      } else if (error.response?.status === 400) {
        toast.error('Already in wishlist')
      } else {
        toast.error('Failed to add to wishlist')
      }
    },
  })

  // Remove from wishlist mutation
  const removeFromWishlistMutation = useMutation({
    mutationFn: (productId) => wishlistAPI.remove(productId),
    onSuccess: () => {
      queryClient.invalidateQueries(['wishlist'])
      toast.success('Removed from wishlist')
    },
    onError: (error) => {
      if (error.response?.status === 401) {
        toast.error('Please login first')
        navigate('/login')
      } else {
        toast.error('Failed to remove from wishlist')
      }
    },
  })

  // GSAP animation on mount
  useEffect(() => {
    gsap.fromTo(
      cardRef.current,
      { opacity: 0, y: 50 },
      {
        opacity: 1,
        y: 0,
        duration: 0.6,
        delay: index * 0.1,
        ease: 'power3.out',
      }
    )
  }, [index])

  // Handle add to cart
  const handleAddToCart = (e) => {
    e.preventDefault()
    e.stopPropagation()
    addItem(product)
  }

  // Handle wishlist
  const handleWishlist = (e) => {
    e.preventDefault()
    e.stopPropagation()
    
    if (!isAuthenticated) {
      toast.error('Please login to add items to wishlist')
      navigate('/login')
      return
    }
    
    if (isInWishlist) {
      removeFromWishlistMutation.mutate(product.id)
    } else {
      addToWishlistMutation.mutate(product.id)
    }
  }

  // Calculate discount percentage
  const discountPercentage = product.compare_price
    ? Math.round(((product.compare_price - product.price) / product.compare_price) * 100)
    : 0

  // Get primary image - use thumbnail_url from API
  const primaryImage = product.thumbnail_url || product.images?.[0]?.image_url || product.image_url || 'https://picsum.photos/400/400'

  return (
    <div
      ref={cardRef}
      className="product-card group"
    >
      <Link to={`/products/${product.slug || product.id}`}>
        {/* Image container */}
        <div className="product-card-image">
          <img
            src={primaryImage}
            alt={product.name}
            loading="lazy"
          />
          
          {/* Badges */}
          <div className="absolute top-3 left-3 flex flex-col gap-2">
            {discountPercentage > 0 && (
              <span className="bg-danger-500 text-white text-xs font-bold px-2 py-1 rounded">
                -{discountPercentage}%
              </span>
            )}
            {product.featured && (
              <span className="bg-accent-500 text-white text-xs font-bold px-2 py-1 rounded">
                Featured
              </span>
            )}
            {product.stock <= 5 && product.stock > 0 && (
              <span className="bg-warning-500 text-white text-xs font-bold px-2 py-1 rounded">
                Low Stock
              </span>
            )}
            {product.stock === 0 && (
              <span className="bg-gray-500 text-white text-xs font-bold px-2 py-1 rounded">
                Out of Stock
              </span>
            )}
          </div>

          {/* Quick actions */}
          <div className="absolute top-3 right-3 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-x-4 group-hover:translate-x-0">
            <button
              onClick={handleWishlist}
              disabled={addToWishlistMutation.isPending || removeFromWishlistMutation.isPending}
              className={clsx(
                "w-9 h-9 rounded-full shadow-md flex items-center justify-center transition-colors disabled:opacity-50",
                isInWishlist
                  ? "bg-danger-50 text-danger-500"
                  : "bg-white hover:bg-danger-50 hover:text-danger-500"
              )}
            >
              <FiHeart className={clsx("w-4 h-4", isInWishlist && "fill-current")} />
            </button>
          </div>

          {/* Add to cart button */}
          <div className="absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-4 group-hover:translate-y-0">
            <button
              onClick={handleAddToCart}
              disabled={product.stock === 0}
              className={clsx(
                'w-full py-2.5 rounded-lg font-medium flex items-center justify-center gap-2 transition-colors',
                product.stock > 0
                  ? 'bg-white text-gray-900 hover:bg-primary-600 hover:text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              )}
            >
              <FiShoppingCart className="w-4 h-4" />
              {product.stock > 0 ? 'Add to Cart' : 'Out of Stock'}
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-4">
          {/* Category */}
          {product.category && (
            <p className="text-xs text-primary-600 font-medium uppercase tracking-wide mb-1">
              {product.category.name}
            </p>
          )}

          {/* Name */}
          <h3 className="font-semibold text-gray-900 line-clamp-2 group-hover:text-primary-600 transition-colors">
            {product.name}
          </h3>

          {/* Rating */}
          {product.rating !== undefined && (
            <div className="flex items-center gap-1 mt-2">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <FiStar
                    key={i}
                    className={clsx(
                      'w-3.5 h-3.5',
                      i < Math.floor(product.rating || 0)
                        ? 'text-yellow-400 fill-current'
                        : 'text-gray-300'
                    )}
                  />
                ))}
              </div>
              <span className="text-xs text-gray-500">
                ({product.review_count || 0})
              </span>
            </div>
          )}

          {/* Price */}
          <div className="flex items-center gap-2 mt-3">
            <span className="text-lg font-bold text-gray-900">
              ${product.price?.toFixed(2)}
            </span>
            {product.original_price && product.original_price > product.price && (
              <span className="text-sm text-gray-400 line-through">
                ${product.original_price?.toFixed(2)}
              </span>
            )}
          </div>

          {/* Brand */}
          {product.brand && (
            <p className="text-xs text-gray-500 mt-1">
              by {product.brand}
            </p>
          )}
        </div>
      </Link>
    </div>
  )
}

export default ProductCard
