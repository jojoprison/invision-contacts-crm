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

### Шаг 2: Настройка переменных окружения

```bash
# Копирование примера .env файла
cp .env.example .env

# Отредактируйте .env файл в соответствии с вашими настройками
# Для Docker установки значения по умолчанию уже должны работать
```

### Шаг 3.1: Запуск через Docker Compose (рекомендуется)

```bash
# Сборка образов
docker-compose build

# Запуск всех сервисов
docker-compose up -d
```

> **Примечание:** Миграции и создание тенанта по умолчанию выполняются 
> автоматически при запуске контейнеров благодаря настройкам в docker-entrypoint.sh

### Шаг 3.2: Локальная установка с Poetry

```bash
# Обновление lock-файла
poetry lock

# Установка зависимостей
poetry install --with dev

# Применение миграций для основной схемы
cd src
poetry run python manage.py migrate
```

## Работа с тенантами (арендаторами)

### Создание нового тенанта

```bash
# Через Docker Compose
docker-compose exec web python src/manage.py create_tenant company1 "Company One"

# Локально с Poetry
cd src
poetry run python manage.py create_tenant company1 "Company One"
```

### Удаление тенанта

```bash
# Через Docker Compose
docker-compose exec web python src/manage.py delete_tenant company1

# Локально с Poetry
cd src
poetry run python manage.py delete_tenant company1
```

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
