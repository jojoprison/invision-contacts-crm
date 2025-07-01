#!/bin/bash

branch=$(git symbolic-ref --short HEAD)

if [ "$branch" == "dev" ] || [ "$branch" == "main" ]; then
  echo "Обновляем контейнеры для ветки $branch..."

  docker-compose down
  docker-compose build
  docker-compose up -d
  
  echo "Контейнеры успешно обновлены!"
else
  echo "Текущая ветка: $branch (не dev/main). Обновление не требуется."
fi
