"""Таблица пользователей"""

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    Таблица пользователей для аутентификации
    
    Атрибуты:
        id: Первичный ключ (автогенерация)
        username: Уникальное имя пользователя (макс. 50 символов)
        password: Хеш пароля (bcrypt, макс. 100 символов)
        email: Уникальный email пользователя (макс. 100 символов)
    """
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    password: str = Field(max_length=100)
    email: str = Field(unique=True, index=True, max_length=100)