# LINK SHORTENER — Сокращатель ссылок

## 🔗 Описание

Веб-сервис для сокращения ссылок с JWT-аутентификацией, статистикой переходов и современным веб-интерфейсом.

---

## ✨ Возможности

- ✂️ Сокращение длинных ссылок
- 📊 Статистика переходов (клики)
- 📈 Детальная статистика кликов (IP, браузер, устройство)
- 🔐 JWT аутентификация (Access + Refresh токены)
- 🗄️ PostgreSQL + Docker
- 📱 Адаптивный веб-интерфейс
- 🚀 Автоматический редирект

---

## 🚀 Запуск проекта

### Вариант 1: Docker (рекомендуется)

1. **Установи Docker Desktop:**
   https://www.docker.com/products/docker-desktop/

2. **Установи зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Запусти контейнеры:**
   ```bash
   docker-compose up -d
   ```

4. **Открой в браузере:**
   http://localhost:8000

---

### Вариант 2: Локальный запуск

1. **Установи Python 3.11+:**
   https://www.python.org/downloads/

2. **Установи зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Установи PostgreSQL:**
   https://www.postgresql.org/download/

4. **Создай базу данных:**
   ```sql
   CREATE DATABASE linkdb;
   ```

5. **Скопируй `.env.example` в `.env` и настрой:**
   ```bash
   cp .env.example .env
   ```

6. **Запусти сервер:**
   ```bash
   uvicorn main:app --reload
   ```

7. **Открой в браузере:**
   http://localhost:8000

---

## 📚 Документация

**Swagger UI (API документация):**
http://localhost:8000/docs

---

## 🌐 Веб-интерфейс

| Страница | URL |
|----------|-----|
| Главная | http://localhost:8000 |
| Вход | http://localhost:8000/login |
| Регистрация | http://localhost:8000/register |
| Создать ссылку | http://localhost:8000/shorten |
| Мои ссылки | http://localhost:8000/my-links |
| Статистика кликов | http://localhost:8000/click-stats/{id}/{code} |

---

## 🔧 API Endpoints

### Авторизация
- `POST /auth/register` — Регистрация
- `POST /auth/login` — Вход
- `POST /auth/refresh` — Обновление токена

### Ссылки
- `POST /links/shorten` — Создать ссылку (требуется токен)
- `GET /links/{code}` — Редирект (без токена)
- `GET /links/my` — Мои ссылки (требуется токен)
- `GET /links/{id}/clicks` — Статистика кликов по ссылке (требуется токен)
- `DELETE /links/{id}` — Удалить ссылку (требуется токен)

---

## 🛠️ Технологии

| Компонент | Технология |
|-----------|------------|
| Backend | FastAPI + Python |
| ORM | SQLModel |
| База данных | PostgreSQL 15 |
| Контейнеризация | Docker + Docker Compose |
| Аутентификация | JWT (Access + Refresh) |
| Валидация | Pydantic |
| Шаблоны | Jinja2 |

---

## 📁 Структура проекта

```
link shortener/
├── main.py              # Точка входа
├── config.py            # Настройки
├── database.py          # Подключение к БД
├── database/
│   ├── models/          # Модели данных (таблицы)
│   │   ├── user.py      # Модель пользователя
│   │   ├── link.py      # Модель ссылки
│   │   ├── click.py     # Модель клика
│   │   └── refresh_token.py
│   └── database.py      # Движок БД
├── api/
│   ├── auth.py          # Роуты авторизации
│   ├── links.py         # Роуты ссылок
│   └── pages.py         # Роуты страниц
├── services/
│   ├── auth.py          # Логика авторизации
│   └── links.py         # Логика ссылок
├── schemas/
│   ├── auth.py          # Схемы авторизации
│   └── links.py         # Схемы ссылок
├── utils/
│   ├── jwt.py           # JWT утилиты
│   └── url.py           # Генерация кодов
├── templates/
│   ├── base.html        # Базовый шаблон
│   ├── home.html        # Главная
│   ├── login.html       # Вход
│   ├── register.html    # Регистрация
│   ├── shorten.html     # Создать ссылку
│   ├── my-links.html    # Мои ссылки
│   ├── click-stats.html # Статистика кликов
│   └── logout.html      # Выход
├── docker-compose.yml   # Docker конфигурация
├── Dockerfile           # Образ приложения
├── requirements.txt     # Зависимости Python
├── .env.example         # Шаблон переменных
└── README.md            # Этот файл
```

---

## 🔑 Пример использования

### 1. Регистрация
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "ValidPass123", "email": "test@example.com"}'
```

### 2. Вход
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "ValidPass123"}'
```

### 3. Создать ссылку
```bash
curl -X POST http://localhost:8000/links/shorten \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <токен>" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### 4. Редирект
```
Открой в браузере: http://localhost:8000/links/{short_code}

> Мной написано 80% кода
> 20% кода написано с помощью ИИ (страницы, отладка, docstring)