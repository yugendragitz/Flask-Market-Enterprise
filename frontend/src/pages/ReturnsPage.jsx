import { FiRefreshCw, FiPackage, FiDollarSign, FiClock, FiCheckCircle, FiAlertCircle } from 'react-icons/fi'

const ReturnsPage = () => {
  const steps = [
    {
      step: 1,
      title: 'Initiate Return',
      description: 'Log into your account, go to Order History, and click "Return Items" on the order you want to return.',
      icon: FiPackage
    },
    {
      step: 2,
      title: 'Pack Your Items',
      description: 'Place items in their original packaging with all tags attached. Print and attach the prepaid return label.',
      icon: FiRefreshCw
    },
    {
      step: 3,
      title: 'Ship It Back',
      description: 'Drop off the package at any authorized shipping location. We recommend keeping the tracking receipt.',
      icon: FiClock
    },
    {
      step: 4,
      title: 'Get Refunded',
      description: 'Once we receive and inspect your return, your refund will be processed within 5-7 business days.',
      icon: FiDollarSign
    }
  ]

  return (
    <div className="pt-32 pb-16">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-display font-bold text-gray-900 mb-4">Returns & Refunds</h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            We want you to love your purchase. If something isn't right, we're here to help.
          </p>
        </div>

        {/* Return Policy Highlights */}
        <div className="grid md:grid-cols-3 gap-6 mb-16">
          <div className="card p-6 text-center">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">30</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">30-Day Returns</h3>
            <p className="text-gray-600 text-sm">Return most items within 30 days of delivery for a full refund.</p>
          </div>
          <div className="card p-6 text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <FiPackage className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Free Returns</h3>
            <p className="text-gray-600 text-sm">We provide prepaid return labels for all eligible returns.</p>
          </div>
          <div className="card p-6 text-center">
            <div className="w-16 h-16 bg-accent-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <FiDollarSign className="w-8 h-8 text-accent-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Quick Refunds</h3>
            <p className="text-gray-600 text-sm">Refunds processed within 5-7 business days of receiving your return.</p>
          </div>
        </div>

        {/* How to Return */}
        <div className="max-w-4xl mx-auto mb-16">
          <h2 className="text-2xl font-semibold text-gray-900 text-center mb-8">How to Return an Item</h2>
          <div className="grid md:grid-cols-4 gap-6">
            {steps.map((item) => (
              <div key={item.step} className="text-center">
                <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-lg font-bold">
                  {item.step}
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{item.title}</h3>
                <p className="text-gray-600 text-sm">{item.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Policy Details */}
        <div className="max-w-4xl mx-auto">
          <div className="card p-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">Return Policy Details</h2>
            
            <div className="space-y-6">
              {/* Eligible Items */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <FiCheckCircle className="text-green-500" />
                  Eligible for Returns
                </h3>
                <ul className="space-y-2 text-gray-600 ml-6">
                  <li>• Items in original, unused condition with tags attached</li>
                  <li>• Items in original packaging</li>
                  <li>• Items returned within 30 days of delivery</li>
                  <li>• Electronics with all accessories and manuals included</li>
                  <li>• Clothing and shoes that haven't been worn or washed</li>
                </ul>
              </div>

              {/* Non-Eligible Items */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <FiAlertCircle className="text-red-500" />
                  Not Eligible for Returns
                </h3>
                <ul className="space-y-2 text-gray-600 ml-6">
                  <li>• Intimate apparel, swimwear, and pierced jewelry (final sale)</li>
                  <li>• Personalized or customized items</li>
                  <li>• Items marked as "Final Sale" or "Non-Returnable"</li>
                  <li>• Items damaged through customer misuse</li>
                  <li>• Gift cards and downloadable products</li>
                  <li>• Items returned after 30 days</li>
                </ul>
              </div>

              {/* Refund Methods */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Refund Methods</h3>
                <p className="text-gray-600 mb-3">
                  Refunds are issued to the original payment method used for the purchase:
                </p>
                <ul className="space-y-2 text-gray-600 ml-6">
                  <li>• Credit/Debit Card: 5-10 business days to appear on statement</li>
                  <li>• PayPal: 3-5 business days</li>
                  <li>• Store Credit: Immediate upon approval</li>
                  <li>• Gift Card: Refunded as store credit</li>
                </ul>
              </div>

              {/* Exchanges */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Exchanges</h3>
                <p className="text-gray-600">
                  Want to exchange an item for a different size or color? The fastest way is to return the original item and place a new order. Alternatively, contact our customer support team to arrange a direct exchange if the item is in stock.
                </p>
              </div>

              {/* Damaged Items */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Damaged or Defective Items</h3>
                <p className="text-gray-600">
                  If you received a damaged or defective item, please contact us within 48 hours of delivery. We'll arrange for a free return and send you a replacement or full refund. Please include photos of the damage when contacting support.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Contact CTA */}
        <div className="mt-12 text-center">
          <p className="text-gray-600 mb-4">Need help with a return?</p>
          <a href="/contact" className="btn btn-primary">Contact Support</a>
        </div>
      </div>
    </div>
  )
}

export default ReturnsPage
