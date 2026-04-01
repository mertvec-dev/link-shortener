"""Таблица ссылок"""

from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class Link(SQLModel, table=True):
    """
    Таблица сокращённых ссылок

    Атрибуты:
        id: Первичный ключ (автогенерация)
        owner_id: Внешний ключ на таблицу пользователей (кто создал)
        original_url: Оригинальная длинная ссылка
        short_code: Уникальный короткий код (для редиректа)
        clicks: Счётчик переходов по ссылке
        created_at: Дата и время создания ссылки (UTC)
    """
    id: int = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    original_url: str = Field()
    short_code: str = Field(unique=True, index=True)
    clicks: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) 