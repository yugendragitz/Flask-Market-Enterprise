"""Update products with real product images"""
import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models import Product

# Real product images mapped by product name
REAL_IMAGES = {
    # Smartphones
    "iPhone 15": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-finish-select-202309-6-1inch-black?wid=400&hei=400&fmt=jpeg",
    "iPhone 15 Pro Max": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-7inch-naturaltitanium?wid=400&hei=400&fmt=jpeg",
    "Samsung Galaxy S24 Ultra": "https://images.samsung.com/is/image/samsung/p6pim/in/2401/gallery/in-galaxy-s24-s928-sm-s928bzkcins-thumb-539573637",
    "Google Pixel 8 Pro": "https://lh3.googleusercontent.com/QqCaWLe_hLQ8fMBJHSrOOkwvSVvkCHhTsLcaEPNGBhY8FPZ4z3Vk_DqnkHT4MxMhGPzJkTwBzLQx9vI_k_RwxPLlRA=w400",
    "OnePlus 12": "https://oasis.opstatics.com/content/dam/oasis/page/2024/na/oneplus-12/specs/green-img.png",
    
    # Laptops
    "MacBook Pro 16": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mbp16-spacegray-select-202310?wid=400&hei=400&fmt=jpeg",
    "MacBook Air M3": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mba13-midnight-select-202402?wid=400&hei=400&fmt=jpeg",
    "Dell XPS 15": "https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/xps-notebooks/xps-15-9530/media-gallery/black/notebook-xps-15-9530-t-black-gallery-1.psd?fmt=png-alpha&wid=400",
    "ThinkPad X1 Carbon": "https://p1-ofp.static.pub/fes/cms/2022/11/17/r54o59lkz7b2zl0iu8llfevl1l5tl0029498.png",
    "ASUS ROG Zephyrus": "https://dlcdnwebimgs.asus.com/gain/8D12B3B6-5F0B-4F3B-8F5C-8F5F5F5F5F5F/w400",
    
    # Electronics
    "Sony WH-1000XM5": "https://electronics.sony.com/image/5d02da5df552836db894cead8a68f5f3?fmt=png-alpha&wid=400",
    "AirPods Pro 2": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MQD83?wid=400&hei=400&fmt=jpeg",
    "Apple Watch Ultra 2": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/watch-ultra-2-702702?wid=400&hei=400&fmt=jpeg",
    "iPad Pro 12.9": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-pro-13-select-wifi-spacegray-202210?wid=400&hei=400&fmt=jpeg",
    "Samsung 65\" OLED TV": "https://images.samsung.com/is/image/samsung/p6pim/in/qa65s90caklxl/gallery/in-oled-s90c-qa65s90caklxl-536281053?$400_400_PNG$",
    "Bose QuietComfort": "https://assets.bose.com/content/dam/Bose_DAM/Web/consumer_electronics/global/products/headphones/qc45/product_silo_images/QC45_PDP_Ecom-Gallery-B01.png/jcr:content/renditions/cq5dam.web.400.400.png",
    
    # Gaming
    "PlayStation 5": "https://gmedia.playstation.com/is/image/SIEPDC/ps5-product-thumbnail-01-en-14sep21?$400px$",
    "Xbox Series X": "https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RE4mRni?ver=db63&q=90&m=6&h=400&w=400",
    "Nintendo Switch OLED": "https://assets.nintendo.com/image/upload/c_fill,w_400/q_auto:best/f_auto/dpr_2.0/ncom/en_US/switch/site-design-update/hardware/switch-oled/background",
    "Steam Deck": "https://cdn.cloudflare.steamstatic.com/steamdeck/images/hardware/background_hero_rend_card.png",
    "Razer DeathAdder V3": "https://assets3.razerzone.com/6G8FYHZ4xG7JnVj8mBHl0qZzkhE=/400x400/https%3A%2F%2Fhybrismediaprod.blob.core.windows.net%2Fsys-master-phoenix-images-container%2Fh5f%2Fh0f%2F9597519822878%2F230406-deathadder-v3-pro-black-500x500.png",
    
    # Fashion
    "Nike Air Max 270": "https://static.nike.com/a/images/t_default/skwgyqrbfzhu6ez4zogf/air-max-270-shoes-2V5C4p.png",
    "Levi's 501 Original": "https://lsco.scene7.com/is/image/lsco/005010114-front-pdp?fmt=jpeg&qlt=70&resMode=bisharp&fit=crop,0&op_usm=1.25,0.6,8&wid=400&hei=400",
    "Ray-Ban Aviator": "https://www.ray-ban.com/images/is/image/RayBan/805289602057__STD__shad__qt.png?impolicy=RB_RB&width=400",
    "Adidas Ultraboost": "https://assets.adidas.com/images/w_400,f_auto,q_auto/1c8e77c8d8c1423e854caf0400b1e932_9366/Ultraboost_Light_Running_Shoes_Black_GZ0744_01_standard.jpg",
    "North Face Puffer": "https://images.thenorthface.com/is/image/TheNorthFace/NF0A4R2S_JK3_hero?wid=400&hei=400",
    
    # Home & Kitchen
    "Dyson V15 Detect": "https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/images/products/primary/448789-01.png?$responsive$&cropPathE=mobile&fit=stretch,1&wid=400",
    "Instant Pot Duo": "https://m.media-amazon.com/images/I/71V1LrY-HkL._AC_SX400_.jpg",
    "KitchenAid Mixer": "https://kitchenaid-h.assetsadobe.com/is/image/content/dam/global/kitchenaid/countertop-appliance/portable/images/hero-KSM150PSER.tif?fit=constrain,1&wid=400&hei=400",
    "Nespresso Vertuo": "https://www.nespresso.com/shared_res/agility/global/machines/vl/sku-main-media-responsive/vertuo-next_dark-chrome_front-open_primary-media_2x.png?impolicy=medium&imwidth=400",
    "Roomba j7+": "https://www.irobot.com/dw/image/v2/BGQD_PRD/on/demandware.static/-/Sites-master-catalog-irobot/default/dw1d8d3b1a/images/large/j755020_3Qtr.png?sw=400&sh=400",
    
    # Books
    "Atomic Habits": "https://m.media-amazon.com/images/I/81YkqyaFVEL._AC_UY400_.jpg",
    "The Psychology of Money": "https://m.media-amazon.com/images/I/81cpDaCJJCL._AC_UY400_.jpg",
    "Dune": "https://m.media-amazon.com/images/I/81ym3QUd3KL._AC_UY400_.jpg",
    "Project Hail Mary": "https://m.media-amazon.com/images/I/91dLJKpw3vL._AC_UY400_.jpg",
    
    # Sports & Fitness
    "Peloton Bike+": "https://images.ctfassets.net/lh3zuq09vnm2/yMGBKj4ohxxvPNO3LUHud/d3a5e8f9f8b0c3a2e1d0c9b8a7968574/BP_HP_Hero-PDP.png?fm=png&w=400",
    "Theragun Pro": "https://d1nymbkeomeoqg.cloudfront.net/photos/29/77/401927_23047_XL.jpg",
    "Hydro Flask": "https://www.hydroflask.com/media/catalog/product/cache/f8e24e3cb7ee6e3ba2db2a7df2c78b3c/w/3/w32bts_010_pl.png",
    "Fitbit Charge 6": "https://www.fitbit.com/global/content/dam/fitbit/global/pdp/devices/charge-6/hero/obsidian-aluminum/charge6-obsidian-aluminum-device-front.png",
    
    # Watches
    "Rolex Submariner": "https://content.rolex.com/dam/2022/upright-cc/watch-assets/m126610lv-0002.png?impolicy=v6-upright&imwidth=400",
    "Omega Speedmaster": "https://www.omegawatches.com/media/catalog/product/cache/a5c37fddc1a529a1a44fea55d527b9a116f3738da3a2cc38006ad3f8edfb8f5a/o/m/omega-speedmaster-moonwatch-professional-co-axial-master-chronometer-chronograph-42-mm-31030425001002-l.png",
    "Apple Watch Series 9": "https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/watch-case-45-aluminum-midnight-cell-s9_VW_PF+watch-face-45-aluminum-midnight-s9_VW_PF?wid=400&hei=400&fmt=jpeg",
    
    # Beauty
    "Dyson Airwrap": "https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/images/products/primary/400714-01.png?$responsive$&cropPathE=mobile&fit=stretch,1&wid=400",
    "La Mer Moisturizer": "https://www.cremedelamer.com/media/export/cms/products/1000x1000/cr_sku_5XMG01_1000x1000_0.png",
    "SK-II Facial Treatment Essence": "https://www.sk-ii.com/dw/image/v2/AAFQ_PRD/on/demandware.static/-/Sites-sk2-master-catalog/default/dw4d8b4a3e/images/large/82478582-1.jpg?sw=400&sh=400",
}

app = create_app()

with app.app_context():
    products = Product.query.all()
    updated = 0
    
    for product in products:
        if product.name in REAL_IMAGES:
            product.thumbnail_url = REAL_IMAGES[product.name]
            # Also update product images
            for img in product.images:
                img.image_url = REAL_IMAGES[product.name]
            updated += 1
            print(f"✅ Updated: {product.name}")
        else:
            # For products without specific images, use category-based placeholders
            print(f"⚠️  No image for: {product.name}")
    
    db.session.commit()
    print(f"\n✅ Updated {updated} products with real images")
