import { Link } from 'react-router-dom'
import { FiTrash2, FiMinus, FiPlus, FiShoppingBag, FiArrowRight } from 'react-icons/fi'
import useCartStore from '../store/cartStore'
import clsx from 'clsx'

const CartPage = () => {
  const { items, updateQuantity, removeItem, clearCart, getCartTotals } = useCartStore()
  const totals = getCartTotals()

  if (items.length === 0) {
    return (
      <div className="pt-32 pb-16">
        <div className="container mx-auto px-4">
          <div className="max-w-md mx-auto text-center">
            <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <FiShoppingBag className="w-12 h-12 text-gray-400" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Your cart is empty</h1>
            <p className="text-gray-500 mb-8">
              Looks like you haven't added any items to your cart yet.
            </p>
            <Link to="/products" className="btn btn-primary">
              Start Shopping
              <FiArrowRight className="ml-2" />
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="pt-32 pb-16">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-display font-bold text-gray-900 mb-8">
          Shopping Cart ({items.length} {items.length === 1 ? 'item' : 'items'})
        </h1>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2 space-y-4">
            {items.map((item) => (
              <div key={item.product_id} className="card p-4 flex gap-4">
                {/* Product Image */}
                <Link
                  to={`/products/${item.product.slug || item.product_id}`}
                  className="flex-shrink-0 w-24 h-24 md:w-32 md:h-32 bg-gray-100 rounded-lg overflow-hidden"
                >
                  <img
                    src={item.product.thumbnail_url || item.product.images?.[0]?.image_url || item.product.image_url || 'https://via.placeholder.com/200'}
                    alt={item.product.name}
                    className="w-full h-full object-cover"
                  />
                </Link>

                {/* Product Info */}
                <div className="flex-1 min-w-0">
                  <Link
                    to={`/products/${item.product.slug || item.product_id}`}
                    className="font-medium text-gray-900 hover:text-primary-600 line-clamp-2"
                  >
                    {item.product.name}
                  </Link>
                  
                  {item.product.brand && (
                    <p className="text-sm text-gray-500 mt-1">by {item.product.brand}</p>
                  )}

                  <div className="flex items-center gap-4 mt-3">
                    {/* Quantity Controls */}
                    <div className="flex items-center border border-gray-300 rounded-lg">
                      <button
                        onClick={() => updateQuantity(item.product_id, item.quantity - 1)}
                        className="p-2 hover:bg-gray-100"
                      >
                        <FiMinus className="w-4 h-4" />
                      </button>
                      <span className="w-10 text-center font-medium text-sm">
                        {item.quantity}
                      </span>
                      <button
                        onClick={() => updateQuantity(item.product_id, item.quantity + 1)}
                        disabled={item.quantity >= item.product.stock}
                        className="p-2 hover:bg-gray-100 disabled:opacity-50"
                      >
                        <FiPlus className="w-4 h-4" />
                      </button>
                    </div>

                    {/* Remove Button */}
                    <button
                      onClick={() => removeItem(item.product_id)}
                      className="text-gray-400 hover:text-danger-500 transition-colors"
                    >
                      <FiTrash2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>

                {/* Price */}
                <div className="text-right">
                  <p className="font-bold text-gray-900">
                    ${(item.price * item.quantity).toFixed(2)}
                  </p>
                  {item.quantity > 1 && (
                    <p className="text-sm text-gray-500">
                      ${item.price.toFixed(2)} each
                    </p>
                  )}
                </div>
              </div>
            ))}

            {/* Clear Cart Button */}
            <button
              onClick={clearCart}
              className="text-sm text-gray-500 hover:text-danger-500 transition-colors"
            >
              Clear all items
            </button>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="card p-6 sticky top-32">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Order Summary
              </h2>

              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Subtotal</span>
                  <span className="font-medium">${totals.subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Shipping</span>
                  <span className={clsx(
                    'font-medium',
                    totals.shipping === 0 && 'text-success-600'
                  )}>
                    {totals.shipping === 0 ? 'FREE' : `$${totals.shipping.toFixed(2)}`}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Tax (8%)</span>
                  <span className="font-medium">${totals.tax.toFixed(2)}</span>
                </div>

                <hr className="my-4" />

                <div className="flex justify-between text-base">
                  <span className="font-semibold">Total</span>
                  <span className="font-bold text-xl">${totals.total.toFixed(2)}</span>
                </div>
              </div>

              {totals.subtotal < 100 && (
                <div className="mt-4 p-3 bg-primary-50 rounded-lg">
                  <p className="text-sm text-primary-700">
                    Add ${(100 - totals.subtotal).toFixed(2)} more for free shipping!
                  </p>
                  <div className="mt-2 h-2 bg-primary-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary-600 rounded-full transition-all"
                      style={{ width: `${Math.min(100, (totals.subtotal / 100) * 100)}%` }}
                    />
                  </div>
                </div>
              )}

              <Link
                to="/checkout"
                className="btn btn-primary btn-lg w-full mt-6"
              >
                Proceed to Checkout
                <FiArrowRight className="ml-2" />
              </Link>

              <Link
                to="/products"
                className="btn btn-ghost w-full mt-3"
              >
                Continue Shopping
              </Link>

              {/* Accepted Payments */}
              <div className="mt-6 pt-4 border-t">
                <p className="text-xs text-gray-500 text-center mb-2">
                  Secure checkout powered by
                </p>
                <div className="flex justify-center gap-2">
                  <div className="w-10 h-6 bg-gray-200 rounded flex items-center justify-center text-xs text-gray-500">
                    Visa
                  </div>
                  <div className="w-10 h-6 bg-gray-200 rounded flex items-center justify-center text-xs text-gray-500">
                    MC
                  </div>
                  <div className="w-10 h-6 bg-gray-200 rounded flex items-center justify-center text-xs text-gray-500">
                    Amex
                  </div>
                  <div className="w-10 h-6 bg-gray-200 rounded flex items-center justify-center text-xs text-gray-500">
                    PP
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CartPage
