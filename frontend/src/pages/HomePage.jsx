import { useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { FiArrowRight, FiTruck, FiShield, FiCreditCard, FiHeadphones } from 'react-icons/fi'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import ProductCard from '../components/ProductCard'
import { productsAPI, categoriesAPI } from '../services/api'

gsap.registerPlugin(ScrollTrigger)

const HomePage = () => {
  const heroRef = useRef(null)
  const featuresRef = useRef(null)
  const categoriesRef = useRef(null)
  const productsRef = useRef(null)

  // Fetch featured products
  const { data: featuredProducts, isLoading: productsLoading } = useQuery({
    queryKey: ['featuredProducts'],
    queryFn: async () => {
      const response = await productsAPI.getAll({ featured: true, per_page: 8 })
      return response.data.data.products || response.data.data || []
    },
  })

  // Fetch categories
  const { data: categories, isLoading: categoriesLoading } = useQuery({
    queryKey: ['categories'],
    queryFn: async () => {
      const response = await categoriesAPI.getAll()
      return response.data.data.categories || response.data.data || []
    },
  })

  // GSAP animations
  useEffect(() => {
    // Hero animation
    const heroTl = gsap.timeline()
    heroTl
      .fromTo(
        '.hero-title',
        { opacity: 0, y: 100 },
        { opacity: 1, y: 0, duration: 1, ease: 'power3.out' }
      )
      .fromTo(
        '.hero-subtitle',
        { opacity: 0, y: 50 },
        { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' },
        '-=0.5'
      )
      .fromTo(
        '.hero-cta',
        { opacity: 0, scale: 0.8 },
        { opacity: 1, scale: 1, duration: 0.6, ease: 'back.out(1.7)' },
        '-=0.3'
      )

    // Features animation
    gsap.fromTo(
      '.feature-item',
      { opacity: 0, y: 50 },
      {
        opacity: 1,
        y: 0,
        duration: 0.6,
        stagger: 0.1,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: featuresRef.current,
          start: 'top 80%',
        },
      }
    )

    // Categories animation
    gsap.fromTo(
      '.category-card',
      { opacity: 0, scale: 0.9 },
      {
        opacity: 1,
        scale: 1,
        duration: 0.6,
        stagger: 0.1,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: categoriesRef.current,
          start: 'top 80%',
        },
      }
    )

    return () => {
      ScrollTrigger.getAll().forEach((trigger) => trigger.kill())
    }
  }, [])

  const features = [
    {
      icon: FiTruck,
      title: 'Free Shipping',
      description: 'Free delivery on orders over $100',
    },
    {
      icon: FiShield,
      title: 'Secure Payment',
      description: '100% secure payment methods',
    },
    {
      icon: FiCreditCard,
      title: 'Easy Returns',
      description: '30-day return policy',
    },
    {
      icon: FiHeadphones,
      title: '24/7 Support',
      description: 'Round the clock assistance',
    },
  ]

  return (
    <div className="pt-24">
      {/* Hero Section */}
      <section
        ref={heroRef}
        className="relative min-h-[80vh] flex items-center overflow-hidden"
      >
        {/* Realistic 4K Background Image */}
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?q=80&w=2070&auto=format&fit=crop')`,
          }}
        />
        {/* Dark overlay for better text readability */}
        <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-black/60 to-black/40" />

        <div className="container mx-auto px-4 py-20 relative z-10">
          <div className="max-w-3xl">
            <h1 className="hero-title text-5xl md:text-7xl font-display font-bold text-white leading-tight">
              Discover the
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-accent-400 to-primary-400">
                Future of Shopping
              </span>
            </h1>
            <p className="hero-subtitle mt-6 text-xl text-gray-300 max-w-xl">
              Explore thousands of premium products with unbeatable prices.
              Your one-stop destination for electronics, fashion, and more.
            </p>
            <div className="hero-cta flex flex-wrap gap-4 mt-8">
              <Link
                to="/products"
                className="btn btn-lg bg-white text-primary-900 hover:bg-gray-100 font-semibold px-8 group"
              >
                Shop Now
                <FiArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                to="/category/electronics"
                className="btn btn-lg border-2 border-white/30 text-white hover:bg-white/10"
              >
                Explore Electronics
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section ref={featuresRef} className="py-16 bg-white border-b">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="feature-item flex flex-col items-center text-center p-6"
              >
                <div className="w-14 h-14 bg-primary-100 rounded-2xl flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-primary-600" />
                </div>
                <h3 className="font-semibold text-gray-900">{feature.title}</h3>
                <p className="text-sm text-gray-500 mt-1">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section ref={categoriesRef} className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-display font-bold text-gray-900">
                Shop by Category
              </h2>
              <p className="text-gray-500 mt-1">
                Browse our curated collection of categories
              </p>
            </div>
            <Link
              to="/products"
              className="hidden sm:flex items-center gap-2 text-primary-600 font-medium hover:text-primary-700"
            >
              View All Categories
              <FiArrowRight />
            </Link>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
            {categoriesLoading
              ? [...Array(8)].map((_, i) => (
                  <div
                    key={i}
                    className="aspect-square skeleton rounded-2xl"
                  />
                ))
              : categories?.slice(0, 8).map((category, index) => (
                  <Link
                    key={category.id}
                    to={`/category/${category.slug}`}
                    className="category-card group relative aspect-square rounded-2xl overflow-hidden"
                  >
                    <img
                      src={category.image_url || `https://via.placeholder.com/400?text=${category.name}`}
                      alt={category.name}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
                    <div className="absolute bottom-0 left-0 right-0 p-4">
                      <h3 className="text-lg font-semibold text-white">
                        {category.name}
                      </h3>
                      <p className="text-sm text-gray-300 mt-1">
                        {category.product_count || 0} Products
                      </p>
                    </div>
                  </Link>
                ))}
          </div>
        </div>
      </section>

      {/* Featured Products Section */}
      <section ref={productsRef} className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-display font-bold text-gray-900">
                Featured Products
              </h2>
              <p className="text-gray-500 mt-1">
                Handpicked products just for you
              </p>
            </div>
            <Link
              to="/products"
              className="hidden sm:flex items-center gap-2 text-primary-600 font-medium hover:text-primary-700"
            >
              View All Products
              <FiArrowRight />
            </Link>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
            {productsLoading
              ? [...Array(8)].map((_, i) => (
                  <div key={i} className="card">
                    <div className="aspect-square skeleton" />
                    <div className="p-4 space-y-3">
                      <div className="h-4 skeleton w-1/3" />
                      <div className="h-5 skeleton" />
                      <div className="h-4 skeleton w-2/3" />
                      <div className="h-6 skeleton w-1/2" />
                    </div>
                  </div>
                ))
              : featuredProducts?.map((product, index) => (
                  <ProductCard
                    key={product.id}
                    product={product}
                    index={index}
                  />
                ))}
          </div>

          <div className="mt-10 text-center sm:hidden">
            <Link
              to="/products"
              className="btn btn-primary"
            >
              View All Products
              <FiArrowRight className="ml-2" />
            </Link>
          </div>
        </div>
      </section>

      {/* Promo Banner */}
      <section className="py-16 bg-gradient-to-r from-accent-600 to-primary-600">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-display font-bold text-white">
            Get 20% Off Your First Order
          </h2>
          <p className="mt-4 text-lg text-white/80 max-w-2xl mx-auto">
            Sign up for our newsletter and receive an exclusive discount code
            along with the latest deals and new arrivals.
          </p>
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center max-w-md mx-auto">
            <input
              type="email"
              placeholder="Enter your email"
              className="flex-1 px-5 py-3 rounded-full bg-white/10 border border-white/30 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50"
            />
            <button className="px-8 py-3 bg-white text-primary-600 font-semibold rounded-full hover:bg-gray-100 transition-colors">
              Get Code
            </button>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
