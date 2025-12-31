import { Link } from 'react-router-dom'
import useAuthStore from '../store/authStore'

const ProfilePage = () => {
  const { user } = useAuthStore()

  if (!user) {
    return (
      <div className="pt-32 pb-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Please login to view your profile</h1>
          <Link to="/login" className="btn btn-primary">Login</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="pt-32 pb-16">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-display font-bold text-gray-900 mb-8">
          My Profile
        </h1>
        <div className="card p-8">
          <div className="flex items-center gap-6 mb-8">
            <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-accent-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-3xl">
                {user.username?.[0]?.toUpperCase()}
              </span>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{user.username}</h2>
              <p className="text-gray-500">{user.email}</p>
              <span className="badge badge-primary mt-2">{user.role || 'Customer'}</span>
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div className="p-4 bg-gray-50 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-2">Wallet Balance</h3>
              <p className="text-2xl font-bold text-primary-600">
                ${user.budget?.toFixed(2) || '0.00'}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-2">Account Status</h3>
              <p className={`font-medium ${user.is_verified ? 'text-success-600' : 'text-warning-600'}`}>
                {user.is_verified ? 'Verified' : 'Pending Verification'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProfilePage
