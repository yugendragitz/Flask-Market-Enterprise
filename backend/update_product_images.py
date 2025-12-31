"""Update ALL products with accurate, working images based on product type"""
import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models import Product

app = create_app()

# Accurate product images from reliable sources
PRODUCT_IMAGES = {
    # === SMARTPHONES (1-5) ===
    1: "https://m.media-amazon.com/images/I/81dT7CUY6GL._SL1500_.jpg",  # iPhone 15 Pro Max
    2: "https://m.media-amazon.com/images/I/71lD7eGdW-L._SL1500_.jpg",  # Samsung Galaxy S24 Ultra
    3: "https://m.media-amazon.com/images/I/71GKBjwqRIL._SL1500_.jpg",  # Google Pixel 8 Pro
    4: "https://m.media-amazon.com/images/I/61amb0CfMGL._SL1500_.jpg",  # OnePlus 12
    5: "https://m.media-amazon.com/images/I/71d7rfSl0wL._SL1500_.jpg",  # iPhone 15
    
    # === LAPTOPS (6-10) ===
    6: "https://m.media-amazon.com/images/I/61lsexTCOhL._SL1500_.jpg",  # MacBook Pro 16" M3 Max
    7: "https://m.media-amazon.com/images/I/71jG+e7roXL._SL1500_.jpg",  # Dell XPS 15
    8: "https://m.media-amazon.com/images/I/71f5Eu5lJSL._SL1500_.jpg",  # MacBook Air M3
    9: "https://m.media-amazon.com/images/I/81GrCeuCzxL._SL1500_.jpg",  # ASUS ROG Zephyrus G14
    10: "https://m.media-amazon.com/images/I/71h1wzfGyyL._SL1500_.jpg",  # HP Spectre x360
    
    # === ELECTRONICS (11-16) ===
    11: "https://m.media-amazon.com/images/I/61+btxzpfDL._SL1500_.jpg",  # Sony WH-1000XM5
    12: "https://m.media-amazon.com/images/I/61SUj2aKoEL._SL1500_.jpg",  # AirPods Pro 2nd Gen
    13: "https://m.media-amazon.com/images/I/A1peVHBjqIL._SL1500_.jpg",  # Samsung 65" OLED 4K TV
    14: "https://m.media-amazon.com/images/I/51Ib6pqfRzL._SL1200_.jpg",  # Bose QuietComfort Ultra
    15: "https://m.media-amazon.com/images/I/71s4CmPLq+L._SL1500_.jpg",  # JBL Charge 5
    16: "https://m.media-amazon.com/images/I/71mIs2g3x0L._SL1500_.jpg",  # Apple HomePod mini
    
    # === GAMING (17-21) ===
    17: "https://m.media-amazon.com/images/I/51mWHXY8hyL._SL1500_.jpg",  # PlayStation 5
    18: "https://m.media-amazon.com/images/I/61nqNujSF3L._SL1280_.jpg",  # Nintendo Switch OLED
    19: "https://m.media-amazon.com/images/I/61-jjE67uqL._SL1500_.jpg",  # Xbox Series X
    20: "https://m.media-amazon.com/images/I/61yHgdjkRCL._SL1500_.jpg",  # Steam Deck OLED
    21: "https://m.media-amazon.com/images/I/61CGHv6kmWL._SL1500_.jpg",  # Razer BlackShark V2 Pro
    
    # === FASHION (22-26) ===
    22: "https://m.media-amazon.com/images/I/61-cPcbxbTL._SL1500_.jpg",  # Nike Air Max 270
    23: "https://m.media-amazon.com/images/I/71eGlFKLPSL._SL1500_.jpg",  # Adidas Ultraboost 23
    24: "https://m.media-amazon.com/images/I/61fkBa7OAEL._SL1500_.jpg",  # Levi's 501 Original Jeans
    25: "https://m.media-amazon.com/images/I/41tygoHeqmL._SL1000_.jpg",  # Ray-Ban Aviator Classic
    26: "https://m.media-amazon.com/images/I/71JhLu1I77L._SL1500_.jpg",  # The North Face Puffer Jacket
    
    # === HOME & KITCHEN (27-31) ===
    27: "https://m.media-amazon.com/images/I/61QRgOaVcVL._SL1500_.jpg",  # Dyson V15 Detect
    28: "https://m.media-amazon.com/images/I/71JlN7X3DAL._SL1500_.jpg",  # Nespresso Vertuo Next
    29: "https://m.media-amazon.com/images/I/71V1LrY-HkL._SL1500_.jpg",  # Instant Pot Duo 7-in-1
    30: "https://m.media-amazon.com/images/I/71Dv2LrwUcL._SL1500_.jpg",  # KitchenAid Stand Mixer
    31: "https://m.media-amazon.com/images/I/71MQN-8GKOL._SL1500_.jpg",  # Philips Air Fryer XXL
    
    # === BOOKS (32-35) ===
    32: "https://m.media-amazon.com/images/I/81YkqyaFVEL._SL1500_.jpg",  # Atomic Habits
    33: "https://m.media-amazon.com/images/I/81cpDaCJJCL._SL1500_.jpg",  # The Psychology of Money
    34: "https://m.media-amazon.com/images/I/71QKQ9mwV7L._SL1500_.jpg",  # Deep Work
    35: "https://m.media-amazon.com/images/I/71UypkUjStL._SL1500_.jpg",  # Think and Grow Rich
    
    # === SPORTS & FITNESS (36-39) ===
    36: "https://m.media-amazon.com/images/I/81sVcXqp8QL._SL1500_.jpg",  # Yoga Mat Premium
    37: "https://m.media-amazon.com/images/I/71vPp8F5yDL._SL1500_.jpg",  # Bowflex Adjustable Dumbbells
    38: "https://m.media-amazon.com/images/I/71z0GEqPUSL._SL1500_.jpg",  # Fitbit Charge 6
    39: "https://m.media-amazon.com/images/I/61wKRPwKKVL._SL1500_.jpg",  # Theragun Elite
    
    # === WATCHES (40-42) ===
    40: "https://m.media-amazon.com/images/I/81MWo-yqPnL._SL1500_.jpg",  # Apple Watch Ultra 2
    41: "https://m.media-amazon.com/images/I/61PqvTjgWRL._SL1500_.jpg",  # Samsung Galaxy Watch 6 Classic
    42: "https://m.media-amazon.com/images/I/71+-LjjhbGL._SL1500_.jpg",  # Garmin Fenix 7
    
    # === BEAUTY (43-45) ===
    43: "https://m.media-amazon.com/images/I/61BxsqfT7vL._SL1500_.jpg",  # Dyson Airwrap Complete
    44: "https://m.media-amazon.com/images/I/51gT-HPhAJL._SL1000_.jpg",  # La Mer Moisturizing Cream
    45: "https://m.media-amazon.com/images/I/61HMvYcxgnL._SL1500_.jpg",  # SK-II Facial Treatment Essence
}

with app.app_context():
    updated_count = 0
    
    for product_id, image_url in PRODUCT_IMAGES.items():
        product = Product.query.get(product_id)
        if product:
            product.thumbnail_url = image_url
            # Update all product images too
            for img in product.images:
                img.image_url = image_url
            print(f"✅ {product_id:2d}. {product.name}")
            updated_count += 1
        else:
            print(f"❌ Product ID {product_id} not found")
    
    db.session.commit()
    print(f"\n🎉 Successfully updated {updated_count} products with real images!")
