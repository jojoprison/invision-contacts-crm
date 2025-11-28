.PHONY: install db db-stop db-clean migrate migrate-new run test lint format help

# Default target
help:
	@echo "Доступные команды:"
	@echo "  make install      - Установить зависимости"
	@echo "  make db           - Запустить PostgreSQL"
	@echo "  make db-stop      - Остановить PostgreSQL"
	@echo "  make db-clean     - Удалить PostgreSQL + данные"
	@echo "  make migrate      - Применить миграции"
	@echo "  make migrate-new  - Создать новую миграцию (MSG=описание)"
	@echo "  make run          - Запустить сервер (порт 8001)"
	@echo "  make test         - Запустить тесты"
	@echo "  make test-db      - Создать тестовую БД"
	@echo "  make lint         - Проверить код (ruff)"
	@echo "  make format       - Форматировать код (black)"

# Зависимости
install:
	uv sync

# База данных
db:
	docker-compose up -d

db-stop:
	docker-compose stop

db-clean:
	docker-compose down -v

# Миграции
migrate:
	uv run alembic upgrade head

migrate-new:
	uv run alembic revision --autogenerate -m "$(MSG)"

# Сервер
run:
	uv run uvicorn src.main:app --reload --port 8001

# Тесты
test-db:
	docker exec -it senior_crm-db-1 psql -U postgres -c "CREATE DATABASE senior_crm_test;" || true

test: test-db
	uv run pytest -v

# Линтеры
lint:
	uv run ruff check src/

format:
	uv run black src/
	uv run isort src/
