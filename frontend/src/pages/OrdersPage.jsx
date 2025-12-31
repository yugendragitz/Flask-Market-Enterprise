import { Link } from 'react-router-dom'
import { FiPackage } from 'react-icons/fi'
import useAuthStore from '../store/authStore'

const OrdersPage = () => {
  const { user } = useAuthStore()

  if (!user) {
    return (
      <div className="pt-32 pb-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Please login to view your orders</h1>
          <Link to="/login" className="btn btn-primary">Login</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="pt-32 pb-16">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-display font-bold text-gray-900 mb-8">
          My Orders
        </h1>
        <div className="card p-8 text-center">
          <FiPackage className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No orders yet</h2>
          <p className="text-gray-500 mb-6">You haven't placed any orders yet. Start shopping!</p>
          <Link to="/products" className="btn btn-primary">Browse Products</Link>
        </div>
      </div>
    </div>
  )
}

export default OrdersPage
