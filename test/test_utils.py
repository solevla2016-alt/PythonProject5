import pytest
import json
from unittest.mock import mock_open, patch
from src.models import Product, Category
from src.utils import load_data_from_json


def test_load_data_from_json(monkeypatch):
    # создаём фейковые данные
    fake_json = json.dumps([
        {
            "name": "Смартфоны",
            "description": "Описание категории",
            "products": [
                {"name": "Iphone", "description": "Desc", "price": 1000.0, "quantity": 5}
            ]
        }
    ])

    m_open = mock_open(read_data=fake_json)
    monkeypatch.setattr("builtins.open", m_open)

    categories = load_data_from_json()
    assert isinstance(categories, list)
    assert all(isinstance(cat, Category) for cat in categories)
    assert categories[0].products_list[0].name == "Iphone"


def test_load_data_with_broken_json(monkeypatch):
    bad_json = '{"name": "test"'  # невалидный JSON
    m_open = mock_open(read_data=bad_json)
    monkeypatch.setattr("builtins.open", m_open)

    categories = load_data_from_json()
    assert categories == []  # при ошибке JSON возвращается пустой список


def test_categories_have_products():
    categories = load_data_from_json()
    for category in categories:
        assert isinstance(category.products_list, list)
        for product in category.products_list:
            assert isinstance(product, Product)


def test_product_attributes():
    categories = load_data_from_json()
    for category in categories:
        for product in category.products_list:
            assert isinstance(product.name, str)
            assert isinstance(product.description, str)
            assert isinstance(product.price, float)
            assert isinstance(product.quantity, int)


def test_product_attributes():
    """Проверяем, что атрибуты продуктов заполнены корректно"""
    categories = load_data_from_json()
    for category in categories:
        for product in category.products_list:  # <-- здесь тоже
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




