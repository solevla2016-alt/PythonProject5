import json
from pathlib import Path
from typing import List

from src.models import Category, Product


def load_data_from_json() -> List[Category]:
    """
    Безопасно загружает данные из data/products.json
    и создаёт объекты Category и Product.
    """

    # путь к корню проекта
    base_path = Path(__file__).resolve().parent.parent
    file_path = base_path / "data" / "products.json"

    # читаем файл с utf-8-sig, чтобы убрать BOM
    with open(file_path, "r", encoding="utf-8-sig") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Ошибка чтения JSON: {e}")
            return []

    categories = []

    for category_data in data:
        products = []

        for product_data in category_data.get("products", []):
            product = Product(
                name=product_data.get("name", ""),
                description=product_data.get("description", ""),
                price=product_data.get("price", 0.0),
                quantity=product_data.get("quantity", 0),
            )
            products.append(product)

        category = Category(
            name=category_data.get("name", ""),
            description=category_data.get("description", ""),
            products=products,
        )

        categories.append(category)

    return categories
