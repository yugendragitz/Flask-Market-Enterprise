import { useState } from 'react'
import { FiInfo } from 'react-icons/fi'

const SizeGuidePage = () => {
  const [activeTab, setActiveTab] = useState('clothing')

  const tabs = [
    { id: 'clothing', name: "Men's Clothing" },
    { id: 'women', name: "Women's Clothing" },
    { id: 'shoes', name: 'Shoes' },
    { id: 'kids', name: 'Kids' }
  ]

  const mensSizes = {
    tops: [
      { size: 'XS', chest: '32-34', waist: '26-28', neck: '13-13.5' },
      { size: 'S', chest: '34-36', waist: '28-30', neck: '14-14.5' },
      { size: 'M', chest: '38-40', waist: '32-34', neck: '15-15.5' },
      { size: 'L', chest: '42-44', waist: '36-38', neck: '16-16.5' },
      { size: 'XL', chest: '46-48', waist: '40-42', neck: '17-17.5' },
      { size: '2XL', chest: '50-52', waist: '44-46', neck: '18-18.5' }
    ],
    pants: [
      { size: '28', waist: '28', hip: '34-35', inseam: '30-32' },
      { size: '30', waist: '30', hip: '36-37', inseam: '30-32' },
      { size: '32', waist: '32', hip: '38-39', inseam: '30-32' },
      { size: '34', waist: '34', hip: '40-41', inseam: '30-32' },
      { size: '36', waist: '36', hip: '42-43', inseam: '30-32' },
      { size: '38', waist: '38', hip: '44-45', inseam: '30-32' }
    ]
  }

  const womensSizes = {
    tops: [
      { size: 'XS (0-2)', bust: '31-32', waist: '24-25', hip: '34-35' },
      { size: 'S (4-6)', bust: '33-34', waist: '26-27', hip: '36-37' },
      { size: 'M (8-10)', bust: '35-36', waist: '28-29', hip: '38-39' },
      { size: 'L (12-14)', bust: '37-39', waist: '30-32', hip: '40-42' },
      { size: 'XL (16-18)', bust: '40-42', waist: '33-35', hip: '43-45' },
      { size: '2XL (20-22)', bust: '43-45', waist: '36-38', hip: '46-48' }
    ]
  }

  const shoesSizes = [
    { us: '6', uk: '5.5', eu: '38.5', cm: '24' },
    { us: '6.5', uk: '6', eu: '39', cm: '24.5' },
    { us: '7', uk: '6.5', eu: '40', cm: '25' },
    { us: '7.5', uk: '7', eu: '40.5', cm: '25.5' },
    { us: '8', uk: '7.5', eu: '41', cm: '26' },
    { us: '8.5', uk: '8', eu: '42', cm: '26.5' },
    { us: '9', uk: '8.5', eu: '42.5', cm: '27' },
    { us: '9.5', uk: '9', eu: '43', cm: '27.5' },
    { us: '10', uk: '9.5', eu: '44', cm: '28' },
    { us: '10.5', uk: '10', eu: '44.5', cm: '28.5' },
    { us: '11', uk: '10.5', eu: '45', cm: '29' },
    { us: '12', uk: '11.5', eu: '46', cm: '30' }
  ]

  const kidsSizes = [
    { age: '2-3', height: '92-98', chest: '53-55', waist: '50-52' },
    { age: '3-4', height: '98-104', chest: '55-57', waist: '51-53' },
    { age: '4-5', height: '104-110', chest: '57-59', waist: '52-54' },
    { age: '5-6', height: '110-116', chest: '59-61', waist: '53-55' },
    { age: '6-7', height: '116-122', chest: '61-63', waist: '54-56' },
    { age: '7-8', height: '122-128', chest: '63-65', waist: '55-57' },
    { age: '8-9', height: '128-134', chest: '65-67', waist: '57-59' },
    { age: '9-10', height: '134-140', chest: '67-69', waist: '59-61' }
  ]

  return (
    <div className="pt-32 pb-16">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-display font-bold text-gray-900 mb-4">Size Guide</h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Find your perfect fit with our comprehensive size charts. All measurements are in inches unless otherwise noted.
          </p>
        </div>

        {/* Tabs */}
        <div className="flex flex-wrap justify-center gap-2 mb-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-2 rounded-full font-medium transition-colors ${
                activeTab === tab.id
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {tab.name}
            </button>
          ))}
        </div>

        {/* Size Charts */}
        <div className="max-w-4xl mx-auto">
          {/* Men's Clothing */}
          {activeTab === 'clothing' && (
            <div className="space-y-8">
              <div className="card p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Men's Tops & Shirts</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="px-4 py-3 text-left font-semibold text-gray-900">Size</th>
                        <th className="px-4 py-3 text-left font-semibold text-gray-900">Chest (in)</th>
                        <th className="px-4 py-3 text-left font-semibold text-gray-900">Waist (in)</th>
                        <th className="px-4 py-3 text-left font-semibold text-gray-900">Neck (in)</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {mensSizes.tops.map((row) => (
                        <tr key={row.size} className="hover:bg-gray-50">
                          <td className="px-4 py-3 font-medium text-gray-900">{row.size}</td>
                          <td className="px-4 py-3 text-gray-600">{row.chest}</td>
                          <td className="px-4 py-3 text-gray-600">{row.waist}</td>
                          <td className="px-4 py-3 text-gray-600">{row.neck}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="card p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Men's Pants & Jeans</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="px-4 py-3 text-left font-semibold text-gray-900">Size</th>
                        <th className="px-4 py-3 text-left font-semibold text-gray-900">Waist (in)</th>
                        <th className="px-4 py-3 text-left font-semibold text-gray-900">Hip (in)</th>
                        <th className="px-4 py-3 text-left font-semibold text-gray-900">Inseam (in)</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {mensSizes.pants.map((row) => (
                        <tr key={row.size} className="hover:bg-gray-50">
                          <td className="px-4 py-3 font-medium text-gray-900">{row.size}</td>
                          <td className="px-4 py-3 text-gray-600">{row.waist}</td>
                          <td className="px-4 py-3 text-gray-600">{row.hip}</td>
                          <td className="px-4 py-3 text-gray-600">{row.inseam}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* Women's Clothing */}
          {activeTab === 'women' && (
            <div className="card p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Women's Clothing</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="bg-gray-50">
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Size (US)</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Bust (in)</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Waist (in)</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Hip (in)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {womensSizes.tops.map((row) => (
                      <tr key={row.size} className="hover:bg-gray-50">
                        <td className="px-4 py-3 font-medium text-gray-900">{row.size}</td>
                        <td className="px-4 py-3 text-gray-600">{row.bust}</td>
                        <td className="px-4 py-3 text-gray-600">{row.waist}</td>
                        <td className="px-4 py-3 text-gray-600">{row.hip}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Shoes */}
          {activeTab === 'shoes' && (
            <div className="card p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Shoe Size Conversion</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="bg-gray-50">
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">US</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">UK</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">EU</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">CM</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {shoesSizes.map((row) => (
                      <tr key={row.us} className="hover:bg-gray-50">
                        <td className="px-4 py-3 font-medium text-gray-900">{row.us}</td>
                        <td className="px-4 py-3 text-gray-600">{row.uk}</td>
                        <td className="px-4 py-3 text-gray-600">{row.eu}</td>
                        <td className="px-4 py-3 text-gray-600">{row.cm}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Kids */}
          {activeTab === 'kids' && (
            <div className="card p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Kids' Clothing (cm)</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="bg-gray-50">
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Age (years)</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Height (cm)</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Chest (cm)</th>
                      <th className="px-4 py-3 text-left font-semibold text-gray-900">Waist (cm)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {kidsSizes.map((row) => (
                      <tr key={row.age} className="hover:bg-gray-50">
                        <td className="px-4 py-3 font-medium text-gray-900">{row.age}</td>
                        <td className="px-4 py-3 text-gray-600">{row.height}</td>
                        <td className="px-4 py-3 text-gray-600">{row.chest}</td>
                        <td className="px-4 py-3 text-gray-600">{row.waist}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>

        {/* Measuring Tips */}
        <div className="max-w-4xl mx-auto mt-12">
          <div className="card p-6 bg-primary-50 border-primary-200">
            <div className="flex items-start gap-3">
              <FiInfo className="w-6 h-6 text-primary-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">How to Measure</h3>
                <ul className="text-gray-600 space-y-1 text-sm">
                  <li>• <strong>Chest/Bust:</strong> Measure around the fullest part of your chest, keeping the tape horizontal.</li>
                  <li>• <strong>Waist:</strong> Measure around your natural waistline, keeping the tape comfortably loose.</li>
                  <li>• <strong>Hip:</strong> Measure around the fullest part of your hips and buttocks.</li>
                  <li>• <strong>Inseam:</strong> Measure from the crotch seam to the bottom of the leg.</li>
                  <li>• <strong>Foot:</strong> Stand on a piece of paper and trace around your foot. Measure the longest distance.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Contact CTA */}
        <div className="mt-12 text-center">
          <p className="text-gray-600 mb-4">Need help finding your size?</p>
          <a href="/contact" className="btn btn-primary">Contact Us</a>
        </div>
      </div>
    </div>
  )
}

export default SizeGuidePage
