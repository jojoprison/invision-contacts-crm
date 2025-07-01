#!/bin/bash

SCRIPT_NAME="update-containers.sh"

branch=$(git symbolic-ref --short HEAD)

if [ "$branch" == "dev" ] || [ "$branch" == "main" ]; then
  echo "[$SCRIPT_NAME] Обнаружена целевая ветка: $branch. Обновляем контейнеры..."

  docker-compose down
  docker-compose build
  docker-compose up -d
  
  echo "[$SCRIPT_NAME] Контейнеры успешно обновлены!"
else
  # был ли недавно влит PR в dev или main
  merge_to_dev=$(git log --merges -n 1 --grep="Merge" --grep="dev" | grep -c "^commit")
  merge_to_main=$(git log --merges -n 1 --grep="Merge" --grep="main" | grep -c "^commit")
  
  if [ $merge_to_dev -gt 0 ] || [ $merge_to_main -gt 0 ]; then
    echo "[$SCRIPT_NAME] Обнаружено недавнее слияние в dev или main. Обновляем контейнеры..."
    
    docker-compose down
    docker-compose build
    docker-compose up -d
    
    echo "[$SCRIPT_NAME] Контейнеры успешно обновлены после слияния PR!"
  else
    echo "[$SCRIPT_NAME] Текущая ветка: $branch (не dev/main), и нет недавних слияний. Обновление не требуется."
  fi
fi
