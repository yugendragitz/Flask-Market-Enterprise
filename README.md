# FlaskMarket Enterprise 🛒

A production-ready, enterprise-level e-commerce platform built with Flask REST API backend and React + Tailwind CSS frontend. Features JWT authentication, GSAP animations, and a modern shopping experience similar to Amazon/Flipkart.

![FlaskMarket Banner](https://via.placeholder.com/1200x400?text=FlaskMarket+Enterprise)

## 🚀 Features

### Backend (Flask REST API)
- ✅ RESTful API architecture with Flask
- ✅ JWT-based authentication (access & refresh tokens)
- ✅ Role-based access control (Admin, Seller, Customer)
- ✅ SQLAlchemy ORM with comprehensive models
- ✅ Rate limiting and CORS support
- ✅ Environment-based configuration (Dev/Test/Prod)
- ✅ Product management with categories, images, and reviews
- ✅ Shopping cart and order management
- ✅ Wallet system and coupon support
- ✅ Admin dashboard with analytics

### Frontend (React + Vite)
- ✅ Modern React 18 with hooks
- ✅ Tailwind CSS for styling
- ✅ GSAP animations for smooth interactions
- ✅ React Query for data fetching
- ✅ Zustand for state management
- ✅ Responsive design (mobile-first)
- ✅ Beautiful UI components
- ✅ Toast notifications

## 📁 Project Structure

```
FlaskMarket-Enterprise/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Application factory
│   │   ├── config.py            # Configuration classes
│   │   ├── extensions.py        # Flask extensions
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py      # Authentication endpoints
│   │   │       ├── products.py  # Products API
│   │   │       ├── cart.py      # Cart API
│   │   │       ├── orders.py    # Orders API
│   │   │       ├── users.py     # Users API
│   │   │       └── admin.py     # Admin API
│   │   ├── models/
│   │   │   ├── user.py          # User & Address models
│   │   │   ├── product.py       # Product, Category, Review models
│   │   │   └── order.py         # Cart, Order, Transaction models
│   │   └── utils/
│   │       ├── decorators.py    # Custom decorators
│   │       └── helpers.py       # Helper functions
│   ├── run.py                   # Entry point
│   ├── seed.py                  # Database seeder
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment template
│
└── frontend/
    ├── src/
    │   ├── components/          # Reusable components
    │   │   ├── Header.jsx
    │   │   ├── Footer.jsx
    │   │   └── ProductCard.jsx
    │   ├── pages/               # Page components
    │   │   ├── HomePage.jsx
    │   │   ├── ProductsPage.jsx
    │   │   ├── ProductDetailPage.jsx
    │   │   ├── CartPage.jsx
    │   │   ├── LoginPage.jsx
    │   │   └── RegisterPage.jsx
    │   ├── store/               # Zustand stores
    │   │   ├── authStore.js
    │   │   └── cartStore.js
    │   ├── services/            # API services
    │   │   └── api.js
    │   ├── layouts/
    │   │   └── MainLayout.jsx
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── index.html
```

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd FlaskMarket-Enterprise/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create environment file:
```bash
cp .env.example .env
```

6. Edit `.env` with your settings:
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///flaskmarket.db
```

7. Initialize and seed the database:
```bash
# Initialize database
flask init-db

# Seed with sample data
flask seed-db
```

8. Run the backend server:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd FlaskMarket-Enterprise/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login user |
| POST | `/api/v1/auth/logout` | Logout user |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/auth/me` | Get current user |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/products` | List all products |
| GET | `/api/v1/products/:slug` | Get product details |
| GET | `/api/v1/products/search` | Search products |
| GET | `/api/v1/products/featured` | Get featured products |
| GET | `/api/v1/categories` | List categories |

### Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/cart` | Get cart items |
| POST | `/api/v1/cart/items` | Add item to cart |
| PUT | `/api/v1/cart/items/:id` | Update item quantity |
| DELETE | `/api/v1/cart/items/:id` | Remove item |
| DELETE | `/api/v1/cart` | Clear cart |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/orders` | List user orders |
| GET | `/api/v1/orders/:id` | Get order details |
| POST | `/api/v1/orders/checkout` | Create order |
| POST | `/api/v1/orders/:id/cancel` | Cancel order |

### Admin (Admin only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/admin/dashboard` | Dashboard stats |
| POST | `/api/v1/admin/products` | Create product |
| PUT | `/api/v1/admin/products/:id` | Update product |
| DELETE | `/api/v1/admin/products/:id` | Delete product |

## 🔐 Default Users

After seeding, you can use these accounts:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@flaskmarket.com | Admin@123 |
| Customer | john@example.com | User@123 |
| Seller | bob@example.com | User@123 |

## 🎨 Tech Stack

### Backend
- **Flask** - Web framework
- **Flask-JWT-Extended** - JWT authentication
- **Flask-SQLAlchemy** - ORM
- **Flask-Marshmallow** - Serialization
- **Flask-CORS** - Cross-origin support
- **Flask-Limiter** - Rate limiting

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **GSAP** - Animations
- **React Query** - Data fetching
- **Zustand** - State management
- **React Router** - Routing
- **Axios** - HTTP client

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | development |
| `SECRET_KEY` | Flask secret key | - |
| `JWT_SECRET_KEY` | JWT secret | - |
| `DATABASE_URL` | Database URL | sqlite:///flaskmarket.db |
| `JWT_ACCESS_TOKEN_EXPIRES` | Access token expiry (seconds) | 3600 |
| `JWT_REFRESH_TOKEN_EXPIRES` | Refresh token expiry (seconds) | 2592000 |

## 🚀 Deployment

### Production Build

**Backend:**
```bash
# Set production environment
export FLASK_ENV=production

# Use gunicorn for production
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

**Frontend:**
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 📄 License

MIT License - feel free to use this project for your own purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Built with ❤️ by FlaskMarket Team
