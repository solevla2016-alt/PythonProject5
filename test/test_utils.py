from src.models import Product, Category
from src.utils import load_data_from_json


def test_load_data_returns_list():
    """Проверяем, что функция возвращает список категорий"""
    categories = load_data_from_json()
    assert isinstance(categories, list)
    assert all(isinstance(c, Category) for c in categories)


def test_categories_have_products():
    """Проверяем, что каждая категория содержит список объектов Product"""
    categories = load_data_from_json()
    for category in categories:
        assert isinstance(category.products, list)
        for product in category.products:
            assert isinstance(product, Product)


def test_product_attributes():
    """Проверяем, что атрибуты продуктов заполнены корректно"""
    categories = load_data_from_json()
    for category in categories:
        for product in category.products:
            assert isinstance(product.name, str)
            assert isinstance(product.description, str)
            assert isinstance(product.price, float)
            assert isinstance(product.quantity, int)


def test_category_attributes():
    """Проверяем, что атрибуты категорий заполнены корректно"""
    categories = load_data_from_json()
    for category in categories:
        assert isinstance(category.name, str)
        assert isinstance(category.description, str)


def test_total_counts():
    """Простейший тест на количество категорий и продуктов"""
    categories = load_data_from_json()
    total_products = sum(len(c.products) for c in categories)
    # Проверяем, что количество категорий > 0 и продуктов > 0
    assert len(categories) > 0
    assert total_products > 0




