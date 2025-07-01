#!/bin/bash

# Проверяем, что мы в ветке dev
branch=$(git symbolic-ref --short HEAD)

if [ "$branch" == "dev" ]; then
  echo "Обновляем контейнеры для ветки dev..."
  
  # Остановка и пересборка контейнеров
  docker-compose down
  docker-compose build
  docker-compose up -d
  
  echo "Контейнеры успешно обновлены!"
else
  echo "Текущая ветка: $branch (не dev). Обновление не требуется."
fi
