def validate_password(password: str) -> bool:
    """
    Правила для прохождения пароля:
    1. Длина не меньше 8 символов
    2. Имеет хотя бы одну цифру
    3. Имеет хотя бы одну заглавную букву
    Возвращает True, если все ОК
    """
    # 1. Проверка длины
    if len(password) < 8:
        return False

    # 2. Наличие одной цифры
    has_digit = False

    for char in password:
        if char.isdigit():
            has_digit = True
            break

    if not has_digit: # если нет цифры
        return False

    # 3. Наличие заглавной буквы
    has_upper = False

    for char in password:
        if char.isupper():
            has_upper = True
            break

    if not has_upper:
        return False

    # ЕСЛИ ВСЕ ОКЕЙ
    return True