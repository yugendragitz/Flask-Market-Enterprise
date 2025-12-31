"""
Update product images with category-matched images from Unsplash
"""

from app import create_app
from app.extensions import db
from app.models.product import Product, Category, ProductImage

# Product-specific images using Unsplash Source (free, reliable)
PRODUCT_IMAGES = {
    # SMARTPHONES
    'iphone-15-pro-max': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop',
    'samsung-galaxy-s24-ultra': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&h=400&fit=crop',
    'google-pixel-8-pro': 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400&h=400&fit=crop',
    'oneplus-12': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop',
    'iphone-15': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop',
    
    # LAPTOPS
    'macbook-pro-16-m3-max': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop',
    'dell-xps-15': 'https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400&h=400&fit=crop',
    'macbook-air-m3': 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=400&h=400&fit=crop',
    'asus-rog-zephyrus-g14': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=400&fit=crop',
    'hp-spectre-x360': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop',
    
    # ELECTRONICS
    'sony-wh-1000xm5': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
    'airpods-pro-2': 'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=400&h=400&fit=crop',
    'samsung-65-oled-4k': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400&h=400&fit=crop',
    'bose-quietcomfort-ultra': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400&h=400&fit=crop',
    'jbl-charge-5': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop',
    'apple-homepod-mini': 'https://images.unsplash.com/photo-1589003077984-894e133dabab?w=400&h=400&fit=crop',
    
    # GAMING
    'playstation-5': 'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=400&fit=crop',
    'nintendo-switch-oled': 'https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=400&h=400&fit=crop',
    'xbox-series-x': 'https://images.unsplash.com/photo-1621259182978-fbf93132d53d?w=400&h=400&fit=crop',
    'steam-deck-oled': 'https://images.unsplash.com/photo-1640955014216-75201056c829?w=400&h=400&fit=crop',
    'razer-blackshark-v2-pro': 'https://images.unsplash.com/photo-1599669454699-248893623440?w=400&h=400&fit=crop',
    
    # FASHION
    'nike-air-max-270': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop',
    'adidas-ultraboost-23': 'https://images.unsplash.com/photo-1556906781-9a412961c28c?w=400&h=400&fit=crop',
    'levis-501-original': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop',
    'rayban-aviator-classic': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop',
    'north-face-puffer': 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&h=400&fit=crop',
    
    # HOME & KITCHEN
    'dyson-v15-detect': 'https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=400&fit=crop',
    'nespresso-vertuo-next': 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400&h=400&fit=crop',
    'instant-pot-duo': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=400&h=400&fit=crop',
    'kitchenaid-stand-mixer': 'https://images.unsplash.com/photo-1594385208974-2e75f8d7bb48?w=400&h=400&fit=crop',
    'philips-air-fryer-xxl': 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400&h=400&fit=crop',
    
    # BOOKS
    'atomic-habits-book': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop',
    'psychology-of-money': 'https://images.unsplash.com/photo-1592496431122-2349e0fbc666?w=400&h=400&fit=crop',
    'deep-work-book': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=400&fit=crop',
    'think-grow-rich': 'https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400&h=400&fit=crop',
    
    # SPORTS & FITNESS
    'yoga-mat-premium': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=400&fit=crop',
    'bowflex-dumbbells': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&h=400&fit=crop',
    'fitbit-charge-6': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400&h=400&fit=crop',
    'theragun-elite': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop',
    
    # WATCHES
    'apple-watch-ultra-2': 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=400&fit=crop',
    'samsung-galaxy-watch-6': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
    'garmin-fenix-7': 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400&h=400&fit=crop',
    
    # BEAUTY
    'dyson-airwrap': 'https://images.unsplash.com/photo-1522338140262-f46f5913618a?w=400&h=400&fit=crop',
    'la-mer-cream': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop',
    'sk-ii-essence': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop',
}

# Category images
CATEGORY_IMAGES = {
    'electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=400&fit=crop',
    'smartphones': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop',
    'laptops': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop',
    'fashion': 'https://images.unsplash.com/photo-1445205170230-053b83016050?w=400&h=400&fit=crop',
    'home-kitchen': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop',
    'books': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400&h=400&fit=crop',
    'gaming': 'https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=400&h=400&fit=crop',
    'sports-fitness': 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=400&h=400&fit=crop',
    'beauty': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop',
    'watches': 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=400&h=400&fit=crop',
}


def update_images():
    """Update all product and category images"""
    app = create_app()
    
    with app.app_context():
        print('🖼️  Updating product images...')
        
        # Update products
        products = Product.query.all()
        updated_count = 0
        
        for product in products:
            if product.slug in PRODUCT_IMAGES:
                new_url = PRODUCT_IMAGES[product.slug]
                product.thumbnail_url = new_url
                
                # Update product images too
                for img in product.images:
                    img.image_url = new_url
                
                updated_count += 1
                print(f'  ✓ {product.name}')
        
        print(f'\n🏷️  Updating category images...')
        
        # Update categories
        categories = Category.query.all()
        for category in categories:
            if category.slug in CATEGORY_IMAGES:
                category.image_url = CATEGORY_IMAGES[category.slug]
                print(f'  ✓ {category.name}')
        
        db.session.commit()
        
        print(f'\n✅ Updated {updated_count} products with matching images!')
        print('🔄 Refresh your browser to see the changes.')


if __name__ == '__main__':
    update_images()
