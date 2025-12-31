import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate, useLocation, useParams } from 'react-router-dom'
import { FiSearch, FiShoppingCart, FiUser, FiHeart, FiMenu, FiX, FiChevronDown } from 'react-icons/fi'
import gsap from 'gsap'
import clsx from 'clsx'
import useAuthStore from '../store/authStore'
import useCartStore from '../store/cartStore'

const Header = () => {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [isSearchOpen, setIsSearchOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false)

  const headerRef = useRef(null)
  const searchRef = useRef(null)
  const navigate = useNavigate()
  const location = useLocation()
  
  // Get current category from URL
  const getCurrentCategory = () => {
    const match = location.pathname.match(/^\/category\/(.+)$/)
    return match ? match[1] : null
  }
  const currentCategory = getCurrentCategory()
  const isAllProducts = location.pathname === '/products'

  const { user, isAuthenticated, logout } = useAuthStore()
  const getItemCount = useCartStore((state) => state.getItemCount)
  const itemCount = getItemCount()

  // Handle scroll
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // GSAP animation for header
  useEffect(() => {
    gsap.fromTo(
      headerRef.current,
      { y: -100, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out' }
    )
  }, [])

  // Handle search submit
  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`/products?search=${encodeURIComponent(searchQuery)}`)
      setIsSearchOpen(false)
      setSearchQuery('')
    }
  }

  // Handle logout
  const handleLogout = async () => {
    await logout()
    setIsUserMenuOpen(false)
    navigate('/')
  }

  const categories = [
    { name: 'Electronics', slug: 'electronics' },
    { name: 'Smartphones', slug: 'smartphones' },
    { name: 'Laptops', slug: 'laptops' },
    { name: 'Fashion', slug: 'fashion' },
    { name: 'Gaming', slug: 'gaming' },
    { name: 'Home & Kitchen', slug: 'home-kitchen' },
  ]

  return (
    <header
      ref={headerRef}
      className={clsx(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        isScrolled
          ? 'bg-white/95 backdrop-blur-md shadow-md py-2'
          : 'bg-white py-4'
      )}
    >
      <div className="container mx-auto px-4">
        {/* Main header row */}
        <div className="flex items-center justify-between gap-4">
          {/* Logo */}
          <Link
            to="/"
            className="flex items-center gap-2 group"
          >
            <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-accent-600 rounded-xl flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300">
              <span className="text-white font-bold text-xl">F</span>
            </div>
            <span className="text-xl font-display font-bold gradient-text hidden sm:block">
              FlaskMarket
            </span>
          </Link>

          {/* Search bar - Desktop */}
          <form
            onSubmit={handleSearch}
            className="hidden md:flex flex-1 max-w-xl mx-4"
          >
            <div className="relative w-full group">
              <input
                type="text"
                placeholder="Search products, brands, categories..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-5 py-2.5 pl-12 bg-gray-100 border-2 border-transparent rounded-full focus:bg-white focus:border-primary-500 focus:outline-none transition-all duration-300"
              />
              <FiSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-primary-500 transition-colors" />
              <button
                type="submit"
                className="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-1.5 bg-primary-600 text-white text-sm font-medium rounded-full hover:bg-primary-700 transition-colors"
              >
                Search
              </button>
            </div>
          </form>

          {/* Actions */}
          <div className="flex items-center gap-2 sm:gap-4">
            {/* Mobile search toggle */}
            <button
              onClick={() => setIsSearchOpen(!isSearchOpen)}
              className="md:hidden p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <FiSearch className="w-5 h-5" />
            </button>

            {/* Wishlist */}
            {isAuthenticated && (
              <Link
                to="/wishlist"
                className="hidden sm:flex p-2 hover:bg-gray-100 rounded-full transition-colors relative"
              >
                <FiHeart className="w-5 h-5" />
              </Link>
            )}

            {/* Cart */}
            <Link
              to="/cart"
              className="p-2 hover:bg-gray-100 rounded-full transition-colors relative"
            >
              <FiShoppingCart className="w-5 h-5" />
              {itemCount > 0 && (
                <span className="absolute -top-1 -right-1 w-5 h-5 bg-primary-600 text-white text-xs font-bold rounded-full flex items-center justify-center animate-scale-in">
                  {itemCount > 9 ? '9+' : itemCount}
                </span>
              )}
            </Link>

            {/* User menu */}
            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                  className="flex items-center gap-2 p-2 hover:bg-gray-100 rounded-full transition-colors"
                >
                  <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-accent-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-medium text-sm">
                      {user?.username?.[0]?.toUpperCase() || 'U'}
                    </span>
                  </div>
                  <FiChevronDown
                    className={clsx(
                      'hidden sm:block w-4 h-4 transition-transform duration-200',
                      isUserMenuOpen && 'rotate-180'
                    )}
                  />
                </button>

                {/* Dropdown menu */}
                {isUserMenuOpen && (
                  <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-100 py-2 animate-slide-down">
                    <div className="px-4 py-2 border-b border-gray-100">
                      <p className="font-medium text-gray-900">{user?.username}</p>
                      <p className="text-sm text-gray-500">{user?.email}</p>
                    </div>
                    <Link
                      to="/profile"
                      className="flex items-center gap-3 px-4 py-2 hover:bg-gray-50 transition-colors"
                      onClick={() => setIsUserMenuOpen(false)}
                    >
                      <FiUser className="w-4 h-4" />
                      My Profile
                    </Link>
                    <Link
                      to="/orders"
                      className="flex items-center gap-3 px-4 py-2 hover:bg-gray-50 transition-colors"
                      onClick={() => setIsUserMenuOpen(false)}
                    >
                      <FiShoppingCart className="w-4 h-4" />
                      My Orders
                    </Link>
                    <Link
                      to="/wishlist"
                      className="flex items-center gap-3 px-4 py-2 hover:bg-gray-50 transition-colors"
                      onClick={() => setIsUserMenuOpen(false)}
                    >
                      <FiHeart className="w-4 h-4" />
                      Wishlist
                    </Link>
                    <hr className="my-2" />
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-3 px-4 py-2 text-danger-500 hover:bg-danger-50 transition-colors"
                    >
                      Logout
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="hidden sm:block px-4 py-2 text-gray-700 hover:text-primary-600 font-medium transition-colors"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 bg-primary-600 text-white font-medium rounded-full hover:bg-primary-700 transition-colors"
                >
                  Sign Up
                </Link>
              </div>
            )}

            {/* Mobile menu toggle */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="md:hidden p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              {isMobileMenuOpen ? <FiX className="w-5 h-5" /> : <FiMenu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Categories nav - Desktop */}
        <nav className="hidden md:flex items-center gap-6 mt-3 pt-3 border-t border-gray-100">
          {categories.map((category) => (
            <Link
              key={category.slug}
              to={`/category/${category.slug}`}
              className={clsx(
                "text-sm font-medium transition-colors",
                currentCategory === category.slug
                  ? "text-primary-600"
                  : "text-gray-600 hover:text-primary-600"
              )}
            >
              {category.name}
            </Link>
          ))}
          <Link
            to="/products"
            className={clsx(
              "text-sm font-medium transition-colors",
              isAllProducts
                ? "text-primary-600"
                : "text-gray-600 hover:text-primary-600"
            )}
          >
            All Products
          </Link>
        </nav>

        {/* Mobile search */}
        {isSearchOpen && (
          <form
            onSubmit={handleSearch}
            className="md:hidden mt-4 animate-slide-down"
          >
            <div className="relative">
              <input
                ref={searchRef}
                type="text"
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-4 py-3 pl-10 bg-gray-100 rounded-xl focus:bg-white focus:ring-2 focus:ring-primary-500 focus:outline-none transition-all"
                autoFocus
              />
              <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            </div>
          </form>
        )}

        {/* Mobile menu */}
        {isMobileMenuOpen && (
          <nav className="md:hidden mt-4 py-4 border-t border-gray-100 animate-slide-down">
            <div className="flex flex-col gap-2">
              {categories.map((category) => (
                <Link
                  key={category.slug}
                  to={`/category/${category.slug}`}
                  className={clsx(
                    "px-4 py-2 rounded-lg font-medium transition-colors",
                    currentCategory === category.slug
                      ? "text-primary-600 bg-primary-50"
                      : "text-gray-600 hover:text-primary-600 hover:bg-gray-50"
                  )}
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  {category.name}
                </Link>
              ))}
              <Link
                to="/products"
                className={clsx(
                  "px-4 py-2 rounded-lg font-medium transition-colors",
                  isAllProducts
                    ? "text-primary-600 bg-primary-50"
                    : "text-gray-600 hover:text-primary-600 hover:bg-gray-50"
                )}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                All Products
              </Link>
            </div>
          </nav>
        )}
      </div>
    </header>
  )
}

export default Header

