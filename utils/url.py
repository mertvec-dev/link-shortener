import random
import string

def generate_short_code(length: int = 6) -> str:
    """
    Генерит случайный код из букв и цифр длиной в 6 символов или больше
    """

    if length < 6:
        length = 6

    # символы для генератора
    characters = string.ascii_letters + string.digits

    # Случайный выбор символов
    code = "".join(random.choices(characters, k=length))

    return code