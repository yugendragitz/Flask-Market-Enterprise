import { useState } from 'react'
import { FiChevronDown, FiChevronUp, FiSearch } from 'react-icons/fi'

const FAQsPage = () => {
  const [openIndex, setOpenIndex] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')

  const faqs = [
    {
      category: 'Orders & Shipping',
      questions: [
        {
          q: 'How do I track my order?',
          a: 'Once your order is shipped, you will receive an email with a tracking number. You can use this number to track your package on our website or the carrier\'s website. You can also view your order status by logging into your account and visiting the Order History page.'
        },
        {
          q: 'How long does shipping take?',
          a: 'Standard shipping typically takes 5-7 business days. Express shipping takes 2-3 business days. Same-day delivery is available in select areas for orders placed before 12 PM. International shipping may take 10-15 business days depending on the destination.'
        },
        {
          q: 'Do you offer free shipping?',
          a: 'Yes! We offer free standard shipping on all orders over $50. For orders under $50, a flat rate of $5.99 applies. Express and same-day delivery options have additional charges.'
        },
        {
          q: 'Can I change my shipping address after placing an order?',
          a: 'You can change your shipping address within 1 hour of placing your order. After that, please contact our customer support team as soon as possible, and we will try our best to accommodate your request before the order is shipped.'
        }
      ]
    },
    {
      category: 'Returns & Refunds',
      questions: [
        {
          q: 'What is your return policy?',
          a: 'We accept returns within 30 days of delivery for most items. Products must be unused, in original packaging, and with all tags attached. Some items like intimate apparel and customized products are final sale.'
        },
        {
          q: 'How do I initiate a return?',
          a: 'To initiate a return, log into your account, go to Order History, select the order, and click "Return Items". You can also contact our customer support team for assistance. Once approved, you will receive a prepaid return shipping label.'
        },
        {
          q: 'When will I receive my refund?',
          a: 'Refunds are processed within 5-7 business days after we receive and inspect the returned item. The refund will be credited to your original payment method. Please note that it may take additional time for your bank to process the refund.'
        },
        {
          q: 'Can I exchange an item?',
          a: 'Yes! You can exchange items for a different size or color within 30 days. Simply initiate a return and place a new order for the desired item, or contact customer support for a direct exchange.'
        }
      ]
    },
    {
      category: 'Payment',
      questions: [
        {
          q: 'What payment methods do you accept?',
          a: 'We accept Visa, Mastercard, American Express, PayPal, Apple Pay, Google Pay, and FlaskMarket gift cards. All transactions are secured with SSL encryption.'
        },
        {
          q: 'Is my payment information secure?',
          a: 'Absolutely! We use industry-standard SSL encryption and are PCI DSS compliant. We never store your full credit card number on our servers. All payment processing is handled by secure, trusted payment providers.'
        },
        {
          q: 'Can I use multiple payment methods?',
          a: 'Currently, we support one payment method per order. However, you can combine a gift card with another payment method.'
        },
        {
          q: 'Do you offer payment plans?',
          a: 'Yes! For orders over $100, we offer installment payment options through Klarna and Afterpay. You can choose to pay in 4 interest-free installments at checkout.'
        }
      ]
    },
    {
      category: 'Account',
      questions: [
        {
          q: 'How do I create an account?',
          a: 'Click the "Sign Up" button in the top right corner of the website. Fill in your details including email, password, and name. You can also sign up using your Google or Apple account for faster registration.'
        },
        {
          q: 'I forgot my password. What should I do?',
          a: 'Click "Forgot Password" on the login page and enter your email address. You will receive a password reset link within a few minutes. If you don\'t see the email, please check your spam folder.'
        },
        {
          q: 'How do I update my account information?',
          a: 'Log into your account and go to the Profile page. From there, you can update your personal information, shipping addresses, payment methods, and communication preferences.'
        },
        {
          q: 'How do I delete my account?',
          a: 'To delete your account, please contact our customer support team. Please note that account deletion is permanent and cannot be undone. Your order history will be retained for legal purposes.'
        }
      ]
    }
  ]

  const filteredFaqs = searchQuery
    ? faqs.map(category => ({
        ...category,
        questions: category.questions.filter(
          faq => faq.q.toLowerCase().includes(searchQuery.toLowerCase()) ||
                 faq.a.toLowerCase().includes(searchQuery.toLowerCase())
        )
      })).filter(category => category.questions.length > 0)
    : faqs

  return (
    <div className="pt-32 pb-16">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-display font-bold text-gray-900 mb-4">Frequently Asked Questions</h1>
          <p className="text-gray-600 max-w-2xl mx-auto mb-8">
            Find answers to common questions about orders, shipping, returns, and more.
          </p>
          
          {/* Search */}
          <div className="max-w-xl mx-auto relative">
            <FiSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search FAQs..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
        </div>

        {/* FAQs */}
        <div className="max-w-4xl mx-auto space-y-8">
          {filteredFaqs.map((category, catIndex) => (
            <div key={category.category}>
              <h2 className="text-xl font-semibold text-gray-900 mb-4">{category.category}</h2>
              <div className="space-y-3">
                {category.questions.map((faq, faqIndex) => {
                  const index = `${catIndex}-${faqIndex}`
                  const isOpen = openIndex === index
                  
                  return (
                    <div key={index} className="card overflow-hidden">
                      <button
                        onClick={() => setOpenIndex(isOpen ? null : index)}
                        className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-gray-50 transition-colors"
                      >
                        <span className="font-medium text-gray-900 pr-4">{faq.q}</span>
                        {isOpen ? (
                          <FiChevronUp className="w-5 h-5 text-gray-500 flex-shrink-0" />
                        ) : (
                          <FiChevronDown className="w-5 h-5 text-gray-500 flex-shrink-0" />
                        )}
                      </button>
                      {isOpen && (
                        <div className="px-6 pb-4">
                          <p className="text-gray-600 leading-relaxed">{faq.a}</p>
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Contact CTA */}
        <div className="mt-16 text-center">
          <p className="text-gray-600 mb-4">Still have questions?</p>
          <a href="/contact" className="btn btn-primary">Contact Support</a>
        </div>
      </div>
    </div>
  )
}

export default FAQsPage
