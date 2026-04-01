# Базовый образ с Python
FROM python:3.11-slim

# Рабочая директория в контейнере
WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Порт, который слушает приложение
EXPOSE 8000

# Команда запуска (0.0.0.0 = слушать все интерфейсы)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
