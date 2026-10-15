from pathlib import Path

from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

from .models import Category, Product

CATALOG = {
    "Men": {
        "image": "categories/men.jpg",
        "banner": (35, 47, 62),
        "products": [
            ("Men's Cotton T-Shirt", "Soft crew-neck tee for everyday wear.", "499.00", "products/men1.jpg", (37, 99, 166)),
            ("Men's Denim Jeans", "Slim-fit stretch jeans with a classic wash.", "1299.00", "products/men2.jpg", (30, 64, 110)),
            ("Men's Casual Shirt", "Breathable checked shirt for office or outing.", "899.00", "products/men3.jpg", (71, 85, 105)),
            ("Men's Hoodie", "Warm fleece hoodie with front pocket.", "1499.00", "products/men4.jpg", (21, 45, 80)),
        ],
    },
    "Women": {
        "image": "categories/women.jpg",
        "banner": (136, 53, 86),
        "products": [
            ("Women's Kurti", "Printed cotton kurti with comfortable fit.", "799.00", "products/women1.jpg", (190, 90, 120)),
            ("Women's Floral Dress", "Light floral midi dress for casual days.", "1599.00", "products/women2.jpg", (168, 85, 110)),
            ("Women's High-Rise Jeans", "Stretch denim with a flattering high rise.", "1199.00", "products/women3.jpg", (90, 50, 80)),
            ("Women's Saree", "Elegant festive saree with matching blouse.", "2499.00", "products/women4.jpg", (140, 40, 70)),
        ],
    },
    "Children": {
        "image": "categories/children.jpg",
        "banner": (22, 101, 52),
        "products": [
            ("Kids Graphic T-Shirt", "Fun printed tee for school and play.", "349.00", "products/kid1.jpeg", (34, 139, 90)),
            ("Kids Cotton Shorts", "Soft shorts with an elastic waist.", "399.00", "products/kid2.jpeg", (56, 161, 105)),
            ("Girls Frock", "Party frock with a twirl-ready skirt.", "699.00", "products/kid3.jpeg", (244, 114, 140)),
            ("Boys Hoodie", "Cozy zip hoodie for cooler days.", "599.00", "products/kid4.jpg", (14, 116, 144)),
        ],
    },
}


def _draw_label(path, color, title, subtitle, size=(640, 480)):
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.rectangle((24, 24, size[0] - 24, size[1] - 24), outline=(255, 255, 255), width=3)
    draw.text((48, size[1] // 2 - 24), title, fill=(255, 255, 255), font=font)
    draw.text((48, size[1] // 2 + 8), subtitle, fill=(240, 240, 240), font=font)
    image.save(path, "JPEG", quality=88)


def seed_clothes_catalog():
    media_root = Path(settings.MEDIA_ROOT)
    for category_name, data in CATALOG.items():
        category, _ = Category.objects.get_or_create(name=category_name)
        cat_rel = data["image"]
        cat_path = media_root / cat_rel
        if not cat_path.exists() or not category.image:
            _draw_label(cat_path, data["banner"], category_name, "Fashion")
        category.image = cat_rel
        category.save()

        for name, description, price, img_rel, color in data["products"]:
            path = media_root / img_rel
            if not path.exists():
                _draw_label(path, color, name, f"Rs {price}")
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "description": description,
                    "price": price,
                    "image": img_rel,
                },
            )
            product.category = category
            product.description = description
            product.price = price
            product.image = img_rel
            product.save()
