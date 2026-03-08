class ZeroQuantityError(Exception):
    """Ошибка добавления товара с нулевым количеством"""

    def __init__(self) -> None:
        super().__init__("Товар с нулевым количеством не может быть добавлен")
