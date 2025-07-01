# Contacts CRM - Schema-based Multi-tenancy Service

CRM-сервис с контактами, использующий схема-ориентированную мультиарендность для изоляции данных организаций.

## Затраченное время

- Общее время выполнения: 14.1 ч. (846 мин.)

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

#### Создание суперпользователя для доступа к административной панели

```bash
# Создание суперпользователя Django
docker-compose exec web python src/manage.py createsuperuser
```

После создания суперпользователя вы получите доступ к административной панели по адресу http://localhost:8000/admin/

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

#### Создание суперпользователя для доступа к административной панели

```bash
# Создание суперпользователя Django (находясь в директории src)
poetry run python manage.py createsuperuser
```

После создания суперпользователя вы получите доступ к административной панели по адресу http://localhost:8000/admin/

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

## Примеры запросов API

### Создание контакта

```bash
curl -X POST http://localhost:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -H "X-SCHEMA: company1" \
  -d '{"name":"John Doe","email":"john@example.com","phone":"123-456-7890"}'
```

### Получение списка контактов

```bash
curl -X GET http://localhost:8000/api/contacts/ \
  -H "X-SCHEMA: company1"
```

### Фильтрация контактов по email

```bash
curl -X GET "http://localhost:8000/api/contacts/?email=john" \
  -H "X-SCHEMA: company1"
```

### Получение конкретного контакта

```bash
curl -X GET http://localhost:8000/api/contacts/550e8400-e29b-41d4-a716-446655440000 \
  -H "X-SCHEMA: company1"
```

### Обновление контакта

```bash
curl -X PUT http://localhost:8000/api/contacts/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -H "X-SCHEMA: company1" \
  -d '{"name":"John Smith","email":"john.smith@example.com","phone":"123-456-7890"}'
```

### Удаление контакта

```bash
curl -X DELETE http://localhost:8000/api/contacts/550e8400-e29b-41d4-a716-446655440000 \
  -H "X-SCHEMA: company1"
```

## Запуск тестов

### Базовый запуск тестов

```bash
# Через Docker Compose
docker-compose exec web pytest src/tests/

# Локально с Poetry
cd src
poetry run pytest tests/
```

### Запуск с проверкой покрытия кода

```bash
# Через Docker Compose (текущее покрытие > 90%)
docker-compose exec web pytest src/tests/ --cov=src --cov-report=term

# Локально с Poetry
cd src
poetry run pytest tests/ --cov=contacts --cov=tenants --cov-report=term-missing
```

> **Подробная информация:** Дополнительная документация по тестированию мультитенантной архитектуры доступна в [документации по тестированию](src/tests/README.md)

## Автоматизация обновления контейнеров

```bash
# Для автоматического обновления контейнеров
chmod +x setup-hooks.sh
./setup-hooks.sh
```

Эта команда активирует:
- pre-push хук: автообновление контейнеров при push в ветки dev или main
- post-merge хук: автообновление контейнеров при слиянии PR в ветки dev или main

> **ВАЖНО:** После мержа PR через интерфейс GitHub необходимо выполнить `git pull`
в локальном репозитории, чтобы активировать post-merge хук и автоматически обновить контейнеры

```bash
git pull
```

### Ручное обновление контейнеров

```bash
# Подготовка скрипта ручного обновления
chmod +x update-after-push.sh

# Запустить обновление после push в dev или main (для GitHub Desktop)
./update-after-push.sh
```

Этот скрипт обновляет контейнеры в следующих случаях:
- если текущая ветка dev или main
- если обнаружены недавние слияния PR в dev или main

## Использование Makefile

В проекте доступен Makefile для упрощения частых операций:

```bash
# Сборка образов
make build

# Запуск всех контейнеров
make up

# Остановка всех контейнеров
make down

# Просмотр логов в реальном времени
make logs

# Запуск Python shell
make shell

# Применение миграций
make migrate

# Создание суперпользователя
make createuser

# Создание нового тенанта (интерактивно)
make tenant

# Запуск тестов
make test

# Удаление контейнеров и томов
make clean

# Пересоздание окружения с нуля (clean + build + up)
make reset
```

## Настройка автоматизации (опционально)

### Для автоматического обновления контейнеров

```bash
chmod +x setup-hooks.sh
./setup-hooks.sh
````

Что это активирует:
- pre-push хук: автообновление контейнеров при push в ветки dev или main
- post-merge хук: автообновление контейнеров при слиянии PR в ветки dev или main

> **ВАЖНО:** После мержа PR через интерфейс GitHub необходимо выполнить git pull
в локальном репозитории, чтобы активировать post-merge хук и автоматически обновить контейнеры
```bash
git pull
```

## Для ручного обновления контейнеров

```bash
chmod +x update-after-push.sh
```

Этот скрипт обновляет контейнеры в следующих случаях:
- если текущая ветка `dev` или `main`
- если обнаружены недавние слияния `PR` в `dev` или `main`

## 🧪 Тестирование

## Подробная документация по тестированию мультитенантной архитектуры:
## [Документация по тестированию](src/tests/README.md)

``` bash
# Запуск тестов
docker-compose exec web pytest src/tests/

# Запуск тестов с подробным выводом
docker-compose exec web pytest src/tests/ -v

# Запуск с проверкой покрытия кода тестами (текущее покрытие > 90%)
docker-compose exec web pytest src/tests/ --cov=src --cov-report=term

# Генерация HTML-отчета о покрытии
docker-compose exec web pytest src/tests/ --cov=src --cov-report=html
```

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
