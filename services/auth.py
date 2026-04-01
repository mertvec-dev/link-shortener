from database.models.user import User
from database.models.refresh_token import RefreshToken
from database.database import engine
from sqlmodel import Session, select
from utils.jwt_utils import create_access_token, create_refresh_token
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_user_exists(username: str = None, email: str = None) -> bool:
    """
    Проверяет, существует ли пользователь с таким ником или почтой
    Возвращает True если существует, False если нет
    """
    with Session(engine) as session:
        if username:
            statement = select(User).where(User.username == username)
            user = session.exec(statement).first()
            if user:
                return True

        if email:
            statement = select(User).where(User.email == email)
            user = session.exec(statement).first()
            if user:
                return True

        return False


def register_user(username: str, password: str, email: str) -> User:
    """
    Зарегистрировать нового пользователя
    Возвращает созданного пользователя
    """
    # Хешируем пароль
    hashed_password = pwd_context.hash(password)

    with Session(engine) as session:
        # Создаем пользователя
        user = User(username=username, password=hashed_password, email=email)

        # Добавляем пользователя
        session.add(user)

        # Сохраняем изменения
        session.commit()

        # Обновляем объект, чтобы получить id
        session.refresh(user)

        return user


def login_user(username: str, password: str) -> dict | None:
    """
    Войти пользователя
    Возвращает токены или None если ошибка
    """
    with Session(engine) as session:
        # Находим пользователя по username
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()

        # Если не найден
        if not user:
            return None

        # Проверяем пароль
        if not pwd_context.verify(password, user.password):
            return None

        # Создаем токены
        access_token = create_access_token(
            data={"user_id": user.id},
            expires_delta=timedelta(minutes=30)
        )
        refresh_token_str = create_refresh_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        # Создаем объект модели
        db_refresh_token = RefreshToken(
            user_id=user.id,
            refresh_token=refresh_token_str,
            expires_at=expires_at
        )

        session.add(db_refresh_token)
        session.commit()

        # Возврат токенов
        return {
            "access_token": access_token,
            "refresh_token": refresh_token_str
        }


def refresh_token(token: str) -> dict | None:
    """
    Обновить access токен
    Возвращает новый access токен и refresh токен или None если ошибка
    """
    with Session(engine) as session:
        # Получаем токен из БД
        statement = select(RefreshToken).where(RefreshToken.refresh_token == token)
        db_token = session.exec(statement).first()

        # Если не найден
        if not db_token:
            return None

        # Проверяем истек или нет (сравниваем с UTC временем)
        now = datetime.now(timezone.utc)
        
        # Если expires_at без timezone - предполагаем UTC
        expires_at = db_token.expires_at
        if expires_at.tzinfo is None:
            # Делаем timezone-aware (предполагаем UTC)
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        if expires_at < now:
            return None

        # Создаем новый access_token
        new_access = create_access_token(
            data={"user_id": db_token.user_id},
            expires_delta=timedelta(minutes=30)
        )
        
        # Создаем новый refresh_token
        new_refresh = create_refresh_token()
        new_expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        
        # Обновляем refresh_token в БД
        db_token.refresh_token = new_refresh
        db_token.expires_at = new_expires_at
        session.commit()

        return {
            "access_token": new_access,
            "refresh_token": new_refresh
        }