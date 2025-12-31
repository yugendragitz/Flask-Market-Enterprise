import { Link } from 'react-router-dom'
import { FiHome, FiArrowLeft } from 'react-icons/fi'

const NotFoundPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="text-center">
        <h1 className="text-9xl font-display font-bold gradient-text">404</h1>
        <h2 className="text-3xl font-semibold text-gray-900 mt-4">Page Not Found</h2>
        <p className="text-gray-500 mt-2 max-w-md mx-auto">
          Sorry, we couldn't find the page you're looking for. Perhaps you've mistyped the URL or the page has been moved.
        </p>
        <div className="flex items-center justify-center gap-4 mt-8">
          <button
            onClick={() => window.history.back()}
            className="btn btn-outline"
          >
            <FiArrowLeft className="mr-2" />
            Go Back
          </button>
          <Link to="/" className="btn btn-primary">
            <FiHome className="mr-2" />
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  )
}

export default NotFoundPage
