# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения
COPY . /app/

# Открываем порт
EXPOSE 5000

# Команда для запуска Flask-приложения
CMD ["python", "app.py"]
