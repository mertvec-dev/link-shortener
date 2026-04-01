from database.database import engine
from sqlmodel import Session, select
from database.models.link import Link
from database.models.click import Click
from utils.url import generate_short_code
from fastapi import Request
import re


def parse_browser(user_agent: str) -> str:
    """
    Определить браузер из User-Agent
    Возвращает название браузера
    """
    if not user_agent:
        return "Неизвестно"

    if "Edg" in user_agent:
        return "Microsoft Edge"
    elif "Chrome" in user_agent and "Chromium" not in user_agent:
        return "Chrome"
    elif "Firefox" in user_agent:
        return "Firefox"
    elif "Safari" in user_agent and "Chrome" not in user_agent:
        return "Safari"
    elif "Opera" in user_agent or "OPR" in user_agent:
        return "Opera"
    elif "MSIE" in user_agent or "Trident" in user_agent:
        return "Internet Explorer"
    else:
        return "Неизвестно"


def parse_device(user_agent: str) -> str:
    """
    Определить устройство из User-Agent
    Возвращает тип устройства
    """
    if not user_agent:
        return "Неизвестно"

    if re.search(r"Mobile|Android|iPhone|iPad|iPod|webOS|BlackBerry|Opera Mini|IEMobile", user_agent):
        return "Мобильное"
    elif re.search(r"Tablet|iPad|Android", user_agent):
        return "Планшет"
    else:
        return "Десктоп"


def get_request_info(request: Request) -> dict:
    """
    Получить информацию из запроса (IP, User-Agent, браузер, устройство)
    Возвращает словарь с данными
    """
    # Получаем IP адрес
    ip = request.client.host if request.client else "Неизвестно"

    # Получаем User-Agent
    user_agent = request.headers.get("User-Agent", "")

    # Парсим браузер и устройство
    browser = parse_browser(user_agent)
    device = parse_device(user_agent)

    return {
        "ip": ip,
        "user_agent": user_agent,
        "browser": browser,
        "device": device
    }


def log_click(link_id: int, request: Request) -> Click:
    """
    Записать информацию о клике в базу данных
    Возвращает созданный объект клика
    """
    # Получаем данные из запроса
    info = get_request_info(request)

    with Session(engine) as session:
        # Создаём клик
        click = Click(
            link_id=link_id,
            ip=info["ip"],
            user_agent=info["user_agent"],
            browser=info["browser"],
            device=info["device"]
        )

        session.add(click)
        session.commit()
        session.refresh(click)

        return click


def get_link_clicks(link_id: int) -> list[Click]:
    """
    Получить все клики по ссылке
    Возвращает список кликов
    """
    with Session(engine) as session:
        statement = select(Click).where(Click.link_id == link_id).order_by(Click.created_at.desc())
        clicks = session.exec(statement).all()
        return clicks


def create_link(user_id: int, url: str, link_length: int = 6) -> Link:
    """
    Создает короткую ссылку\n
    Возвращает созданную ссылку
    """
    with Session(engine) as session:
        # Генерируем уникальный код
        while True:
            short_code = generate_short_code(length=link_length)
            statement = select(Link).where(Link.short_code == short_code)
            existing = session.exec(statement).first()
            if not existing:
                break

        link = Link(
            owner_id=user_id,
            original_url=url,
            short_code=short_code,
        )
        session.add(link)
        session.commit()
        session.refresh(link)

        return link


def get_link(short_code: str) -> str | None:
    """
    Получить оригинальный URL по короткому коду
    Возвращает URL или None если не найдено
    """
    with Session(engine) as session:
        statement = select(Link).where(Link.short_code == short_code)
        link = session.exec(statement).first()

        if not link:
            return None

        link.clicks += 1
        session.commit()

        return link.original_url


def get_user_links(user_id: int) -> list[Link]:
    """
    Получить все ссылки пользователя
    Возвращает список ссылок
    """
    with Session(engine) as session:
        statement = select(Link).where(Link.owner_id == user_id)
        links = session.exec(statement).all()
        return links


def delete_link(user_id: int, link_id: int) -> bool:
    """
    Удалить ссылку (только если она принадлежит пользователю)
    Возвращает True если успешно, False если не найдено
    """
    with Session(engine) as session:
        # Находим ссылку
        statement = select(Link).where(
            Link.id == link_id,
            Link.owner_id == user_id
        )
        link = session.exec(statement).first()

        # Если не найдена
        if not link:
            return False

        # Удаляем ссылку
        session.delete(link)
        session.commit()
        return True