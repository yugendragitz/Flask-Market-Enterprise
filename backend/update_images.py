"""Update product images with working URLs"""
from app import create_app
from app.extensions import db
from app.models.product import Product, ProductImage

# Working image URLs for each product category
PRODUCT_IMAGES = {
    # Smartphones
    'iphone-15-pro-max': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-max-black-titanium-select?wid=400&hei=400&fmt=jpeg',
    'samsung-galaxy-s24-ultra': 'https://images.samsung.com/is/image/samsung/p6pim/in/2401/gallery/in-galaxy-s24-ultra-492829-sm-s928bzkcins-thumb-539573068?$400_400_PNG$',
    'google-pixel-8-pro': 'https://lh3.googleusercontent.com/pJ0PEGxuNo8sxbLqfYUbZm0g0hk34gKJlwMuB0vQQfSNvLEu3DPLTO8vw1Y_2DqX8A4hzWhgzjkQ=rw-e365-w400',
    'oneplus-12': 'https://oasis.opstatics.com/content/dam/oasis/page/2024/na/oneplus-12/specs/green-img.png',
    'iphone-15': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-blue-select?wid=400&hei=400&fmt=jpeg',
    
    # Laptops
    'macbook-pro-16-m3-max': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp16-spacegray-select-202310?wid=400&hei=400&fmt=jpeg',
    'dell-xps-15': 'https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/xps-notebooks/xps-15-9530/media-gallery/touch/notebook-xps-15-9530-t-gallery-1.psd?fmt=png-alpha&wid=400',
    'macbook-air-m3': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mba13-midnight-select-202402?wid=400&hei=400&fmt=jpeg',
    'asus-rog-zephyrus-g14': 'https://dlcdnwebimgs.asus.com/gain/9D8B5D4C-E8C3-4B3E-8D4D-8F4E0F4E0F4E/w400',
    'hp-spectre-x360': 'https://ssl-product-images.www8-hp.com/digmedialib/prodimg/lowres/c08467383.png',
    
    # Default fallback - using placeholder service
    'default': 'https://via.placeholder.com/400x400/1a1a2e/eee?text=Product'
}

def update_images():
    app = create_app()
    with app.app_context():
        products = Product.query.all()
        
        for product in products:
            # Use picsum with product ID as seed for consistent images
            new_url = f'https://picsum.photos/seed/{product.id}/400/400'
            
            # Update thumbnail
            product.thumbnail_url = new_url
            
            # Update product images
            for img in product.images:
                img.image_url = new_url
        
        db.session.commit()
        print(f'✅ Updated {len(products)} products with working images')

if __name__ == '__main__':
    update_images()
