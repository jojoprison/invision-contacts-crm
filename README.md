# Contacts CRM - Schema-based Multi-tenancy Service

CRM-сервис с контактами, использующий схема-ориентированную мультиарендность для изоляции данных организаций.

## Затраченное время

- Общее время выполнения: 13.6 часов на момент 14:30

## Системные требования

### Вариант 1: Запуск через Docker (рекомендуется)
- Docker
- Docker Compose

### Вариант 2: Локальный запуск
- Python 3.11+
- Poetry 2.1.3+ (для управления зависимостями)
- PostgreSQL 14+
- Redis 7+ (для Celery)

## Установка и настройка

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/jojoprison/invision-contacts-crm.git
cd invision-contacts-crm
```

### Шаг 2.1: Запуск через Docker Compose (рекомендуется)

```bash
# Запуск всех сервисов
docker-compose up -d

# 3. Remove any existing venv and create a new one on 3.11
poetry env remove python  || true
poetry env use python3.11

# 4. Install dependencies (prod + dev)
poetry lock --no-update
poetry install --with dev

# 5. Настройка автоматизации (опционально)

# Для автоматического обновления контейнеров
chmod +x setup-hooks.sh
./setup-hooks.sh

# Что это активирует:
# - pre-push хук: автообновление контейнеров при push в ветки dev или main
# - post-merge хук: автообновление контейнеров при слиянии PR в ветки dev или main

# ВАЖНО: После мержа PR через интерфейс GitHub необходимо выполнить git pull
# в локальном репозитории, чтобы активировать post-merge хук и автоматически обновить контейнеры
git pull

# Для ручного обновления контейнеров
chmod +x update-after-push.sh
# Этот скрипт обновляет контейнеры в следующих случаях:
# - если текущая ветка dev или main
# - если обнаружены недавние слияния PR в dev или main

⸻

🧪 Тестирование

# Запуск тестов
docker-compose exec web pytest src/tests/

# Запуск тестов с подробным выводом
docker-compose exec web pytest src/tests/ -v

# Запуск с проверкой покрытия кода тестами (текущее покрытие > 90%)
docker-compose exec web pytest src/tests/ --cov=src --cov-report=term

# Генерация HTML-отчета о покрытии
docker-compose exec web pytest src/tests/ --cov=src --cov-report=html

# Подробная документация по тестированию мультитенантной архитектуры:
# [Документация по тестированию](src/tests/README.md)

⸻

🐳 Docker Development

# Используйте Makefile для основных операций

# Запустить все контейнеры
make up

# Остановить все контейнеры
make down

# Пересоздать окружение с нуля
make reset

# Создать нового тенанта
make tenant

# Создать суперпользователя
make createuser

# Запустить обновление после push в dev или main (для GitHub Desktop)
./update-after-push.sh
