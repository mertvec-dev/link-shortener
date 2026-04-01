from fastapi import FastAPI
from database.database import init_db
from api.auth import router as auth_router
from api.links import router as links_router
from api.pages import router as pages_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Link Shortener API",
    description="Сокращатель ссылок на FastAPI + PostgreSQL + Docker",
    version="1.0.0",
    lifespan=lifespan
)

# Подключение роутеров
app.include_router(auth_router)   # API авторизации
app.include_router(links_router)  # API ссылок (/links/...)
app.include_router(pages_router)  # Страницы (главная, логин, регистрация)

@app.get("/")
def root():
    return "Добро пожаловать в Link Shortener API"