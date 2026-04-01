from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.jwt_utils import verify_token
from typing import Optional

router = APIRouter(tags=["Страницы"])

# Настройка Jinja2
templates = Jinja2Templates(directory="templates")


# Проверка авторизации
def get_auth_status(request: Request) -> bool:
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "")
        payload = verify_token(token)
        return payload is not None
    return False


# Главная страница
@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    is_auth = get_auth_status(request)
    return templates.TemplateResponse(request=request, name="home.html", context={
        "is_authenticated": is_auth
    })


# Страница регистрации
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    is_auth = get_auth_status(request)
    return templates.TemplateResponse(request=request, name="register.html", context={
        "is_authenticated": is_auth
    })


# Страница входа
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    is_auth = get_auth_status(request)
    return templates.TemplateResponse(request=request, name="login.html", context={
        "is_authenticated": is_auth
    })


# Страница создания ссылки
@router.get("/shorten", response_class=HTMLResponse)
async def shorten_page(request: Request):
    is_auth = get_auth_status(request)
    return templates.TemplateResponse(request=request, name="shorten.html", context={
        "is_authenticated": is_auth
    })


# Страница моих ссылок
@router.get("/my-links", response_class=HTMLResponse)
async def my_links_page(request: Request):
    is_auth = get_auth_status(request)
    return templates.TemplateResponse(request=request, name="my-links.html", context={
        "is_authenticated": is_auth
    })


# Страница статистики кликов
@router.get("/click-stats/{link_id}/{short_code}", response_class=HTMLResponse)
async def click_stats_page(request: Request, link_id: int, short_code: str):
    is_auth = get_auth_status(request)
    return templates.TemplateResponse(request=request, name="click-stats.html", context={
        "is_authenticated": is_auth,
        "link_id": link_id,
        "short_code": short_code
    })


# Страница выхода
@router.get("/logout", response_class=HTMLResponse)
async def logout_page(request: Request):
    return templates.TemplateResponse(request=request, name="logout.html", context={
        "is_authenticated": False
    })
