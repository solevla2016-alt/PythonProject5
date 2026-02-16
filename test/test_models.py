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


def test_category_initialization(sample_products, reset_category_counters):
    category = Category("Электроника", "Техника и гаджеты", sample_products)

    assert category.name == "Электроника"
    assert category.description == "Техника и гаджеты"
    assert category.products == sample_products


def test_category_count(sample_products, reset_category_counters):
    Category("Электроника", "Техника", sample_products)
    Category("Одежда", "Мужская одежда", [])

    assert Category.category_count == 2


def test_product_count(sample_products, reset_category_counters):
    Category("Электроника", "Техника", sample_products)
    Category("Одежда", "Мужская одежда", [])

    assert Category.product_count == 2