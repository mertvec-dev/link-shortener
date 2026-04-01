from fastapi import APIRouter, HTTPException, Response
from schemas.auth import UserRegister, UserLogin, UserResponse, Token, RefreshTokenRequest
from services import auth as auth_service
from utils.password_validator import validate_password

router = APIRouter(prefix="/auth", tags=["Авторизация"])

@router.post("/register", response_model=Token)
def register(user: UserRegister):
    # Проверка на существующего пользователя
    if auth_service.check_user_exists(username=user.username):
        raise HTTPException(status_code=400, detail="Такой username уже занят")

    if auth_service.check_user_exists(email=user.email):
        raise HTTPException(status_code=400, detail="Такой email уже занят")

    # Валидация пароля
    if not validate_password(user.password):
        raise HTTPException(
            status_code=400,
            detail="Пароль должен быть не менее 8 символов, содержать хотя бы одну цифру и заглавную букву"
        )

    # Зарегистрировать пользователя
    new_user = auth_service.register_user(
        username=user.username,
        password=user.password,
        email=user.email
    )

    # Автоматический вход (создать токены)
    tokens = auth_service.login_user(user.username, user.password)

    return tokens

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    tokens = auth_service.login_user(
        username=user.username,
        password=user.password
    )

    # Если ошибка, т.е None
    if not tokens:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    return tokens

@router.post("/refresh", response_model=Token)
def refresh(token_request: RefreshTokenRequest):
    new_token = auth_service.refresh_token(token_request.refresh_token)

    # Если ошибка
    if not new_token:
        raise HTTPException(status_code=401, detail="Токен невалиден или истек")

    return new_token


@router.post("/logout")
def logout():
    """Выход из системы (очистка токенов на клиенте)"""
    return {"message": "Вы успешно вышли из системы"}
