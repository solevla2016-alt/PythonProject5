import pytest
from src.models import Product, Category


@pytest.fixture
def sample_products():
    return [
        Product("Телефон", "Смартфон", 19999.99, 10),
        Product("Ноутбук", "Игровой ноутбук", 79999.50, 5),
    ]


@pytest.fixture
def reset_category_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    product = Product("Наушники", "Беспроводные", 4999.99, 15)
    assert product.name == "Наушники"
    assert product.description == "Беспроводные"
    assert product.price == 4999.99
    assert product.quantity == 15


def test_product_repr():
    product = Product("Test", "Desc", 100.0, 1)
    assert "Test" in repr(product)
    assert "100.0" in repr(product)


def test_category_initialization(sample_products, reset_category_counters):
    category = Category("Электроника", "Техника и гаджеты", sample_products)

    assert category.name == "Электроника"
    assert category.description == "Техника и гаджеты"
    # Проверяем приватный атрибут через геттер
    assert category.products_list == sample_products
    # Проверка строкового геттера
    assert isinstance(category.products, str)
    assert "Телефон" in category.products
    assert "Ноутбук" in category.products


def test_category_count(sample_products, reset_category_counters):
    Category("Электроника", "Техника", sample_products)
    Category("Одежда", "Мужская одежда", [])

    assert Category.category_count == 2


def test_add_product(sample_products, reset_category_counters):
    """Проверяем добавление нового продукта и корректность счетчика"""
    category = Category("Электроника", "Техника", sample_products)
    new_product = Product("Монитор", "LCD 24\"", 12000.0, 3)

    # Сохраняем текущее значение глобального счетчика
    previous_count = Category.product_count

    # Добавляем продукт через метод add_product
    category.add_product(new_product)

    # Проверяем, что новый продукт есть в списке товаров через геттер
    assert new_product in category.products_list

    # Проверяем, что глобальный счетчик увеличился на 1
    assert Category.product_count == previous_count + 1



def test_new_product_creates_or_merges():
    existing = [
        Product("Телефон", "Смартфон", 20000.0, 5)
    ]
    # создаём новый уникальный
    new_prod = Product.new_product(
        {"name": "Ноутбук", "description": "Игровой", "price": 50000.0, "quantity": 2},
        existing
    )
    assert new_prod.name == "Ноутбук"
    assert new_prod.quantity == 2
    assert new_prod.price == 50000.0

    # создаём дубликат — увеличиваем количество и выбираем max цену
    merged_prod = Product.new_product(
        {"name": "Телефон", "description": "Смартфон", "price": 25000.0, "quantity": 3},
        existing
    )
    assert merged_prod is existing[0]
    assert merged_prod.quantity == 8  # 5+3
    assert merged_prod.price == 25000.0  # max(20000, 25000)

def test_price_setter_validation():
    product = Product("Test", "Desc", 100.0, 1)
    product.price = -10
    assert product.price == 100.0


def test_product_str():
    product = Product("Телефон", "Смартфон", 19999.99, 10)
    assert str(product) == "Телефон, 19999.99 руб. Остаток: 10 шт."

def test_category_str(sample_products, reset_category_counters):
    category = Category("Электроника", "Техника", sample_products)

    # 10 + 5 = 15
    assert str(category) == "Электроника, количество продуктов: 15 шт."

def test_product_add():
    p1 = Product("A", "Desc", 100.0, 10)
    p2 = Product("B", "Desc", 200.0, 2)

    # 100*10 + 200*2 = 1000 + 400 = 1400
    assert p1 + p2 == 1400

def test_product_add_invalid_type():
    p = Product("A", "Desc", 100.0, 10)
    assert p.__add__(5) is NotImplemented

