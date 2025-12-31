"""
FlaskMarket Enterprise - Database Seeder
Seeds the database with comprehensive sample data
"""

from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models.user import User, Address
from app.models.product import Product, Category, ProductImage, Review
from app.models.order import Coupon


def seed_database():
    """Seed all data"""
    print('🌱 Starting database seeding...')

    # Clear existing data (in order due to foreign keys)
    print('🗑️  Clearing existing data...')
    db.session.query(Review).delete()
    db.session.query(ProductImage).delete()
    # Clear the association table first
    db.session.execute(db.text('DELETE FROM product_categories'))
    db.session.query(Product).delete()
    db.session.query(Category).delete()
    db.session.query(Address).delete()
    db.session.query(Coupon).delete()
    db.session.commit()

    # Keep existing users or create admin
    admin = User.query.filter_by(email='admin@flaskmarket.com').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@flaskmarket.com',
            role='admin',
            is_verified=True,
            wallet_balance=100000
        )
        admin.set_password('Admin@123')
        db.session.add(admin)

    # Create regular users
    user_data = [
        ('john_doe', 'john@example.com', 'customer', 5000),
        ('jane_smith', 'jane@example.com', 'customer', 7500),
    ]

    for username, email, role, balance in user_data:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                username=username,
                email=email,
                role=role,
                is_verified=True,
                wallet_balance=balance
            )
            user.set_password('User@123')
            db.session.add(user)

    db.session.commit()
    print('✅ Users created')

    # Create Categories with icons
    categories_data = [
        ('Electronics', 'electronics', 'Latest gadgets and electronic devices', 'https://picsum.photos/seed/1/400/400', 'laptop'),
        ('Smartphones', 'smartphones', 'Latest mobile phones and accessories', 'https://picsum.photos/seed/2/400/400', 'smartphone'),
        ('Laptops', 'laptops', 'Powerful laptops for work and gaming', 'https://picsum.photos/seed/3/400/400', 'laptop'),
        ('Fashion', 'fashion', 'Trendy clothing and accessories', 'https://picsum.photos/seed/4/400/400', 'shirt'),
        ('Home & Kitchen', 'home-kitchen', 'Everything for your home', 'https://picsum.photos/seed/5/400/400', 'home'),
        ('Books', 'books', 'Books across all genres', 'https://picsum.photos/seed/6/400/400', 'book'),
        ('Gaming', 'gaming', 'Gaming consoles and accessories', 'https://picsum.photos/seed/7/400/400', 'gamepad'),
        ('Sports & Fitness', 'sports-fitness', 'Sports equipment and fitness gear', 'https://picsum.photos/seed/8/400/400', 'dumbbell'),
        ('Beauty & Personal Care', 'beauty', 'Skincare, makeup, and grooming', 'https://picsum.photos/seed/9/400/400', 'sparkles'),
        ('Watches', 'watches', 'Premium watches and smartwatches', 'https://picsum.photos/seed/10/400/400', 'watch'),
    ]

    categories = {}
    for name, slug, description, image_url, icon in categories_data:
        category = Category(
            name=name,
            slug=slug,
            description=description,
            image_url=image_url,
            icon=icon,
            is_active=True
        )
        db.session.add(category)
        categories[slug] = category

    db.session.commit()
    print('✅ Categories created')

    # Comprehensive Products Data
    products_data = [
        # ============ SMARTPHONES ============
        {
            'name': 'iPhone 15 Pro Max',
            'slug': 'iphone-15-pro-max',
            'sku': 'APL-IP15PM-256',
            'short_description': 'The most powerful iPhone ever with A17 Pro chip',
            'description': 'Experience the pinnacle of smartphone technology with iPhone 15 Pro Max. Featuring the A17 Pro chip, titanium design, and 48MP camera system.',
            'price': 1199.00,
            'compare_price': 1299.00,
            'stock_quantity': 50,
            'thumbnail_url': 'https://images.unsplash.com/photo-1697120531506-c1f0db3ce0a0?w=800&h=800&fit=crop',
            'brand': 'Apple',
            'is_featured': True,
            'is_new': True,
            'category': 'smartphones'
        },
        {
            'name': 'Samsung Galaxy S24 Ultra',
            'slug': 'samsung-galaxy-s24-ultra',
            'sku': 'SAM-S24U-512',
            'short_description': 'Galaxy AI is here. The most powerful Galaxy yet.',
            'description': 'Meet Galaxy S24 Ultra with AI, S Pen, and 200MP camera. Titanium frame and stunning display.',
            'price': 1299.99,
            'compare_price': 1399.99,
            'stock_quantity': 45,
            'thumbnail_url': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=800&h=800&fit=crop',
            'brand': 'Samsung',
            'is_featured': True,
            'is_new': True,
            'category': 'smartphones'
        },
        {
            'name': 'Google Pixel 8 Pro',
            'slug': 'google-pixel-8-pro',
            'sku': 'GOO-PX8P-256',
            'short_description': 'The best of Google AI in a premium phone',
            'description': 'Google Pixel 8 Pro with Tensor G3 chip, advanced AI features, and exceptional camera capabilities.',
            'price': 999.00,
            'compare_price': 1099.00,
            'stock_quantity': 60,
            'thumbnail_url': 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&h=800&fit=crop',
            'brand': 'Google',
            'is_featured': True,
            'category': 'smartphones'
        },
        {
            'name': 'OnePlus 12',
            'slug': 'oneplus-12',
            'sku': 'OP-12-256',
            'short_description': 'Flagship killer with Snapdragon 8 Gen 3',
            'description': 'OnePlus 12 with Hasselblad camera, 100W charging, and buttery smooth display.',
            'price': 799.00,
            'compare_price': 899.00,
            'stock_quantity': 70,
            'thumbnail_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&h=800&fit=crop',
            'brand': 'OnePlus',
            'is_new': True,
            'category': 'smartphones'
        },
        {
            'name': 'iPhone 15',
            'slug': 'iphone-15',
            'sku': 'APL-IP15-128',
            'short_description': 'Dynamic Island comes to iPhone 15',
            'description': 'iPhone 15 with A16 Bionic chip, Dynamic Island, and USB-C. The perfect everyday iPhone.',
            'price': 799.00,
            'compare_price': 899.00,
            'stock_quantity': 80,
            'thumbnail_url': 'https://images.unsplash.com/photo-1592286927505-4fd09de0574e?w=800&h=800&fit=crop',
            'brand': 'Apple',
            'category': 'smartphones'
        },

        # ============ LAPTOPS ============
        {
            'name': 'MacBook Pro 16" M3 Max',
            'slug': 'macbook-pro-16-m3-max',
            'sku': 'APL-MBP16-M3MAX',
            'short_description': 'The most advanced Mac laptops for demanding workflows',
            'description': 'MacBook Pro with M3 Max chip delivers extraordinary performance. Up to 128GB unified memory and stunning Liquid Retina XDR display.',
            'price': 3499.00,
            'compare_price': 3699.00,
            'stock_quantity': 25,
            'thumbnail_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&h=600&fit=crop',
            'brand': 'Apple',
            'is_featured': True,
            'category': 'laptops'
        },
        {
            'name': 'Dell XPS 15',
            'slug': 'dell-xps-15',
            'sku': 'DEL-XPS15-I7',
            'short_description': 'Stunning 15.6" OLED display with Intel Core i7',
            'description': 'The Dell XPS 15 combines power and portability with 3.5K OLED display and NVIDIA RTX graphics.',
            'price': 1899.99,
            'compare_price': 2099.99,
            'stock_quantity': 35,
            'thumbnail_url': 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&h=600&fit=crop',
            'brand': 'Dell',
            'is_new': True,
            'category': 'laptops'
        },
        {
            'name': 'MacBook Air M3',
            'slug': 'macbook-air-m3',
            'sku': 'APL-MBA-M3',
            'short_description': 'Supercharged by M3. Strikingly thin.',
            'description': 'MacBook Air with M3 chip. Fanless design, all-day battery, and stunning Liquid Retina display.',
            'price': 1099.00,
            'compare_price': 1199.00,
            'stock_quantity': 60,
            'thumbnail_url': 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800&h=600&fit=crop',
            'brand': 'Apple',
            'is_featured': True,
            'category': 'laptops'
        },
        {
            'name': 'ASUS ROG Zephyrus G14',
            'slug': 'asus-rog-zephyrus-g14',
            'sku': 'ASUS-ROG-G14',
            'short_description': 'Compact gaming powerhouse with AMD Ryzen 9',
            'description': 'ROG Zephyrus G14 with AMD Ryzen 9, RTX 4090, and AniMe Matrix display.',
            'price': 1999.99,
            'compare_price': 2199.99,
            'stock_quantity': 30,
            'thumbnail_url': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&h=600&fit=crop',
            'brand': 'ASUS',
            'is_featured': True,
            'category': 'laptops'
        },
        {
            'name': 'HP Spectre x360',
            'slug': 'hp-spectre-x360',
            'sku': 'HP-SPECTRE-X360',
            'short_description': '2-in-1 convertible with OLED display',
            'description': 'HP Spectre x360 with Intel Evo platform, OLED display, and premium gem-cut design.',
            'price': 1649.99,
            'compare_price': 1849.99,
            'stock_quantity': 40,
            'thumbnail_url': 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&h=600&fit=crop',
            'brand': 'HP',
            'category': 'laptops'
        },

        # ============ ELECTRONICS ============
        {
            'name': 'Sony WH-1000XM5',
            'slug': 'sony-wh-1000xm5',
            'sku': 'SNY-WH1000XM5-BLK',
            'short_description': 'Industry-leading noise cancellation headphones',
            'description': 'The best noise canceling with 8 microphones. 30-hour battery and multipoint connection.',
            'price': 349.99,
            'compare_price': 399.99,
            'stock_quantity': 100,
            'thumbnail_url': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&h=600&fit=crop',
            'brand': 'Sony',
            'is_featured': True,
            'category': 'electronics'
        },
        {
            'name': 'AirPods Pro 2nd Gen',
            'slug': 'airpods-pro-2',
            'sku': 'APL-APP2-USB',
            'short_description': 'Rebuilt from the sound up with Apple H2 chip',
            'description': 'AirPods Pro with H2 chip, Adaptive Audio, and USB-C charging case.',
            'price': 249.00,
            'compare_price': 279.00,
            'stock_quantity': 120,
            'thumbnail_url': 'https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=800&h=600&fit=crop',
            'brand': 'Apple',
            'is_featured': True,
            'category': 'electronics'
        },
        {
            'name': 'Samsung 65" OLED 4K TV',
            'slug': 'samsung-65-oled-4k',
            'sku': 'SAM-TV65-OLED',
            'short_description': 'Stunning OLED display with infinite contrast',
            'description': 'Samsung S95D OLED with Neural Quantum Processor, Dolby Atmos, and Gaming Hub.',
            'price': 2499.99,
            'compare_price': 2999.99,
            'stock_quantity': 20,
            'thumbnail_url': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800&h=600&fit=crop',
            'brand': 'Samsung',
            'is_featured': True,
            'category': 'electronics'
        },
        {
            'name': 'Bose QuietComfort Ultra',
            'slug': 'bose-quietcomfort-ultra',
            'sku': 'BOSE-QC-ULTRA',
            'short_description': 'Immersive audio with world-class noise cancellation',
            'description': 'Bose QuietComfort Ultra with Immersive Audio and CustomTune technology.',
            'price': 429.00,
            'compare_price': 479.00,
            'stock_quantity': 75,
            'thumbnail_url': 'https://images.unsplash.com/photo-1545127398-14699f92334b?w=800&h=600&fit=crop',
            'brand': 'Bose',
            'is_new': True,
            'category': 'electronics'
        },
        {
            'name': 'JBL Charge 5',
            'slug': 'jbl-charge-5',
            'sku': 'JBL-CHARGE5-BLK',
            'short_description': 'Portable Bluetooth speaker with powerbank',
            'description': 'JBL Charge 5 with 20 hours playtime, IP67 waterproof, and PartyBoost.',
            'price': 179.99,
            'compare_price': 199.99,
            'stock_quantity': 90,
            'thumbnail_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&h=600&fit=crop',
            'brand': 'JBL',
            'category': 'electronics'
        },
        {
            'name': 'Apple HomePod mini',
            'slug': 'apple-homepod-mini',
            'sku': 'APL-HPM-WHT',
            'short_description': 'Big sound in a compact smart speaker',
            'description': 'HomePod mini with Siri, computational audio, and smart home hub.',
            'price': 99.00,
            'compare_price': 119.00,
            'stock_quantity': 150,
            'thumbnail_url': 'https://images.unsplash.com/photo-1589492477829-5e65395b66cc?w=800&h=600&fit=crop',
            'brand': 'Apple',
            'category': 'electronics'
        },

        # ============ GAMING ============
        {
            'name': 'PlayStation 5',
            'slug': 'playstation-5',
            'sku': 'SNY-PS5-STD',
            'short_description': 'Experience lightning-fast loading with ultra-high speed SSD',
            'description': 'PlayStation 5 with haptic feedback, adaptive triggers, and 3D Audio technology.',
            'price': 499.99,
            'compare_price': 549.99,
            'stock_quantity': 30,
            'thumbnail_url': 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=800&h=600&fit=crop',
            'brand': 'Sony',
            'is_featured': True,
            'category': 'gaming'
        },
        {
            'name': 'Nintendo Switch OLED',
            'slug': 'nintendo-switch-oled',
            'sku': 'NTD-SW-OLED',
            'short_description': 'Vibrant 7-inch OLED screen with enhanced audio',
            'description': 'Nintendo Switch OLED with 7-inch OLED screen and wide adjustable stand.',
            'price': 349.99,
            'compare_price': 379.99,
            'stock_quantity': 55,
            'thumbnail_url': 'https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=800&h=600&fit=crop',
            'brand': 'Nintendo',
            'is_featured': True,
            'category': 'gaming'
        },
        {
            'name': 'Xbox Series X',
            'slug': 'xbox-series-x',
            'sku': 'MS-XSX-1TB',
            'short_description': 'The fastest, most powerful Xbox ever',
            'description': 'Xbox Series X with 12 teraflops, Quick Resume, and Smart Delivery.',
            'price': 499.99,
            'compare_price': 549.99,
            'stock_quantity': 40,
            'thumbnail_url': 'https://images.unsplash.com/photo-1621259182978-fbf93132d53d?w=800&h=600&fit=crop',
            'brand': 'Microsoft',
            'is_featured': True,
            'category': 'gaming'
        },
        {
            'name': 'Steam Deck OLED',
            'slug': 'steam-deck-oled',
            'sku': 'VALVE-SD-OLED',
            'short_description': 'Your PC gaming library in your hands',
            'description': 'Steam Deck OLED with HDR display, longer battery, and faster downloads.',
            'price': 549.00,
            'compare_price': 649.00,
            'stock_quantity': 35,
            'thumbnail_url': 'https://images.unsplash.com/photo-1625805866449-3589fe3f71a3?w=800&h=600&fit=crop',
            'brand': 'Valve',
            'is_new': True,
            'category': 'gaming'
        },
        {
            'name': 'Razer BlackShark V2 Pro',
            'slug': 'razer-blackshark-v2-pro',
            'sku': 'RZR-BSV2P-BLK',
            'short_description': 'Wireless esports headset with THX Audio',
            'description': 'Razer BlackShark V2 Pro with TriForce titanium drivers and HyperClear mic.',
            'price': 179.99,
            'compare_price': 199.99,
            'stock_quantity': 80,
            'thumbnail_url': 'https://images.unsplash.com/photo-1599669454699-248893623440?w=800&h=600&fit=crop',
            'brand': 'Razer',
            'category': 'gaming'
        },

        # ============ FASHION ============
        {
            'name': 'Nike Air Max 270',
            'slug': 'nike-air-max-270',
            'sku': 'NKE-AM270-BLK',
            'short_description': 'Maximum Air for the lifestyle',
            'description': 'Nike Air Max 270 with the largest heel Air unit yet for all-day cushioning.',
            'price': 150.00,
            'compare_price': 170.00,
            'stock_quantity': 80,
            'thumbnail_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&h=800&fit=crop',
            'brand': 'Nike',
            'is_featured': True,
            'category': 'fashion'
        },
        {
            'name': 'Adidas Ultraboost 23',
            'slug': 'adidas-ultraboost-23',
            'sku': 'ADI-UB23-WHT',
            'short_description': 'Incredible energy return with BOOST midsole',
            'description': 'Adidas Ultraboost with Linear Energy Push and Continental rubber outsole.',
            'price': 190.00,
            'compare_price': 210.00,
            'stock_quantity': 65,
            'thumbnail_url': 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=800&h=800&fit=crop',
            'brand': 'Adidas',
            'is_featured': True,
            'category': 'fashion'
        },
        {
            'name': 'Levi\'s 501 Original Jeans',
            'slug': 'levis-501-original',
            'sku': 'LVS-501-BLU',
            'short_description': 'The original button fly jean since 1873',
            'description': 'Levi\'s 501 Original Fit with signature straight leg and button fly.',
            'price': 69.50,
            'compare_price': 89.50,
            'stock_quantity': 120,
            'thumbnail_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&h=800&fit=crop',
            'brand': 'Levi\'s',
            'category': 'fashion'
        },
        {
            'name': 'Ray-Ban Aviator Classic',
            'slug': 'rayban-aviator-classic',
            'sku': 'RB-AVIATOR-GLD',
            'short_description': 'Iconic pilot sunglasses since 1937',
            'description': 'Ray-Ban Aviator with crystal green G-15 lenses and gold metal frame.',
            'price': 169.00,
            'compare_price': 199.00,
            'stock_quantity': 90,
            'thumbnail_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&h=600&fit=crop',
            'brand': 'Ray-Ban',
            'is_featured': True,
            'category': 'fashion'
        },
        {
            'name': 'The North Face Puffer Jacket',
            'slug': 'north-face-puffer',
            'sku': 'TNF-PUFFER-BLK',
            'short_description': 'Classic warmth with 700-fill down',
            'description': 'The North Face 1996 Retro Nuptse with water-resistant finish.',
            'price': 320.00,
            'compare_price': 380.00,
            'stock_quantity': 45,
            'thumbnail_url': 'https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=800&h=800&fit=crop',
            'brand': 'The North Face',
            'is_new': True,
            'category': 'fashion'
        },

        # ============ HOME & KITCHEN ============
        {
            'name': 'Dyson V15 Detect',
            'slug': 'dyson-v15-detect',
            'sku': 'DYS-V15-DET',
            'short_description': 'Reveals hidden dust with a precisely-angled laser',
            'description': 'Dyson V15 Detect with piezo sensor that counts and sizes dust particles.',
            'price': 749.99,
            'compare_price': 849.99,
            'stock_quantity': 40,
            'thumbnail_url': 'https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800&h=600&fit=crop',
            'brand': 'Dyson',
            'is_featured': True,
            'category': 'home-kitchen'
        },
        {
            'name': 'Nespresso Vertuo Next',
            'slug': 'nespresso-vertuo-next',
            'sku': 'NSP-VERTUO-BLK',
            'short_description': 'Barista-grade coffee at home',
            'description': 'Nespresso Vertuo Next with Centrifusion technology for perfect crema.',
            'price': 179.00,
            'compare_price': 219.00,
            'stock_quantity': 70,
            'thumbnail_url': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800&h=600&fit=crop',
            'brand': 'Nespresso',
            'is_featured': True,
            'category': 'home-kitchen'
        },
        {
            'name': 'Instant Pot Duo 7-in-1',
            'slug': 'instant-pot-duo',
            'sku': 'IP-DUO-6QT',
            'short_description': 'Pressure cooker, slow cooker, and more',
            'description': 'Instant Pot Duo 7-in-1 electric pressure cooker with 6-quart capacity.',
            'price': 89.99,
            'compare_price': 119.99,
            'stock_quantity': 100,
            'thumbnail_url': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=800&h=600&fit=crop',
            'brand': 'Instant Pot',
            'category': 'home-kitchen'
        },
        {
            'name': 'KitchenAid Stand Mixer',
            'slug': 'kitchenaid-stand-mixer',
            'sku': 'KA-MIXER-RED',
            'short_description': 'Iconic stand mixer with 10 speeds',
            'description': 'KitchenAid Artisan 5-quart stand mixer with tilt-head design.',
            'price': 449.99,
            'compare_price': 499.99,
            'stock_quantity': 35,
            'thumbnail_url': 'https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=800&h=600&fit=crop',
            'brand': 'KitchenAid',
            'is_featured': True,
            'category': 'home-kitchen'
        },
        {
            'name': 'Philips Air Fryer XXL',
            'slug': 'philips-air-fryer-xxl',
            'sku': 'PHL-AF-XXL',
            'short_description': 'Healthier fried food with Rapid Air',
            'description': 'Philips Airfryer XXL with fat removal technology and 3lb capacity.',
            'price': 299.99,
            'compare_price': 349.99,
            'stock_quantity': 55,
            'thumbnail_url': 'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&h=600&fit=crop',
            'brand': 'Philips',
            'is_new': True,
            'category': 'home-kitchen'
        },

        # ============ BOOKS ============
        {
            'name': 'Atomic Habits',
            'slug': 'atomic-habits-book',
            'sku': 'BK-ATOMIC-HB',
            'short_description': 'Tiny Changes, Remarkable Results by James Clear',
            'description': 'Atomic Habits is the most comprehensive guide on how to change your habits. #1 NYT Bestseller.',
            'price': 18.99,
            'compare_price': 27.00,
            'stock_quantity': 200,
            'thumbnail_url': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=600&h=800&fit=crop',
            'brand': 'Random House',
            'is_featured': True,
            'category': 'books'
        },
        {
            'name': 'The Psychology of Money',
            'slug': 'psychology-of-money',
            'sku': 'BK-PSYMONEY',
            'short_description': 'Timeless lessons on wealth by Morgan Housel',
            'description': 'The Psychology of Money explores the strange ways people think about money.',
            'price': 16.99,
            'compare_price': 24.00,
            'stock_quantity': 180,
            'thumbnail_url': 'https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=600&h=800&fit=crop',
            'brand': 'Harriman House',
            'is_featured': True,
            'category': 'books'
        },
        {
            'name': 'Deep Work',
            'slug': 'deep-work-book',
            'sku': 'BK-DEEPWORK',
            'short_description': 'Rules for Focused Success by Cal Newport',
            'description': 'Deep Work: Rules for Focused Success in a Distracted World.',
            'price': 17.99,
            'compare_price': 26.00,
            'stock_quantity': 150,
            'thumbnail_url': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=600&h=800&fit=crop',
            'brand': 'Grand Central',
            'category': 'books'
        },
        {
            'name': 'Think and Grow Rich',
            'slug': 'think-grow-rich',
            'sku': 'BK-THINKRICH',
            'short_description': 'Napoleon Hill\'s timeless classic',
            'description': 'Think and Grow Rich - the classic that has inspired millions.',
            'price': 12.99,
            'compare_price': 18.00,
            'stock_quantity': 220,
            'thumbnail_url': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=600&h=800&fit=crop',
            'brand': 'TarcherPerigee',
            'category': 'books'
        },

        # ============ SPORTS & FITNESS ============
        {
            'name': 'Yoga Mat Premium',
            'slug': 'yoga-mat-premium',
            'sku': 'FIT-YOGA-MAT',
            'short_description': 'Extra thick, non-slip yoga mat',
            'description': 'Premium yoga mat with extra cushioning for joint protection. Eco-friendly TPE material.',
            'price': 49.99,
            'compare_price': 69.99,
            'stock_quantity': 150,
            'thumbnail_url': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800&h=600&fit=crop',
            'brand': 'FitLife',
            'category': 'sports-fitness'
        },
        {
            'name': 'Bowflex Adjustable Dumbbells',
            'slug': 'bowflex-dumbbells',
            'sku': 'BWF-DUMB-552',
            'short_description': 'Replace 15 sets of weights with one',
            'description': 'Bowflex SelectTech 552 adjustable dumbbells from 5 to 52.5 lbs.',
            'price': 429.00,
            'compare_price': 549.00,
            'stock_quantity': 40,
            'thumbnail_url': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800&h=600&fit=crop',
            'brand': 'Bowflex',
            'is_featured': True,
            'category': 'sports-fitness'
        },
        {
            'name': 'Fitbit Charge 6',
            'slug': 'fitbit-charge-6',
            'sku': 'FIT-CHARGE6',
            'short_description': 'Advanced fitness tracker with GPS',
            'description': 'Fitbit Charge 6 with built-in GPS, heart rate zones, and stress management.',
            'price': 159.95,
            'compare_price': 179.95,
            'stock_quantity': 85,
            'thumbnail_url': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800&h=600&fit=crop',
            'brand': 'Fitbit',
            'is_new': True,
            'category': 'sports-fitness'
        },
        {
            'name': 'Theragun Elite',
            'slug': 'theragun-elite',
            'sku': 'TG-ELITE-BLK',
            'short_description': 'Smart percussive therapy device',
            'description': 'Theragun Elite with QuietForce Technology and Bluetooth app integration.',
            'price': 399.00,
            'compare_price': 449.00,
            'stock_quantity': 50,
            'thumbnail_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=600&fit=crop',
            'brand': 'Therabody',
            'is_featured': True,
            'category': 'sports-fitness'
        },

        # ============ WATCHES ============
        {
            'name': 'Apple Watch Ultra 2',
            'slug': 'apple-watch-ultra-2',
            'sku': 'APL-AWU2-49',
            'short_description': 'The most rugged and capable Apple Watch',
            'description': 'Apple Watch Ultra 2 with S9 chip, precision GPS, and 36-hour battery.',
            'price': 799.00,
            'compare_price': 899.00,
            'stock_quantity': 45,
            'thumbnail_url': 'https://images.unsplash.com/photo-1434494878577-86c23bcb06b9?w=800&h=600&fit=crop',
            'brand': 'Apple',
            'is_featured': True,
            'is_new': True,
            'category': 'watches'
        },
        {
            'name': 'Samsung Galaxy Watch 6 Classic',
            'slug': 'samsung-galaxy-watch-6',
            'sku': 'SAM-GW6-47',
            'short_description': 'Premium smartwatch with rotating bezel',
            'description': 'Galaxy Watch 6 Classic with rotating bezel, advanced health monitoring.',
            'price': 399.99,
            'compare_price': 449.99,
            'stock_quantity': 60,
            'thumbnail_url': 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800&h=600&fit=crop',
            'brand': 'Samsung',
            'is_featured': True,
            'category': 'watches'
        },
        {
            'name': 'Garmin Fenix 7',
            'slug': 'garmin-fenix-7',
            'sku': 'GAR-FX7-47',
            'short_description': 'Ultimate multisport GPS watch',
            'description': 'Garmin Fenix 7 with touchscreen, topo maps, and 18-day battery life.',
            'price': 699.99,
            'compare_price': 799.99,
            'stock_quantity': 35,
            'thumbnail_url': 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&h=600&fit=crop',
            'brand': 'Garmin',
            'category': 'watches'
        },

        # ============ BEAUTY ============
        {
            'name': 'Dyson Airwrap Complete',
            'slug': 'dyson-airwrap',
            'sku': 'DYS-AIRWRAP',
            'short_description': 'Multi-styler with Coanda air styling',
            'description': 'Dyson Airwrap multi-styler for curls, waves, smooth, and dry.',
            'price': 599.99,
            'compare_price': 649.99,
            'stock_quantity': 30,
            'thumbnail_url': 'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=800&h=600&fit=crop',
            'brand': 'Dyson',
            'is_featured': True,
            'category': 'beauty'
        },
        {
            'name': 'La Mer Moisturizing Cream',
            'slug': 'la-mer-cream',
            'sku': 'LM-CREAM-60',
            'short_description': 'The legendary Creme de la Mer',
            'description': 'La Mer Creme de la Mer with Miracle Broth for transformative healing.',
            'price': 380.00,
            'compare_price': 420.00,
            'stock_quantity': 25,
            'thumbnail_url': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800&h=600&fit=crop',
            'brand': 'La Mer',
            'is_featured': True,
            'category': 'beauty'
        },
        {
            'name': 'SK-II Facial Treatment Essence',
            'slug': 'sk-ii-essence',
            'sku': 'SKII-FTE-230',
            'short_description': 'The miracle water with Pitera',
            'description': 'SK-II Facial Treatment Essence with over 90% Pitera for crystal clear skin.',
            'price': 265.00,
            'compare_price': 295.00,
            'stock_quantity': 40,
            'thumbnail_url': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&h=600&fit=crop',
            'brand': 'SK-II',
            'category': 'beauty'
        },
    ]

    for prod_data in products_data:
        category_slug = prod_data.pop('category')
        category = categories.get(category_slug)
        
        product = Product(
            name=prod_data['name'],
            slug=prod_data['slug'],
            sku=prod_data['sku'],
            short_description=prod_data.get('short_description'),
            description=prod_data['description'],
            price=prod_data['price'],
            compare_price=prod_data.get('compare_price'),
            stock_quantity=prod_data.get('stock_quantity', 100),
            thumbnail_url=prod_data.get('thumbnail_url'),
            brand=prod_data.get('brand'),
            is_featured=prod_data.get('is_featured', False),
            is_new=prod_data.get('is_new', False),
            is_active=True
        )
        
        if category:
            product.categories.append(category)
        
        db.session.add(product)

    db.session.commit()
    print('✅ Products created')

    # Create Coupons
    coupons_data = [
        {
            'code': 'WELCOME10',
            'discount_type': 'percentage',
            'discount_value': 10,
            'min_order_amount': 50,
            'max_discount_amount': 100,
            'usage_limit': 1000,
            'per_user_limit': 1,
            'expires_at': datetime.utcnow() + timedelta(days=90)
        },
        {
            'code': 'FLAT50',
            'discount_type': 'fixed',
            'discount_value': 50,
            'min_order_amount': 200,
            'usage_limit': 500,
            'per_user_limit': 2,
            'expires_at': datetime.utcnow() + timedelta(days=60)
        },
        {
            'code': 'SAVE20',
            'discount_type': 'percentage',
            'discount_value': 20,
            'min_order_amount': 100,
            'max_discount_amount': 200,
            'usage_limit': 300,
            'per_user_limit': 1,
            'expires_at': datetime.utcnow() + timedelta(days=30)
        },
        {
            'code': 'NEWYEAR25',
            'discount_type': 'percentage',
            'discount_value': 25,
            'min_order_amount': 150,
            'max_discount_amount': 500,
            'usage_limit': 200,
            'per_user_limit': 1,
            'expires_at': datetime.utcnow() + timedelta(days=15)
        },
    ]

    for coupon_data in coupons_data:
        coupon = Coupon(**coupon_data)
        db.session.add(coupon)

    db.session.commit()
    print('✅ Coupons created')

    # Create product images for all products
    products = Product.query.all()
    for product in products:
        for i in range(3):
            image = ProductImage(
                product_id=product.id,
                image_url=product.thumbnail_url or f'https://picsum.photos/seed/{product.id}{i}/800/600',
                alt_text=f'{product.name} - Image {i+1}',
                is_primary=(i == 0),
                display_order=i
            )
            db.session.add(image)

    db.session.commit()
    print('✅ Product images created')

    print('\n✨ Database seeding completed successfully!')
    print('\n📋 Summary:')
    print(f'   - Users: {User.query.count()}')
    print(f'   - Categories: {Category.query.count()}')
    print(f'   - Products: {Product.query.count()}')
    print(f'   - Coupons: {Coupon.query.count()}')
    print(f'   - Product Images: {ProductImage.query.count()}')
    print('\n🔐 Test Accounts:')
    print('   Admin: admin@flaskmarket.com / Admin@123')
    print('   User: john@example.com / User@123')
    print('   User: jane@example.com / User@123')


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_database()










