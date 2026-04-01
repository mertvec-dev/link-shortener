"""Схемы для авторизации и регистрации"""

from pydantic import BaseModel


class UserRegister(BaseModel):
    """
    Схема для регистрации нового пользователя

    Атрибуты:
        username: Имя пользователя (уникальное)
        password: Пароль (будет захеширован при сохранении)
        email: Email пользователя (уникальный)
    """
    username: str
    password: str
    email: str  # Убрал EmailStr — простая строка


class UserLogin(BaseModel):
    """
    Схема для входа пользователя
    
    Атрибуты:
        username: Имя пользователя
        password: Пароль для проверки
    """
    username: str
    password: str


class Token(BaseModel):
    """
    Схема ответа с токенами доступа
    
    Атрибуты:
        access_token: JWT токен для доступа к API (30 минут)
        refresh_token: Токен для обновления access_token (7 дней)
        token_type: Тип токена (Bearer)
    """
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class UserResponse(BaseModel):
    """
    Схема ответа с данными пользователя

    Атрибуты:
        id: ID пользователя
        username: Имя пользователя
        email: Email пользователя
    """
    id: int
    username: str
    email: str


class RefreshTokenRequest(BaseModel):
    """
    Схема запроса на обновление токена

    Атрибуты:
        refresh_token: Refresh токен для получения нового access токена
    """
    refresh_token: str