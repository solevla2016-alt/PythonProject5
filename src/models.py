from typing import List, Optional
from typing import Any


class Product:
    """
    Класс для описания товара
    """

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price  # полностью приватный атрибут
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            answer = input(
                f"Вы действительно хотите понизить цену с {self.__price} до {new_price}? (y/n): "
            )
            if answer.lower() != "y":
                return

        self.__price = new_price

    @classmethod
    def new_product(
        cls, data: dict, existing_products: Optional[List["Product"]] = None
    ) -> "Product":
        existing_products = existing_products or []
        name = data.get("name", "")
        description = data.get("description", "")
        price = data.get("price", 0.0)
        quantity = data.get("quantity", 0)

        for prod in existing_products:
            if prod.name == name:
                prod.quantity += quantity
                if price > prod.price:
                    prod.price = price
                return prod

        return cls(name, description, price, quantity)

    def __repr__(self) -> str:
        return (
            f"Product(name={self.name}, price={self.__price}, quantity={self.quantity})"
        )

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")

        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    """
    Класс смартфонов
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """
    Класс газонной травы
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """
    Класс для описания категории товаров
    """

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self, name: str, description: str, products: Optional[List[Product]] = None
    ) -> None:
        self.name = name
        self.description = description
        self.__products: List[Product] = products or []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Any) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только продукты или их наследников")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """
        Геттер для приватного атрибута products.
        Возвращает строку строго по шаблону:
        "Название продукта, X руб. Остаток: X шт.\n"
        """
        return "".join(
            f"{prod.name}, {prod.price} руб. Остаток: {prod.quantity} шт.\n"
            for prod in self.__products
        )

    @property
    def products_list(self) -> List[Product]:
        """
        Возвращает список объектов Product (если нужен доступ к объектам)
        """
        return self.__products

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
