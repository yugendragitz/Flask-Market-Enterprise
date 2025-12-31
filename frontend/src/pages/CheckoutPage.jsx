import { Link } from 'react-router-dom'

const CheckoutPage = () => {
  return (
    <div className="pt-32 pb-16">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-display font-bold text-gray-900 mb-8">
          Checkout
        </h1>
        <div className="card p-8 text-center">
          <p className="text-gray-500 mb-4">Checkout page coming soon!</p>
          <Link to="/cart" className="btn btn-primary">Back to Cart</Link>
        </div>
      </div>
    </div>
  )
}

export default CheckoutPage
