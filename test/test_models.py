import pytest
from src.models import Product, Category, Smartphone, LawnGrass


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


def test_product_str():
    product = Product("Телефон", "Смартфон", 19999.99, 10)

    assert str(product) == "Телефон, 19999.99 руб. Остаток: 10 шт."


def test_product_add_same_type():
    p1 = Product("A", "Desc", 100.0, 10)
    p2 = Product("B", "Desc", 200.0, 2)

    assert p1 + p2 == 1400


def test_product_add_different_type():
    p1 = Product("A", "Desc", 100.0, 10)
    phone = Smartphone("Phone", "Desc", 200.0, 2, 90.0, "X", 128, "Black")

    with pytest.raises(TypeError):
        p1 + phone


def test_price_setter_validation():
    product = Product("Test", "Desc", 100.0, 1)
    product.price = -10

    assert product.price == 100.0


def test_new_product_creates_or_merges():
    existing = [Product("Телефон", "Смартфон", 20000.0, 5)]

    # новый товар
    new_prod = Product.new_product(
        {
            "name": "Ноутбук",
            "description": "Игровой",
            "price": 50000.0,
            "quantity": 2,
        },
        existing,
    )

    assert new_prod.name == "Ноутбук"
    assert new_prod.quantity == 2
    assert new_prod.price == 50000.0

    # объединение существующего
    merged_prod = Product.new_product(
        {
            "name": "Телефон",
            "description": "Смартфон",
            "price": 25000.0,
            "quantity": 3,
        },
        existing,
    )

    assert merged_prod is existing[0]
    assert merged_prod.quantity == 8
    assert merged_prod.price == 25000.0


def test_smartphone_creation():
    phone = Smartphone(
        "iPhone",
        "Смартфон",
        100000.0,
        5,
        95.5,
        "15 Pro",
        256,
        "Black",
    )

    assert phone.model == "15 Pro"
    assert phone.memory == 256
    assert phone.efficiency == 95.5
    assert isinstance(phone, Product)


def test_lawngrass_creation():
    grass = LawnGrass(
        "Газон",
        "Трава",
        500.0,
        20,
        "Россия",
        7,
        "Зеленый",
    )

    assert grass.country == "Россия"
    assert grass.germination_period == 7
    assert grass.color == "Зеленый"
    assert isinstance(grass, Product)


def test_add_same_subclass():
    phone1 = Smartphone("A", "Desc", 100.0, 2, 90.0, "X", 128, "Black")
    phone2 = Smartphone("B", "Desc", 200.0, 1, 85.0, "Y", 256, "White")

    assert phone1 + phone2 == 400


def test_add_different_subclasses():
    phone = Smartphone("A", "Desc", 100.0, 1, 90.0, "X", 128, "Black")
    grass = LawnGrass("B", "Desc", 50.0, 2, "RU", 5, "Green")

    with pytest.raises(TypeError):
        phone + grass

def test_category_initialization(sample_products, reset_category_counters):
    category = Category("Электроника", "Техника", sample_products)

    assert category.name == "Электроника"
    assert category.description == "Техника"
    assert category.products_list == sample_products
    assert "Телефон" in category.products


def test_category_str(sample_products, reset_category_counters):
    category = Category("Электроника", "Техника", sample_products)

    # 10 + 5 = 15
    assert str(category) == "Электроника, количество продуктов: 15 шт."


def test_category_count(sample_products, reset_category_counters):
    Category("Электроника", "Техника", sample_products)
    Category("Одежда", "Мужская одежда", [])

    assert Category.category_count == 2


def test_add_product(sample_products, reset_category_counters):
    category = Category("Электроника", "Техника", sample_products)
    new_product = Product("Монитор", "LCD 24", 12000.0, 3)

    previous_count = Category.product_count
    category.add_product(new_product)

    assert new_product in category.products_list
    assert Category.product_count == previous_count + 1


def test_add_invalid_object_to_category(reset_category_counters):
    category = Category("Test", "Desc")

    with pytest.raises(TypeError):
        category.add_product("not a product")
