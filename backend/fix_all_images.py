"""Update ALL products with reliable, production-ready image URLs"""
import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models import Product

app = create_app()

# Using Unsplash and Picsum for reliable, production-ready images
# These CDNs support hotlinking and work perfectly in production
PRODUCT_IMAGES = {
    # Smartphones (IDs 1-5)
    1: "https://images.unsplash.com/photo-1697120531506-c1f0db3ce0a0?w=800&h=800&fit=crop",  # iPhone 15 Pro Max
    2: "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=800&h=800&fit=crop",  # Samsung Galaxy S24
    3: "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&h=800&fit=crop",  # Google Pixel
    4: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&h=800&fit=crop",  # OnePlus
    5: "https://images.unsplash.com/photo-1592286927505-4fd09de0574e?w=800&h=800&fit=crop",  # iPhone 15
    
    # Laptops (IDs 6-10)
    6: "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&h=600&fit=crop",  # MacBook Pro
    7: "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&h=600&fit=crop",  # Dell XPS
    8: "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800&h=600&fit=crop",  # MacBook Air
    9: "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&h=600&fit=crop",  # Gaming Laptop
    10: "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&h=600&fit=crop",  # HP Laptop
    
    # Electronics (IDs 11-16)
    11: "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&h=600&fit=crop",  # Sony Headphones
    12: "https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=800&h=600&fit=crop",  # AirPods Pro
    13: "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800&h=600&fit=crop",  # Samsung TV
    14: "https://images.unsplash.com/photo-1545127398-14699f92334b?w=800&h=600&fit=crop",  # Bose Headphones
    15: "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&h=600&fit=crop",  # JBL Speaker
    16: "https://images.unsplash.com/photo-1589492477829-5e65395b66cc?w=800&h=600&fit=crop",  # HomePod
    
    # Gaming (IDs 17-21)
    17: "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=800&h=600&fit=crop",  # PS5
    18: "https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=800&h=600&fit=crop",  # Nintendo Switch
    19: "https://images.unsplash.com/photo-1621259182978-fbf93132d53d?w=800&h=600&fit=crop",  # Xbox Series X
    20: "https://images.unsplash.com/photo-1625805866449-3589fe3f71a3?w=800&h=600&fit=crop",  # Steam Deck
    21: "https://images.unsplash.com/photo-1599669454699-248893623440?w=800&h=600&fit=crop",  # Gaming Headset
    
    # Fashion (IDs 22-26)
    22: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&h=800&fit=crop",  # Nike Shoes
    23: "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=800&h=800&fit=crop",  # Adidas Shoes
    24: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&h=800&fit=crop",  # Jeans
    25: "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&h=600&fit=crop",  # Sunglasses
    26: "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=800&h=800&fit=crop",  # Jacket
    
    # Home & Kitchen (IDs 27-31)
    27: "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800&h=600&fit=crop",  # Vacuum
    28: "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800&h=600&fit=crop",  # Coffee Machine
    29: "https://images.unsplash.com/photo-1585515320310-259814833e62?w=800&h=600&fit=crop",  # Instant Pot
    30: "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=800&h=600&fit=crop",  # Kitchen Mixer
    31: "https://images.unsplash.com/photo-1585032226651-759b368d7246?w=800&h=600&fit=crop",  # Air Fryer
    
    # Books (IDs 32-35)
    32: "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=600&h=800&fit=crop",  # Atomic Habits
    33: "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=600&h=800&fit=crop",  # Psychology Book
    34: "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=600&h=800&fit=crop",  # Deep Work
    35: "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=600&h=800&fit=crop",  # Classic Book
    
    # Sports & Fitness (IDs 36-39)
    36: "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800&h=600&fit=crop",  # Yoga Mat
    37: "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800&h=600&fit=crop",  # Dumbbells
    38: "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800&h=600&fit=crop",  # Fitbit
    39: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=600&fit=crop",  # Massage Gun
    
    # Watches (IDs 40-42)
    40: "https://images.unsplash.com/photo-1434494878577-86c23bcb06b9?w=800&h=600&fit=crop",  # Apple Watch
    41: "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800&h=600&fit=crop",  # Samsung Watch
    42: "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&h=600&fit=crop",  # Garmin Watch
    
    # Beauty (IDs 43-45)
    43: "https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=800&h=600&fit=crop",  # Hair Styling
    44: "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800&h=600&fit=crop",  # Skincare
    45: "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&h=600&fit=crop",  # Beauty Product
}

with app.app_context():
    for product_id, image_url in PRODUCT_IMAGES.items():
        product = Product.query.get(product_id)
        if product:
            product.thumbnail_url = image_url
            for img in product.images:
                img.image_url = image_url
            print(f"✅ {product_id}: {product.name}")
    
    db.session.commit()
    print(f"\n✅ Updated all {len(PRODUCT_IMAGES)} products with production-ready images!")
