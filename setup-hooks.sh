#!/bin/bash

# Создаем pre-push хук
cat > .git/hooks/pre-push <<'EOF'
#!/bin/bash

branch=$(git symbolic-ref --short HEAD)

if [ "$branch" == "dev" ]; then
  echo "Обнаружен пуш в ветку dev. Обновляем контейнеры..."
  
  # Остановка и пересборка контейнеров
  docker-compose down
  docker-compose build
  docker-compose up -d
  
  echo "Контейнеры успешно обновлены!"
fi

# Разрешаем пуш (возврат 0)
exit 0
EOF

chmod +x .git/hooks/pre-push

echo "Pre-push хук установлен! Теперь при пуше в ветку dev контейнеры будут автоматически обновляться."
