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
            'thumbnail_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-7inch-naturaltitanium?wid=400&hei=400&fmt=jpeg&qlt=90',
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
            'thumbnail_url': 'https://images.samsung.com/is/image/samsung/p6pim/in/2401/gallery/in-galaxy-s24-sm-s928bzkcins-thumb-539573074?w=400&h=400',
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
            'thumbnail_url': 'https://lh3.googleusercontent.com/oJMZhLkGKhAlKZdqxQ3FkKLV3EB_zCE6dsYwlqKMzmzKqgKIGZ4e9VcbZhGvCnBKIQ5_dVGQwR8BIw=w400-h400-rw',
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
            'thumbnail_url': 'https://oasis.opstatics.com/content/dam/oasis/page/2024/operation/0116/1200x1200.png.webp',
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
            'thumbnail_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-finish-select-202309-6-1inch-pink?wid=400&hei=400&fmt=jpeg&qlt=90',
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
            'thumbnail_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp16-spacegray-select-202310?wid=400&hei=400&fmt=jpeg&qlt=90',
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
            'thumbnail_url': 'https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/xps-notebooks/xps-15-9530/media-gallery/black/laptop-xps-9530-t-black-gallery-1.psd?fmt=png-alpha&pscan=auto&scl=1&wid=400&hei=400',
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
            'thumbnail_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mba13-midnight-select-202402?wid=400&hei=400&fmt=jpeg&qlt=90',
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
            'thumbnail_url': 'https://dlcdnwebimgs.asus.com/gain/10E8A46A-A5C4-4E4D-9C26-0B5C4F42E255/w400/h400',
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
            'thumbnail_url': 'https://www.hp.com/content/dam/sites/worldwide/personal-computers/consumer/laptops-tablets/hp-spectre-x360/702x532-spectre.png',
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
            'thumbnail_url': 'https://www.sony.com/image/5d02da5df552836db894cead8a68f5f3?fmt=png-alpha&wid=400',
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
            'thumbnail_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MQD83?wid=400&hei=400&fmt=jpeg&qlt=90',
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
            'thumbnail_url': 'https://images.samsung.com/is/image/samsung/p6pim/uk/qa65s95datxxu/gallery/uk-oled-s95d-qa65s95datxxu-thumb-539465109?$400_400_PNG$',
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
            'thumbnail_url': 'https://assets.bose.com/content/dam/cloudassets/Bose_DAM/Web/consumer_electronics/global/products/headphones/qc-ultra-headphones/product_silo_images/QCUltra_HP_black_EC_hero.png/jcr:content/renditions/cq5dam.web.400.400.png',
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
            'thumbnail_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop',
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
            'thumbnail_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/homepod-mini-select-blue-202110?wid=400&hei=400&fmt=jpeg&qlt=90',
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
            'thumbnail_url': 'https://www.sony.com/image/e1ca5c8ba5d155a7c98b3d5f0d8a1d02?fmt=png-alpha&wid=400',
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
            'thumbnail_url': 'https://assets.nintendo.com/image/upload/c_fill,w_400/q_auto:best/f_auto/dpr_auto/ncom/en_US/switch/site-design-update/hardware/switch-oled/nintendo-switch-oled-model-white-set-background',
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
            'thumbnail_url': 'https://compass-ssl.xbox.com/assets/0d/fa/0dfa368f-f03c-4f32-80a1-e5fb62969faf.jpg?n=Xbox-Series-X_Image-702x394.jpg',
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
            'thumbnail_url': 'https://clan.cloudflare.steamstatic.com/images//39049601/e09ed8fc2ea07d5df1eef6c034f7e58e2f6a8d1e.png',
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
            'thumbnail_url': 'https://assets3.razerzone.com/sOE_cxVVqLbWXHB6kFNNGa3hWJo=/400x400/https%3A%2F%2Fhybrismediaprod.blob.core.windows.net%2Fsys-master-phoenix-images-container%2Fh69%2Fh33%2F9356652167198%2Fblackshark-v2-pro-2023-black-500x500.png',
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
            'thumbnail_url': 'https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/awjogtdnqxniqqk0wpgf/air-max-270-shoes-2V5C4p.png',
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
            'thumbnail_url': 'https://assets.adidas.com/images/w_400,f_auto,q_auto/6312e22aa6b14ea29706af46015ca0da_9366/Ultraboost_Light_Shoes_White_GY9350_01_standard.jpg',
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
            'thumbnail_url': 'https://lsco.scene7.com/is/image/lsco/005010114-front-pdp?fmt=jpeg&qlt=70&resMode=bisharp&fit=crop,1&op_usm=0.6,0.6,8&wid=400&hei=400',
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
            'thumbnail_url': 'https://www.ray-ban.com/images/shared/sun/0RB3025-L0205_large.png',
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
            'thumbnail_url': 'https://images.thenorthface.com/is/image/TheNorthFace/NF0A3C8D_LE4_hero?wid=400&hei=400&fmt=jpeg&qlt=50',
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
            'thumbnail_url': 'https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/images/products/primary/394472-01.png?$responsive$&cropPathE=desktop&fit=stretch,1&wid=400',
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
            'thumbnail_url': 'https://www.nespresso.com/shared_res/agility/next-components/assets/machines/vertuo-next/vertuo-next-mat-black-side.png',
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
            'thumbnail_url': 'https://m.media-amazon.com/images/I/71WtwEvYDOS._AC_SX400_.jpg',
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
            'thumbnail_url': 'https://kitchenaid-h.assetsadobe.com/is/image/content/dam/business-unit/kitchenaid/en-us/marketing-content/site-assets/page-content/pinch-of-help/how-to-use-a-stand-mixer/how-to-use-a-stand-mixer-img1.jpg?wid=400',
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
            'thumbnail_url': 'https://www.usa.philips.com/c-dam/b2c/category-pages/household/cooking/airfryer/HD9867-96.png',
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
            'thumbnail_url': 'https://jamesclear.com/wp-content/uploads/2023/09/atomic-habits-dots.png',
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
            'thumbnail_url': 'https://m.media-amazon.com/images/I/71TRUbzcvaL._AC_UF400,400_QL80_.jpg',
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
            'thumbnail_url': 'https://m.media-amazon.com/images/I/81JJ7fyyKyS._AC_UF400,400_QL80_.jpg',
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
            'thumbnail_url': 'https://m.media-amazon.com/images/I/71UypkUjStL._AC_UF400,400_QL80_.jpg',
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
            'thumbnail_url': 'https://m.media-amazon.com/images/I/81Jyf-C5hbL._AC_SX400_.jpg',
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
            'thumbnail_url': 'https://m.media-amazon.com/images/I/61HmqhW0xLL._AC_SX400_.jpg',
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
            'thumbnail_url': 'https://www.fitbit.com/global/content/dam/fitbit/global/pdp/devices/charge-6/images/device-only/charge6-obsidian-angle-front.png',
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
            'thumbnail_url': 'https://www.therabody.com/dw/image/v2/BDFQ_PRD/on/demandware.static/-/Sites-therabody-master-catalog/default/dw7ea66a16/images/elite/g6-elite-product-img.png?sw=400&sh=400',
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
            'thumbnail_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MRF23ref_VW_34FR+watch-49-titanium-702x772?wid=400&hei=400&fmt=png-alpha',
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
            'thumbnail_url': 'https://images.samsung.com/is/image/samsung/p6pim/in/2307/gallery/in-galaxy-watch6-classic-sm-r960nzkains-536924028?$400_400_PNG$',
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
            'thumbnail_url': 'https://res.garmin.com/en/products/010-02540-01/g/cf-lg.jpg',
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
            'thumbnail_url': 'https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/images/products/hero/400185-01.png?$responsive$&cropPathE=desktop&fit=stretch,1&wid=400',
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
            'thumbnail_url': 'https://www.cremedelamer.com/media/export/cms/products/1000x1000/la_mer_sku_LMLJ01_1000x1000_0.png',
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
            'thumbnail_url': 'https://www.sk-ii.com/on/demandware.static/-/Sites-skii_master/default/dw3b7d9fb4/images/products/essence/facial-treatment-essence-75ml/FTE_75ML_Standing_Cap_On.png',
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










