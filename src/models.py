from typing import List


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, quantity={self.quantity})"


class Category:
    # Атрибуты класса (общие для всех объектов)
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        # Атрибуты экземпляра
        self.name: str = name
        self.description: str = description
        self.products: List[Product] = products

        # Увеличиваем счётчики класса
        Category.category_count += 1
        Category.product_count += len(products)

