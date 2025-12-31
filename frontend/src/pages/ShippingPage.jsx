import { FiTruck, FiPackage, FiGlobe, FiClock, FiCheckCircle } from 'react-icons/fi'

const ShippingPage = () => {
  const shippingOptions = [
    {
      name: 'Standard Shipping',
      price: 'FREE over $50 / $5.99',
      time: '5-7 business days',
      icon: FiPackage,
      features: ['Track your package', 'Email notifications', 'Signature not required']
    },
    {
      name: 'Express Shipping',
      price: '$12.99',
      time: '2-3 business days',
      icon: FiTruck,
      features: ['Priority handling', 'Real-time tracking', 'Signature optional']
    },
    {
      name: 'Same-Day Delivery',
      price: '$24.99',
      time: 'Same day (select areas)',
      icon: FiClock,
      features: ['Order by 12 PM', 'Available in major cities', 'Signature required']
    },
    {
      name: 'International Shipping',
      price: 'Starting at $19.99',
      time: '10-15 business days',
      icon: FiGlobe,
      features: ['Available worldwide', 'Customs handling', 'Full tracking']
    }
  ]

  return (
    <div className="pt-32 pb-16">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-display font-bold text-gray-900 mb-4">Shipping Information</h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            We offer multiple shipping options to get your order to you as quickly as possible.
          </p>
        </div>

        {/* Shipping Options */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {shippingOptions.map((option) => (
            <div key={option.name} className="card p-6 hover:shadow-lg transition-shadow">
              <div className="w-14 h-14 bg-primary-100 rounded-xl flex items-center justify-center mb-4">
                <option.icon className="w-7 h-7 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{option.name}</h3>
              <p className="text-2xl font-bold text-primary-600 mb-1">{option.price}</p>
              <p className="text-sm text-gray-500 mb-4">{option.time}</p>
              <ul className="space-y-2">
                {option.features.map((feature) => (
                  <li key={feature} className="flex items-center gap-2 text-sm text-gray-600">
                    <FiCheckCircle className="w-4 h-4 text-green-500" />
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Additional Info */}
        <div className="max-w-4xl mx-auto">
          <div className="card p-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">Shipping Policies</h2>
            
            <div className="space-y-6">
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Order Processing</h3>
                <p className="text-gray-600">
                  Orders are processed within 1-2 business days. Orders placed on weekends or holidays will be processed the next business day. You will receive an email confirmation once your order ships with tracking information.
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Free Shipping Threshold</h3>
                <p className="text-gray-600">
                  Enjoy FREE standard shipping on all orders over $50 within the continental United States. This offer applies automatically at checkout when your cart total meets the minimum requirement.
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Delivery Areas</h3>
                <p className="text-gray-600">
                  We ship to all 50 US states, Puerto Rico, and over 100 countries worldwide. Same-day delivery is available in select metropolitan areas including New York, Los Angeles, San Francisco, Chicago, and Miami.
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Tracking Your Order</h3>
                <p className="text-gray-600">
                  Once your order ships, you'll receive a tracking number via email. You can track your package using the link in the email or by logging into your account and viewing your order history.
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Shipping Restrictions</h3>
                <p className="text-gray-600">
                  Some products may have shipping restrictions due to size, weight, or regulatory requirements. Hazardous materials cannot be shipped by air. Items that exceed standard dimensions may incur additional shipping charges.
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-gray-900 mb-2">International Shipping</h3>
                <p className="text-gray-600">
                  International orders may be subject to import duties and taxes, which are the responsibility of the recipient. Delivery times for international orders vary by destination. We are not responsible for delays due to customs processing.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Contact CTA */}
        <div className="mt-12 text-center">
          <p className="text-gray-600 mb-4">Have questions about shipping?</p>
          <a href="/contact" className="btn btn-primary">Contact Us</a>
        </div>
      </div>
    </div>
  )
}

export default ShippingPage
