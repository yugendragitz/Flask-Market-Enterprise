import { useState, useEffect, useRef } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { FiHeart, FiShoppingCart, FiMinus, FiPlus, FiStar, FiTruck, FiShield, FiRefreshCw, FiShare2 } from 'react-icons/fi'
import gsap from 'gsap'
import clsx from 'clsx'
import { productsAPI, wishlistAPI } from '../services/api'
import useCartStore from '../store/cartStore'
import useAuthStore from '../store/authStore'
import toast from 'react-hot-toast'

const ProductDetailPage = () => {
  const { slug } = useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [quantity, setQuantity] = useState(1)
  const [selectedImage, setSelectedImage] = useState(0)
  const [activeTab, setActiveTab] = useState('description')
  
  const imageRef = useRef(null)
  const addItem = useCartStore((state) => state.addItem)
  const { isAuthenticated } = useAuthStore()

  // Fetch product
  const { data: product, isLoading, error } = useQuery({
    queryKey: ['product', slug],
    queryFn: async () => {
      const response = await productsAPI.getOne(slug)
      // Handle nested response structure
      const data = response.data.data?.product || response.data.data || response.data
      return data
    },
  })

  // Fetch wishlist to check if product is already in wishlist
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

  // GSAP animation
  useEffect(() => {
    if (product) {
      gsap.fromTo(
        '.product-detail',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }
      )
    }
  }, [product])

  // Handle quantity change
  const decreaseQuantity = () => {
    if (quantity > 1) setQuantity(quantity - 1)
  }

  const increaseQuantity = () => {
    const maxStock = product?.stock_quantity ?? product?.stock ?? 10
    if (quantity < maxStock) setQuantity(quantity + 1)
  }

  // Handle add to cart
  const handleAddToCart = () => {
    if (product) {
      addItem(product, quantity)
      setQuantity(1)
    }
  }

  // Handle wishlist
  const handleWishlist = () => {
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

  // Handle share
  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href)
    toast.success('Link copied to clipboard!')
  }

  if (isLoading) {
    return (
      <div className="pt-32 pb-16">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-2 gap-10">
            <div className="aspect-square skeleton rounded-2xl" />
            <div className="space-y-4">
              <div className="h-6 skeleton w-1/4" />
              <div className="h-10 skeleton w-3/4" />
              <div className="h-8 skeleton w-1/3" />
              <div className="h-24 skeleton" />
              <div className="h-12 skeleton w-1/2" />
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error || !product) {
    return (
      <div className="pt-32 pb-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-2xl font-bold text-gray-900">Product not found</h1>
          <Link to="/products" className="btn btn-primary mt-4">
            Back to Products
          </Link>
        </div>
      </div>
    )
  }

  const images = product.images?.length > 0 
    ? product.images 
    : [{ image_url: product.thumbnail_url || product.image_url || 'https://via.placeholder.com/600' }]

  const discountPercentage = product.compare_price && product.compare_price > product.price
    ? Math.round(((product.compare_price - product.price) / product.compare_price) * 100)
    : product.discount_percentage || 0
  
  const stockQuantity = product.stock_quantity ?? product.stock ?? 0
  const originalPrice = product.compare_price || product.original_price

  return (
    <div className="pt-32 pb-16">
      <div className="container mx-auto px-4">
        {/* Breadcrumb */}
        <nav className="flex items-center gap-2 text-sm text-gray-500 mb-8">
          <Link to="/" className="hover:text-primary-600">Home</Link>
          <span>/</span>
          <Link to="/products" className="hover:text-primary-600">Products</Link>
          {product.categories?.length > 0 && (
            <>
              <span>/</span>
              <Link
                to={`/category/${product.categories[0].slug}`}
                className="hover:text-primary-600"
              >
                {product.categories[0].name}
              </Link>
            </>
          )}
          <span>/</span>
          <span className="text-gray-900">{product.name}</span>
        </nav>

        <div className="product-detail grid md:grid-cols-2 gap-10">
          {/* Image Gallery */}
          <div className="space-y-4">
            {/* Main Image */}
            <div
              ref={imageRef}
              className="aspect-square bg-gray-100 rounded-2xl overflow-hidden relative group"
            >
              <img
                src={images[selectedImage]?.image_url}
                alt={product.name}
                className="w-full h-full object-cover"
              />
              {discountPercentage > 0 && (
                <span className="absolute top-4 left-4 bg-danger-500 text-white text-sm font-bold px-3 py-1 rounded-full">
                  -{discountPercentage}%
                </span>
              )}
            </div>

            {/* Thumbnails */}
            {images.length > 1 && (
              <div className="flex gap-3 overflow-x-auto no-scrollbar">
                {images.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedImage(index)}
                    className={clsx(
                      'flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-colors',
                      selectedImage === index
                        ? 'border-primary-500'
                        : 'border-transparent hover:border-gray-300'
                    )}
                  >
                    <img
                      src={image.image_url}
                      alt={`${product.name} ${index + 1}`}
                      className="w-full h-full object-cover"
                    />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            {/* Category & Brand */}
            <div className="flex items-center gap-3">
              {product.categories?.length > 0 && (
                <Link
                  to={`/category/${product.categories[0].slug}`}
                  className="text-sm text-primary-600 font-medium hover:text-primary-700"
                >
                  {product.categories[0].name}
                </Link>
              )}
              {product.brand && (
                <span className="text-sm text-gray-500">by {product.brand}</span>
              )}
            </div>

            {/* Name */}
            <h1 className="text-3xl md:text-4xl font-display font-bold text-gray-900">
              {product.name}
            </h1>

            {/* Rating */}
            {(product.average_rating !== undefined || product.review_count > 0) && (
              <div className="flex items-center gap-3">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <FiStar
                      key={i}
                      className={clsx(
                        'w-5 h-5',
                        i < Math.floor(product.average_rating || product.rating || 0)
                          ? 'text-yellow-400 fill-current'
                          : 'text-gray-300'
                      )}
                    />
                  ))}
                </div>
                <span className="text-gray-600">
                  {(product.average_rating || product.rating || 0).toFixed(1)} ({product.review_count || 0} reviews)
                </span>
              </div>
            )}

            {/* Price */}
            <div className="flex items-baseline gap-3">
              <span className="text-4xl font-bold text-gray-900">
                ${product.price?.toFixed(2)}
              </span>
              {originalPrice && originalPrice > product.price && (
                <>
                  <span className="text-xl text-gray-400 line-through">
                    ${originalPrice?.toFixed(2)}
                  </span>
                  <span className="text-sm font-medium text-success-600 bg-success-50 px-2 py-1 rounded">
                    Save ${(originalPrice - product.price).toFixed(2)}
                  </span>
                </>
              )}
            </div>

            {/* Description */}
            <p className="text-gray-600 leading-relaxed">
              {product.description}
            </p>

            {/* Stock Status */}
            <div className="flex items-center gap-2">
              <span
                className={clsx(
                  'w-2 h-2 rounded-full',
                  stockQuantity > 10
                    ? 'bg-success-500'
                    : stockQuantity > 0
                    ? 'bg-warning-500'
                    : 'bg-danger-500'
                )}
              />
              <span className="text-sm text-gray-600">
                {stockQuantity > 10
                  ? 'In Stock'
                  : stockQuantity > 0
                  ? `Only ${stockQuantity} left`
                  : 'Out of Stock'}
              </span>
            </div>

            {/* Quantity & Add to Cart */}
            <div className="flex flex-wrap items-center gap-4">
              {/* Quantity selector */}
              <div className="flex items-center border border-gray-300 rounded-lg">
                <button
                  onClick={decreaseQuantity}
                  disabled={quantity <= 1}
                  className="p-3 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <FiMinus className="w-4 h-4" />
                </button>
                <span className="w-12 text-center font-medium">{quantity}</span>
                <button
                  onClick={increaseQuantity}
                  disabled={quantity >= stockQuantity}
                  className="p-3 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <FiPlus className="w-4 h-4" />
                </button>
              </div>

              {/* Add to Cart */}
              <button
                onClick={handleAddToCart}
                disabled={stockQuantity === 0}
                className="flex-1 btn btn-primary btn-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <FiShoppingCart className="w-5 h-5 mr-2" />
                Add to Cart
              </button>

              {/* Wishlist */}
              <button
                onClick={handleWishlist}
                disabled={addToWishlistMutation.isPending || removeFromWishlistMutation.isPending}
                className={clsx(
                  "p-3 border rounded-lg transition-colors disabled:opacity-50",
                  isInWishlist
                    ? "bg-danger-50 border-danger-300 text-danger-500"
                    : "border-gray-300 hover:bg-gray-100 hover:border-danger-300 hover:text-danger-500"
                )}
              >
                <FiHeart className={clsx("w-5 h-5", isInWishlist && "fill-current")} />
              </button>

              {/* Share */}
              <button
                onClick={handleShare}
                className="p-3 border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <FiShare2 className="w-5 h-5" />
              </button>
            </div>

            {/* Features */}
            <div className="grid grid-cols-3 gap-4 pt-6 border-t">
              <div className="text-center">
                <FiTruck className="w-6 h-6 mx-auto text-primary-600 mb-2" />
                <p className="text-xs text-gray-600">Free Shipping</p>
              </div>
              <div className="text-center">
                <FiShield className="w-6 h-6 mx-auto text-primary-600 mb-2" />
                <p className="text-xs text-gray-600">2 Year Warranty</p>
              </div>
              <div className="text-center">
                <FiRefreshCw className="w-6 h-6 mx-auto text-primary-600 mb-2" />
                <p className="text-xs text-gray-600">30-Day Returns</p>
              </div>
            </div>

            {/* SKU & Barcode */}
            <div className="pt-4 border-t text-sm text-gray-500">
              {product.sku && <p>SKU: {product.sku}</p>}
              {product.barcode && <p>Barcode: {product.barcode}</p>}
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="mt-16">
          <div className="flex border-b">
            {['description', 'reviews', 'shipping'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={clsx(
                  'px-6 py-3 font-medium border-b-2 transition-colors capitalize',
                  activeTab === tab
                    ? 'border-primary-600 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                )}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="py-8">
            {activeTab === 'description' && (
              <div className="prose max-w-none">
                <p className="text-gray-600 leading-relaxed">
                  {product.description}
                </p>
              </div>
            )}

            {activeTab === 'reviews' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-semibold">Customer Reviews</h3>
                  <button className="btn btn-outline btn-sm">Write a Review</button>
                </div>
                
                {product.reviews?.length > 0 ? (
                  <div className="space-y-4">
                    {product.reviews.map((review) => (
                      <div key={review.id} className="card p-4">
                        <div className="flex items-center gap-3 mb-2">
                          <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                            <span className="font-medium text-primary-600">
                              {review.user?.username?.[0]?.toUpperCase() || 'U'}
                            </span>
                          </div>
                          <div>
                            <p className="font-medium">{review.user?.username || 'Anonymous'}</p>
                            <div className="flex items-center gap-1">
                              {[...Array(5)].map((_, i) => (
                                <FiStar
                                  key={i}
                                  className={clsx(
                                    'w-3 h-3',
                                    i < review.rating
                                      ? 'text-yellow-400 fill-current'
                                      : 'text-gray-300'
                                  )}
                                />
                              ))}
                            </div>
                          </div>
                        </div>
                        <p className="text-gray-600">{review.comment}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-8">
                    No reviews yet. Be the first to review this product!
                  </p>
                )}
              </div>
            )}

            {activeTab === 'shipping' && (
              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <FiTruck className="w-6 h-6 text-primary-600 mt-1" />
                  <div>
                    <h4 className="font-medium">Free Standard Shipping</h4>
                    <p className="text-gray-600 text-sm">
                      Orders over $100 qualify for free standard shipping. Delivery within 5-7 business days.
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <FiRefreshCw className="w-6 h-6 text-primary-600 mt-1" />
                  <div>
                    <h4 className="font-medium">30-Day Returns</h4>
                    <p className="text-gray-600 text-sm">
                      Not satisfied? Return within 30 days for a full refund. Items must be in original condition.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProductDetailPage
