# Використовуємо офіційний образ Python
FROM python:3.14-slim

# Встановлюємо змінні середовища
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл залежностей та встановлюємо їх
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проєкт
COPY . .

# Відкриваємо порт 8000
EXPOSE 8000

# Команда для запуску
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]