import { Link } from 'react-router-dom'
import { FiMail, FiPhone, FiMapPin, FiFacebook, FiTwitter, FiInstagram, FiYoutube } from 'react-icons/fi'

const Footer = () => {
  const currentYear = new Date().getFullYear()

  const footerLinks = {
    shop: [
      { name: 'All Products', href: '/products' },
      { name: 'Electronics', href: '/category/electronics' },
      { name: 'Smartphones', href: '/category/smartphones' },
      { name: 'Laptops', href: '/category/laptops' },
      { name: 'Fashion', href: '/category/fashion' },
      { name: 'Gaming', href: '/category/gaming' },
    ],
    account: [
      { name: 'My Account', href: '/profile' },
      { name: 'Order History', href: '/orders' },
      { name: 'Wishlist', href: '/wishlist' },
      { name: 'Shopping Cart', href: '/cart' },
    ],
    support: [
      { name: 'Contact Us', href: '/contact' },
      { name: 'FAQs', href: '/faqs' },
      { name: 'Shipping Info', href: '/shipping' },
      { name: 'Returns & Refunds', href: '/returns' },
      { name: 'Size Guide', href: '/size-guide' },
    ],
    company: [
      { name: 'About Us', href: '/about' },
      { name: 'Careers', href: '/careers' },
      { name: 'Blog', href: '/blog' },
      { name: 'Privacy Policy', href: '/privacy' },
      { name: 'Terms of Service', href: '/terms' },
    ],
  }

  return (
    <footer className="bg-gray-900 text-gray-300">
      {/* Newsletter section */}
      <div className="bg-gradient-to-r from-primary-600 to-accent-600">
        <div className="container mx-auto px-4 py-10">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div>
              <h3 className="text-xl font-display font-bold text-white">
                Subscribe to our Newsletter
              </h3>
              <p className="text-primary-100 mt-1">
                Get exclusive deals, new arrivals & more delivered to your inbox
              </p>
            </div>
            <form className="flex w-full md:w-auto gap-2">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 md:w-80 px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50"
              />
              <button
                type="submit"
                className="px-6 py-3 bg-white text-primary-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Main footer content */}
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8">
          {/* Brand section */}
          <div className="col-span-2 md:col-span-1">
            <Link to="/" className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-accent-500 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-xl">F</span>
              </div>
              <span className="text-xl font-display font-bold text-white">
                FlaskMarket
              </span>
            </Link>
            <p className="text-sm text-gray-400 mb-4">
              Your premier destination for quality products at unbeatable prices.
              Shop with confidence and enjoy our premium customer service.
            </p>
            <div className="flex gap-3">
              <a
                href="#"
                className="w-9 h-9 bg-gray-800 rounded-full flex items-center justify-center hover:bg-primary-600 transition-colors"
              >
                <FiFacebook className="w-4 h-4" />
              </a>
              <a
                href="#"
                className="w-9 h-9 bg-gray-800 rounded-full flex items-center justify-center hover:bg-primary-600 transition-colors"
              >
                <FiTwitter className="w-4 h-4" />
              </a>
              <a
                href="#"
                className="w-9 h-9 bg-gray-800 rounded-full flex items-center justify-center hover:bg-primary-600 transition-colors"
              >
                <FiInstagram className="w-4 h-4" />
              </a>
              <a
                href="#"
                className="w-9 h-9 bg-gray-800 rounded-full flex items-center justify-center hover:bg-primary-600 transition-colors"
              >
                <FiYoutube className="w-4 h-4" />
              </a>
            </div>
          </div>

          {/* Shop links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Shop</h4>
            <ul className="space-y-2">
              {footerLinks.shop.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.href}
                    className="text-sm text-gray-400 hover:text-white transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Account links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Account</h4>
            <ul className="space-y-2">
              {footerLinks.account.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.href}
                    className="text-sm text-gray-400 hover:text-white transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Support links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Support</h4>
            <ul className="space-y-2">
              {footerLinks.support.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.href}
                    className="text-sm text-gray-400 hover:text-white transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact info */}
          <div>
            <h4 className="text-white font-semibold mb-4">Contact</h4>
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <FiMapPin className="w-4 h-4 mt-1 text-primary-500" />
                <span className="text-sm text-gray-400">
                  Hyderabad<br />
                  Telangana, India
                </span>
              </li>
              <li className="flex items-center gap-3">
                <FiPhone className="w-4 h-4 text-primary-500" />
                <span className="text-sm text-gray-400">+91 1234567890</span>
              </li>
              <li className="flex items-center gap-3">
                <FiMail className="w-4 h-4 text-primary-500" />
                <span className="text-sm text-gray-400">yugendrabsns@gmail.com</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Payment methods & bottom bar */}
        <div className="mt-12 pt-8 border-t border-gray-800">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-gray-500">
              © {currentYear} FlaskMarket. All rights reserved.
            </p>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-500">We accept:</span>
              <div className="flex items-center gap-2">
                {/* Payment icons (placeholder) */}
                <div className="w-10 h-6 bg-gray-700 rounded flex items-center justify-center text-xs text-gray-400">
                  Visa
                </div>
                <div className="w-10 h-6 bg-gray-700 rounded flex items-center justify-center text-xs text-gray-400">
                  MC
                </div>
                <div className="w-10 h-6 bg-gray-700 rounded flex items-center justify-center text-xs text-gray-400">
                  Amex
                </div>
                <div className="w-10 h-6 bg-gray-700 rounded flex items-center justify-center text-xs text-gray-400">
                  PP
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
