from typing import List, Optional


class Product:
    """
    Класс для описания товара
    """

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self._price = price  # приватный атрибут цены
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для цены"""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if new_price < self._price:
            answer = input(
                f"Вы действительно хотите понизить цену с {self._price} до {new_price}? (y/n): "
            )
            if answer.lower() != "y":
                return
        self._price = new_price

    @classmethod
    def new_product(
        cls, data: dict, existing_products: Optional[List["Product"]] = None
    ) -> "Product":
        """
        Создает новый продукт из словаря.
        Если продукт с таким именем уже есть, суммирует количество
        и выбирает более высокую цену.
        """
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
            f"Product(name={self.name}, price={self._price}, quantity={self.quantity})"
        )


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

    def add_product(self, product: Product) -> None:
        """
        Добавляет продукт в категорию
        """
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
