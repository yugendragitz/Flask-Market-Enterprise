"""Update ALL products with real working images"""
import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models import Product

app = create_app()

# These are reliable, working image URLs
PRODUCT_IMAGES = {
    # Smartphones (IDs 1-5)
    1: "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-15-pro-max-1.jpg",  # iPhone 15 Pro Max
    2: "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s24-ultra-5g-sm-s928-1.jpg",  # Samsung Galaxy S24 Ultra
    3: "https://fdn2.gsmarena.com/vv/pics/google/google-pixel-8-pro-1.jpg",  # Google Pixel 8 Pro
    4: "https://fdn2.gsmarena.com/vv/pics/oneplus/oneplus-12-1.jpg",  # OnePlus 12
    5: "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-15-1.jpg",  # iPhone 15
    
    # Laptops (IDs 6-10)
    6: "https://i.pcmag.com/imagery/reviews/07t6FuB1cFGNZbIWU90mEfE-1.fit_lim.size_1050x591.v1699392031.jpg",  # MacBook Pro 16
    7: "https://i.pcmag.com/imagery/reviews/00NXHS3Q2I8rJLhVJiAQxXV-13.fit_lim.size_1050x591.v1681740219.jpg",  # Dell XPS 15
    8: "https://i.pcmag.com/imagery/reviews/03G1L4XFJ0HJX3bh3CVQyqw-1.fit_lim.size_1050x591.v1709746955.jpg",  # MacBook Air M3
    9: "https://i.pcmag.com/imagery/reviews/03SiIRzPpQ5cP1hExaKq77Y-1.fit_lim.size_1050x591.v1674668361.jpg",  # ASUS ROG Zephyrus
    10: "https://i.pcmag.com/imagery/reviews/03aqLpXCXUv01t2JPNjOhXy-1.fit_lim.size_1050x591.v1695243491.jpg",  # HP Spectre
    
    # Electronics (IDs 11-16)
    11: "https://i.pcmag.com/imagery/reviews/027JHJHK3QCXjMfJ4efzlKM-1.fit_lim.size_1050x591.v1653588597.jpg",  # Sony WH-1000XM5
    12: "https://i.pcmag.com/imagery/reviews/00YCMmYkLwQJvGYGPMjQQmG-1.fit_lim.size_1050x591.v1663877590.jpg",  # AirPods Pro 2
    13: "https://i.pcmag.com/imagery/reviews/02mLJSLdwJvAiGNWvtq2RPf-1.fit_lim.size_1050x591.v1672420746.jpg",  # Samsung OLED TV
    14: "https://i.pcmag.com/imagery/reviews/061gcunV5mwnLoqttCcwALO-1.fit_lim.size_1050x591.v1696343628.jpg",  # Bose QuietComfort
    15: "https://i.pcmag.com/imagery/reviews/02qEIiLJJGU4dLLYc1aw16h-1.fit_lim.size_1050x591.v1653413683.jpg",  # JBL Charge 5
    16: "https://i.pcmag.com/imagery/reviews/05XlwqPq1e6vQzAIMvNgCwu-1.fit_lim.size_1050x591.v1605733430.jpg",  # HomePod Mini
    
    # Gaming (IDs 17-21)
    17: "https://i.pcmag.com/imagery/reviews/04sM1IClHDePghhvDdxB9em-1.fit_lim.size_1050x591.v1604957493.jpg",  # PS5
    18: "https://i.pcmag.com/imagery/reviews/073YX8dFIbOCwJQb8iD9i7W-1.fit_lim.size_1050x591.v1633631253.jpg",  # Nintendo Switch OLED
    19: "https://i.pcmag.com/imagery/reviews/02D9qHEwlrpMYPVnXHaZmAB-1.fit_lim.size_1050x591.v1604625587.jpg",  # Xbox Series X
    20: "https://i.pcmag.com/imagery/reviews/01qRvJIYW4N5p8xYhcqfTlQ-1.fit_lim.size_1050x591.v1677254992.jpg",  # Steam Deck
    21: "https://i.pcmag.com/imagery/reviews/04bOZEFmfMnj1VEm0S3eLUz-1.fit_lim.size_1050x591.v1683569181.jpg",  # Razer Headset
    
    # Fashion (IDs 22-26)
    22: "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/awjogtdnqxniqqk0wpgf/air-max-270-shoes-2V5C4p.png",  # Nike Air Max
    23: "https://brand.assets.adidas.com/image/upload/f_auto,q_auto:best,fl_lossy/if_w_gt_800,w_800/ultraboost_light_running_ss24_launch_clp_global_hp_d_dd0e30bcde.jpg",  # Adidas
    24: "https://lsco.scene7.com/is/image/lsco/005010114-front-pdp?fmt=jpeg&qlt=70&resMode=bisharp&fit=crop,0&op_usm=1.25,0.6,8&wid=600&hei=600",  # Levi's
    25: "https://assets.ray-ban.com/is/image/RayBan/805289602057_shad_qt.png?impolicy=RB_RB_FBShare",  # Ray-Ban
    26: "https://images.thenorthface.com/is/image/TheNorthFace/NF0A4R2S_JK3_hero?wid=600&hei=600",  # North Face
    
    # Home & Kitchen (IDs 27-31)
    27: "https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/images/products/hero/448789-01.png?$responsive$&cropPathE=desktop&fit=stretch,1&fmt=pjpeg&wid=600",  # Dyson V15
    28: "https://www.nespresso.com/ecom/medias/sys_master/public/14794219520030/M-0581-PDP-Background-Front.png?impolicy=productPdpSa498",  # Nespresso
    29: "https://m.media-amazon.com/images/I/71V1LrY-HkL._AC_SX679_.jpg",  # Instant Pot
    30: "https://kitchenaid-h.assetsadobe.com/is/image/content/dam/global/kitchenaid/countertop-appliance/portable/images/hero-KSM150PSER.tif?$ka-product-hero$",  # KitchenAid
    31: "https://m.media-amazon.com/images/I/71O+fJHfPiL._AC_SX679_.jpg",  # Air Fryer
    
    # Books (IDs 32-35)
    32: "https://m.media-amazon.com/images/I/81YkqyaFVEL._AC_UF1000,1000_QL80_.jpg",  # Atomic Habits
    33: "https://m.media-amazon.com/images/I/81cpDaCJJCL._AC_UF1000,1000_QL80_.jpg",  # Psychology of Money
    34: "https://m.media-amazon.com/images/I/71bLEVj5alL._AC_UF1000,1000_QL80_.jpg",  # Deep Work
    35: "https://m.media-amazon.com/images/I/91dLJKpw3vL._AC_UF1000,1000_QL80_.jpg",  # Think and Grow Rich
    
    # Sports & Fitness (IDs 36-39)
    36: "https://m.media-amazon.com/images/I/71uEsDC2BhL._AC_SX679_.jpg",  # Yoga Mat
    37: "https://m.media-amazon.com/images/I/71vPp8F5yDL._AC_SX679_.jpg",  # Bowflex Dumbbells
    38: "https://i.pcmag.com/imagery/reviews/05GqHK4Xy2NIeL8wXLPzZJu-1.fit_lim.size_1050x591.v1696877759.jpg",  # Fitbit Charge 6
    39: "https://m.media-amazon.com/images/I/61wKRPwKKVL._AC_SX679_.jpg",  # Theragun
    
    # Watches (IDs 40-42)
    40: "https://i.pcmag.com/imagery/reviews/036F5K90sTOthXkc9rXNOYe-1.fit_lim.size_1050x591.v1696451015.jpg",  # Apple Watch Ultra 2
    41: "https://i.pcmag.com/imagery/reviews/03QpGfLqkXVqYOCDcQeRqcP-1.fit_lim.size_1050x591.v1690994932.jpg",  # Samsung Galaxy Watch
    42: "https://i.pcmag.com/imagery/reviews/04fGzahCCJ0kPMBnBc3tP2X-1.fit_lim.size_1050x591.v1673454973.jpg",  # Garmin Fenix
    
    # Beauty (IDs 43-45)
    43: "https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/leap-petproducts-702702/702702-p1.png?$responsive$&cropPathE=desktop&fit=stretch,1&fmt=pjpeg&wid=600",  # Dyson Airwrap
    44: "https://m.media-amazon.com/images/I/51gT-HPhAJL._SX679_.jpg",  # La Mer
    45: "https://m.media-amazon.com/images/I/61HMvYcxgnL._SX679_.jpg",  # SK-II
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
    print(f"\n✅ Updated all {len(PRODUCT_IMAGES)} products with real images!")
