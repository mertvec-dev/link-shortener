"""Схемы для ссылок"""

from pydantic import BaseModel, HttpUrl
from datetime import datetime


class LinkCreate(BaseModel):
    """
    Схема для создания короткой ссылки

    Атрибуты:
        url: Оригинальная длинная ссылка (валидируется формат URL)
    """
    url: str


class LinkResponse(BaseModel):
    """
    Схема ответа с данными ссылки

    Атрибуты:
        id: ID ссылки
        short_code: Уникальный короткий код (для редиректа)
        original_url: Оригинальная длинная ссылка
        clicks: Количество переходов по ссылке
        created_at: Дата и время создания ссылки
    """
    id: int
    short_code: str
    original_url: HttpUrl
    clicks: int
    created_at: datetime


class LinkList(BaseModel):
    """
    Схема ответа со списком ссылок пользователя

    Атрибуты:
        links: Список ссылок
        total: Общее количество ссылок
    """
    links: list[LinkResponse]
    total: int


class ClickResponse(BaseModel):
    """
    Схема ответа с данными клика

    Атрибуты:
        id: ID клика
        ip: IP адрес пользователя
        user_agent: User-Agent браузера
        browser: Название браузера
        device: Тип устройства
        created_at: Дата и время клика
    """
    id: int
    ip: str
    user_agent: str
    browser: str
    device: str
    created_at: datetime


class ClickList(BaseModel):
    """
    Схема ответа со списком кликов

    Атрибуты:
        clicks: Список кликов
        total: Общее количество кликов
    """
    clicks: list[ClickResponse]
    total: int