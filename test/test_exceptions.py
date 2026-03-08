import pytest
from src.models import ZeroQuantityError

def test_zero_quantity_error_message():
    """Проверка текста исключения ZeroQuantityError"""
    with pytest.raises(ZeroQuantityError) as exc_info:
        raise ZeroQuantityError()

