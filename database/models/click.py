"""Таблица кликов по ссылкам"""

from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class Click(SQLModel, table=True):
    """
    Таблица кликов для отслеживания переходов по ссылкам

    Атрибуты:
        id: Первичный ключ (автогенерация)
        link_id: Внешний ключ на таблицу ссылок (какая ссылка)
        ip: IP адрес пользователя (макс. 50 символов)
        user_agent: User-Agent браузера (макс. 500 символов)
        browser: Название браузера (макс. 100 символов)
        device: Тип устройства (макс. 100 символов)
        created_at: Дата и время клика (UTC)
    """
    id: int = Field(default=None, primary_key=True)
    link_id: int = Field(foreign_key="link.id")
    ip: str = Field(max_length=50)
    user_agent: str = Field(max_length=500)
    browser: str = Field(default="Неизвестно", max_length=100)
    device: str = Field(default="Неизвестно", max_length=100)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
