import { useState, useEffect } from 'react'
import { useSearchParams, useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { FiFilter, FiX, FiChevronDown, FiGrid, FiList } from 'react-icons/fi'
import clsx from 'clsx'
import ProductCard from '../components/ProductCard'
import { productsAPI, categoriesAPI } from '../services/api'

const ProductsPage = () => {
  const [searchParams, setSearchParams] = useSearchParams()
  const { slug: categorySlug } = useParams()
  const navigate = useNavigate()
  
  const [isFilterOpen, setIsFilterOpen] = useState(false)
  const [viewMode, setViewMode] = useState('grid')
  
  // Get filter values from URL
  const page = parseInt(searchParams.get('page') || '1')
  const search = searchParams.get('search') || ''
  const sortBy = searchParams.get('sort') || 'newest'
  const minPrice = searchParams.get('min_price') || ''
  const maxPrice = searchParams.get('max_price') || ''
  // Use URL slug as the primary category source
  const selectedCategory = categorySlug || ''

  // Fetch products
  const { data: productsData, isLoading: productsLoading } = useQuery({
    queryKey: ['products', { page, search, sortBy, minPrice, maxPrice, selectedCategory }],
    queryFn: async () => {
      const params = {
        page,
        per_page: 12,
        search: search || undefined,
        sort: sortBy,
        min_price: minPrice || undefined,
        max_price: maxPrice || undefined,
        category: selectedCategory ? selectedCategory : undefined,
      }
      const response = await productsAPI.getAll(params)
      return response.data.data
    },
  })

  // Fetch categories for filter
  const { data: categoriesData } = useQuery({
    queryKey: ['categories'],
    queryFn: async () => {
      const response = await categoriesAPI.getAll()
      return response.data.data?.categories || response.data.data || []
    },
  })

  const products = productsData?.products || productsData?.items || []
  const pagination = productsData?.pagination || {}
  const categories = categoriesData || []

  // Update filters
  const updateFilter = (key, value) => {
    // If changing category, always use URL navigation for consistency
    if (key === 'category') {
      if (value) {
        navigate(`/category/${value}`)
      } else {
        navigate('/products')
      }
      return
    }
    
    const newParams = new URLSearchParams(searchParams)
    if (value) {
      newParams.set(key, value)
    } else {
      newParams.delete(key)
    }
    if (key !== 'page') {
      newParams.set('page', '1') // Reset to first page when changing other filters
    }
    setSearchParams(newParams)
  }

  // Clear all filters
  const clearFilters = () => {
    if (categorySlug) {
      navigate('/products')
    } else {
      setSearchParams({ page: '1' })
    }
  }

  const sortOptions = [
    { value: 'newest', label: 'Newest First' },
    { value: 'price_asc', label: 'Price: Low to High' },
    { value: 'price_desc', label: 'Price: High to Low' },
    { value: 'rating', label: 'Highest Rated' },
    { value: 'popular', label: 'Most Popular' },
  ]

  return (
    <div className="pt-32 pb-16">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-display font-bold text-gray-900">
            {selectedCategory
              ? categories.find(c => c.slug === selectedCategory)?.name || 'Products'
              : search
              ? `Search results for "${search}"`
              : 'All Products'}
          </h1>
          <p className="text-gray-500 mt-1">
            {pagination.total_items || products.length} products found
          </p>
        </div>

        <div className="flex gap-8">
          {/* Sidebar Filters - Desktop */}
          <aside className="hidden lg:block w-64 flex-shrink-0">
            <div className="sticky top-32 space-y-6">
              {/* Categories */}
              <div className="card p-4">
                <h3 className="font-semibold text-gray-900 mb-3">Categories</h3>
                <div className="space-y-2">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="radio"
                      name="category"
                      checked={!selectedCategory}
                      onChange={() => updateFilter('category', '')}
                      className="text-primary-600 focus:ring-primary-500"
                    />
                    <span className="text-sm text-gray-600">All Categories</span>
                  </label>
                  {categories.map((category) => (
                    <label
                      key={category.id}
                      className="flex items-center gap-2 cursor-pointer"
                    >
                      <input
                        type="radio"
                        name="category"
                        checked={selectedCategory === category.slug}
                        onChange={() => updateFilter('category', category.slug)}
                        className="text-primary-600 focus:ring-primary-500"
                      />
                      <span className="text-sm text-gray-600">{category.name}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Price Range */}
              <div className="card p-4">
                <h3 className="font-semibold text-gray-900 mb-3">Price Range</h3>
                <div className="flex items-center gap-2">
                  <input
                    type="number"
                    placeholder="Min"
                    value={minPrice}
                    onChange={(e) => updateFilter('min_price', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                  <span className="text-gray-400">-</span>
                  <input
                    type="number"
                    placeholder="Max"
                    value={maxPrice}
                    onChange={(e) => updateFilter('max_price', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
              </div>

              {/* Clear Filters */}
              {(selectedCategory || minPrice || maxPrice || search) && (
                <button
                  onClick={clearFilters}
                  className="w-full btn btn-outline text-sm"
                >
                  Clear All Filters
                </button>
              )}
            </div>
          </aside>

          {/* Main Content */}
          <div className="flex-1">
            {/* Toolbar */}
            <div className="flex items-center justify-between gap-4 mb-6 pb-4 border-b">
              {/* Mobile filter button */}
              <button
                onClick={() => setIsFilterOpen(true)}
                className="lg:hidden btn btn-outline btn-sm"
              >
                <FiFilter className="w-4 h-4 mr-2" />
                Filters
              </button>

              {/* Sort dropdown */}
              <div className="flex items-center gap-2">
                <span className="hidden sm:block text-sm text-gray-500">Sort by:</span>
                <div className="relative">
                  <select
                    value={sortBy}
                    onChange={(e) => updateFilter('sort', e.target.value)}
                    className="appearance-none px-4 py-2 pr-10 bg-white border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    {sortOptions.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                  <FiChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
                </div>
              </div>

              {/* View mode toggle */}
              <div className="hidden sm:flex items-center gap-1 bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('grid')}
                  className={clsx(
                    'p-2 rounded-md transition-colors',
                    viewMode === 'grid'
                      ? 'bg-white shadow text-primary-600'
                      : 'text-gray-400 hover:text-gray-600'
                  )}
                >
                  <FiGrid className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={clsx(
                    'p-2 rounded-md transition-colors',
                    viewMode === 'list'
                      ? 'bg-white shadow text-primary-600'
                      : 'text-gray-400 hover:text-gray-600'
                  )}
                >
                  <FiList className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Products Grid */}
            {productsLoading ? (
              <div
                className={clsx(
                  'grid gap-4 md:gap-6',
                  viewMode === 'grid'
                    ? 'grid-cols-2 md:grid-cols-3'
                    : 'grid-cols-1'
                )}
              >
                {[...Array(12)].map((_, i) => (
                  <div key={i} className="card">
                    <div className="aspect-square skeleton" />
                    <div className="p-4 space-y-3">
                      <div className="h-4 skeleton w-1/3" />
                      <div className="h-5 skeleton" />
                      <div className="h-4 skeleton w-2/3" />
                      <div className="h-6 skeleton w-1/2" />
                    </div>
                  </div>
                ))}
              </div>
            ) : products.length > 0 ? (
              <div
                className={clsx(
                  'grid gap-4 md:gap-6',
                  viewMode === 'grid'
                    ? 'grid-cols-2 md:grid-cols-3'
                    : 'grid-cols-1'
                )}
              >
                {products.map((product, index) => (
                  <ProductCard
                    key={product.id}
                    product={product}
                    index={index}
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-16">
                <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FiFilter className="w-10 h-10 text-gray-400" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900">No products found</h3>
                <p className="text-gray-500 mt-2">
                  Try adjusting your filters or search terms
                </p>
                <button
                  onClick={clearFilters}
                  className="btn btn-primary mt-4"
                >
                  Clear Filters
                </button>
              </div>
            )}

            {/* Pagination */}
            {pagination.total_pages > 1 && (
              <div className="flex items-center justify-center gap-2 mt-10">
                <button
                  onClick={() => updateFilter('page', Math.max(1, page - 1).toString())}
                  disabled={page <= 1}
                  className="btn btn-outline btn-sm disabled:opacity-50"
                >
                  Previous
                </button>
                
                {[...Array(Math.min(5, pagination.total_pages))].map((_, i) => {
                  const pageNum = i + 1
                  return (
                    <button
                      key={pageNum}
                      onClick={() => updateFilter('page', pageNum.toString())}
                      className={clsx(
                        'btn btn-sm',
                        page === pageNum
                          ? 'btn-primary'
                          : 'btn-outline'
                      )}
                    >
                      {pageNum}
                    </button>
                  )
                })}
                
                <button
                  onClick={() => updateFilter('page', Math.min(pagination.total_pages, page + 1).toString())}
                  disabled={page >= pagination.total_pages}
                  className="btn btn-outline btn-sm disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Mobile Filter Drawer */}
        {isFilterOpen && (
          <div className="lg:hidden fixed inset-0 z-50">
            <div
              className="absolute inset-0 bg-black/50"
              onClick={() => setIsFilterOpen(false)}
            />
            <div className="absolute right-0 top-0 bottom-0 w-80 bg-white shadow-xl animate-slide-left">
              <div className="flex items-center justify-between p-4 border-b">
                <h3 className="font-semibold text-gray-900">Filters</h3>
                <button
                  onClick={() => setIsFilterOpen(false)}
                  className="p-2 hover:bg-gray-100 rounded-full"
                >
                  <FiX className="w-5 h-5" />
                </button>
              </div>
              <div className="p-4 space-y-6 overflow-y-auto max-h-[calc(100vh-64px)]">
                {/* Categories */}
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Categories</h4>
                  <div className="space-y-2">
                    {categories.map((category) => (
                      <label
                        key={category.id}
                        className="flex items-center gap-2"
                      >
                        <input
                          type="radio"
                          name="mobile-category"
                          checked={selectedCategory === category.slug}
                          onChange={() => {
                            updateFilter('category', category.slug)
                            setIsFilterOpen(false)
                          }}
                          className="text-primary-600"
                        />
                        <span className="text-sm text-gray-600">{category.name}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Price Range */}
                <div>
                  <h4 className="font-medium text-gray-900 mb-3">Price Range</h4>
                  <div className="flex items-center gap-2">
                    <input
                      type="number"
                      placeholder="Min"
                      value={minPrice}
                      onChange={(e) => updateFilter('min_price', e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg text-sm"
                    />
                    <span>-</span>
                    <input
                      type="number"
                      placeholder="Max"
                      value={maxPrice}
                      onChange={(e) => updateFilter('max_price', e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg text-sm"
                    />
                  </div>
                </div>

                <button
                  onClick={() => {
                    clearFilters()
                    setIsFilterOpen(false)
                  }}
                  className="w-full btn btn-outline"
                >
                  Clear All Filters
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ProductsPage
