#!/bin/bash

# Остановка и удаление существующих контейнеров
echo "Остановка и удаление существующих контейнеров..."
docker-compose down

# Удаление старой базы данных, если нужно пересоздать (опционально)
if [ -f "./books.db" ]; then
    echo "Удаление старой базы данных..."
    rm ./books.db
fi

# Сборка Docker-образов
echo "Сборка Docker-образов..."
docker-compose build

# Запуск контейнеров в фоне
echo "Запуск контейнеров..."
docker-compose up -d

# Применение миграций
echo "Применение миграций..."
docker exec backend flask db init || true  # Если директория миграций уже существует, пропускаем init
docker exec backend flask db migrate -m "Initial migration"
docker exec backend flask db upgrade

# Вывод состояния контейнеров
echo "Проверка состояния контейнеров..."
docker-compose ps

echo "Проект успешно собран и запущен!"
