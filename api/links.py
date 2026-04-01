from fastapi import APIRouter, HTTPException, Path, Depends, Request
from fastapi.responses import RedirectResponse
from schemas.links import LinkCreate, LinkResponse, LinkList, ClickList, ClickResponse
from services.links import create_link, get_link, get_user_links, log_click, get_link_clicks
from services.links import delete_link as delete_link_services
from utils.jwt_utils import get_current_user
from database.database import engine
from sqlmodel import Session, select
from database.models.link import Link

router = APIRouter(prefix="/links", tags=["Ссылки"])

@router.post("/shorten", response_model=LinkResponse)
def make_link(link: LinkCreate, user_id: int = Depends(get_current_user)):
    link = create_link(user_id=user_id, url=link.url)

    return link

@router.get("/my", response_model=LinkList)
def my_links(user_id: int = Depends(get_current_user)):
    links = get_user_links(user_id)

    # Конвертируем Link модели в LinkResponse
    links_response = [
        LinkResponse(
            id=link.id,
            short_code=link.short_code,
            original_url=link.original_url,
            clicks=link.clicks,
            created_at=link.created_at
        )
        for link in links
    ]

    return LinkList(links=links_response, total=len(links))

@router.get("/{short_code}")
def redirect(short_code: str, request: Request):
    # Получаем оригинальный URL
    original_url = get_link(short_code=short_code)

    # Если нет -> 404
    if not original_url:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")

    # Получаем ссылку из БД для получения ID
    with Session(engine) as session:
        statement = select(Link).where(Link.short_code == short_code)
        link = session.exec(statement).first()

        # Если ссылка найдена - логируем клик
        if link:
            log_click(link_id=link.id, request=request)

    # Делаем редирект (307 = временный редирект)
    return RedirectResponse(url=original_url)

@router.get("/{id}/clicks", response_model=ClickList)
def get_clicks(id: int, user_id: int = Depends(get_current_user)):
    """Получить все клики по ссылке"""
    # Проверяем, что ссылка принадлежит пользователю
    with Session(engine) as session:
        statement = select(Link).where(Link.id == id, Link.owner_id == user_id)
        link = session.exec(statement).first()

        # Если ссылка не найдена
        if not link:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")

    # Получаем клики
    clicks = get_link_clicks(link_id=id)

    # Конвертируем в ClickResponse
    clicks_response = [
        ClickResponse(
            id=click.id,
            ip=click.ip,
            user_agent=click.user_agent,
            browser=click.browser,
            device=click.device,
            created_at=click.created_at
        )
        for click in clicks
    ]

    return ClickList(clicks=clicks_response, total=len(clicks_response))

@router.delete("/{id}")
def delete_link(id: int, user_id: int = Depends(get_current_user)):
    # Удаляем ссылку
    success = delete_link_services(link_id=id, user_id=user_id)

    # Если нет
    if not success:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")

    return {
        "message": "Ссылка удалена"
    }