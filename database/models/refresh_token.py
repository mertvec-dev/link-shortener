"""Таблица refresh-токенов"""

from sqlmodel import SQLModel, Field
from datetime import datetime, timezone, timedelta


class RefreshToken(SQLModel, table=True):
    """
    Таблица refresh-токенов для обновления access-токенов
    
    Атрибуты:
        id: Первичный ключ (автогенерация)
        user_id: Внешний ключ на таблицу пользователей (кому принадлежит)
        refresh_token: Уникальный токен обновления (случайная строка)
        expires_at: Дата и время истечения токена (7 дней от создания, UTC)
    """
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    refresh_token: str = Field(unique=True, index=True)
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=7))