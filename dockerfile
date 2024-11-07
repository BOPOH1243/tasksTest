# Используем официальный Python-образ
FROM python:3.11-slim

# Устанавливаем необходимые пакеты и wait-for-it
RUN apt-get update && \
    apt-get install -y curl && \
    curl -o /usr/local/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем команду запуска
CMD ["wait-for-it", "postgres:5433", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
