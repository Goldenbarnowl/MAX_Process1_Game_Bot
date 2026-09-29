import re

def validate_name(name: str) -> bool:
    """
    Проверяет:
    - только кириллица
    - длина от 1 до 20 символов
    """
    return bool(re.fullmatch(r"[А-Яа-яЁё]{1,20}", name.strip()))
