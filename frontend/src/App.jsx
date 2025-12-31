import { Routes, Route } from 'react-router-dom'
import { useEffect } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

// Layout
import MainLayout from './layouts/MainLayout'

// Pages
import HomePage from './pages/HomePage'
import ProductsPage from './pages/ProductsPage'
import ProductDetailPage from './pages/ProductDetailPage'
import CartPage from './pages/CartPage'
import CheckoutPage from './pages/CheckoutPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ProfilePage from './pages/ProfilePage'
import OrdersPage from './pages/OrdersPage'
import WishlistPage from './pages/WishlistPage'
import ContactPage from './pages/ContactPage'
import FAQsPage from './pages/FAQsPage'
import ShippingPage from './pages/ShippingPage'
import ReturnsPage from './pages/ReturnsPage'
import SizeGuidePage from './pages/SizeGuidePage'
import NotFoundPage from './pages/NotFoundPage'

// Register GSAP plugins
gsap.registerPlugin(ScrollTrigger)

function App() {
  useEffect(() => {
    // Initialize GSAP defaults
    gsap.defaults({
      ease: 'power3.out',
      duration: 0.8,
    })

    // Refresh ScrollTrigger on route change
    ScrollTrigger.refresh()
  }, [])

  return (
    <Routes>
      {/* Public routes with main layout */}
      <Route path="/" element={<MainLayout />}>
        <Route index element={<HomePage />} />
        <Route path="products" element={<ProductsPage />} />
        <Route path="products/:slug" element={<ProductDetailPage />} />
        <Route path="category/:slug" element={<ProductsPage />} />
        <Route path="cart" element={<CartPage />} />
        <Route path="checkout" element={<CheckoutPage />} />
        <Route path="profile" element={<ProfilePage />} />
        <Route path="orders" element={<OrdersPage />} />
        <Route path="wishlist" element={<WishlistPage />} />
        {/* Support Pages */}
        <Route path="contact" element={<ContactPage />} />
        <Route path="faqs" element={<FAQsPage />} />
        <Route path="shipping" element={<ShippingPage />} />
        <Route path="returns" element={<ReturnsPage />} />
        <Route path="size-guide" element={<SizeGuidePage />} />
      </Route>

      {/* Auth routes (no layout) */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* 404 */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

export default App
