#!/bin/bash

cat > .git/hooks/pre-push <<'EOF'
#!/bin/bash

branch=$(git symbolic-ref --short HEAD)

if [ "$branch" == "dev" ] || [ "$branch" == "main" ]; then
  echo "Обнаружен пуш в ветку $branch. Обновляем контейнеры..."

  docker-compose down
  docker-compose build
  docker-compose up -d
  
  echo "Контейнеры успешно обновлены!"
fi

# Разрешаем пуш (возврат 0)
exit 0
EOF

chmod +x .git/hooks/pre-push

cat > .git/hooks/post-merge <<'EOF'
#!/bin/bash

branch=$(git symbolic-ref --short HEAD)

if [ "$branch" == "dev" ] || [ "$branch" == "main" ]; then
  echo "Обнаружено слияние (merge) в ветку $branch. Обновляем контейнеры..."

  docker-compose down
  docker-compose build
  docker-compose up -d
  
  echo "Контейнеры успешно обновлены после слияния!"
fi

exit 0
EOF

chmod +x .git/hooks/post-merge

echo "Хуки установлены! Теперь при пуше или слиянии в ветки dev и main контейнеры будут автоматически обновляться."
