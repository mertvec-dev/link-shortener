import secrets
from jose import jwt, exceptions
from datetime import datetime, timezone, timedelta
from config import SECRET_KEY, ALGORITHM
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """Создает токен доступа (jwt)"""
    # Добавляем данные + срок действия
    payload = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta

    payload.update({"exp": expire})

    # Создать JWT-токен и подписать его
    token = jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)
    
    return token

def create_refresh_token() -> str:
    """Создает случайную строку из 64 символов"""
    return secrets.token_hex(32)

def verify_token(token: str) -> dict | None:
    """Возвращает данные из токена (dict) или None если токен невалиден"""
    try:
        # Пробуем раскодировать токен
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])

        return payload # возврат полезной нагрузки токена
    except (exceptions.ExpiredSignatureError, exceptions.JWTError):
        return None

# Создание схемы для Bearer токена
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """Получаем user_id текущего пользователя из jwt-токена"""
    token = credentials.credentials # Токен из заголовка

    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Токен невалиден или истек")

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Токен не содержит user_id")

    return user_id