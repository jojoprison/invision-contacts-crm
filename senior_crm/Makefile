.PHONY: install db db-stop db-clean migrate migrate-new run test test-cov lint format typecheck docker-build help

# Default target
help:
	@echo "Доступные команды:"
	@echo ""
	@echo "  Установка:"
	@echo "    make install      - Установить зависимости"
	@echo ""
	@echo "  База данных:"
	@echo "    make db           - Запустить PostgreSQL"
	@echo "    make db-stop      - Остановить PostgreSQL"
	@echo "    make db-clean     - Удалить PostgreSQL + данные"
	@echo ""
	@echo "  Миграции:"
	@echo "    make migrate      - Применить миграции"
	@echo "    make migrate-new  - Создать миграцию (MSG=описание)"
	@echo ""
	@echo "  Разработка:"
	@echo "    make run          - Запустить сервер (порт 8001)"
	@echo ""
	@echo "  Тесты:"
	@echo "    make test         - Запустить тесты"
	@echo "    make test-cov     - Тесты с coverage"
	@echo ""
	@echo "  Качество кода:"
	@echo "    make lint         - Проверить код (ruff)"
	@echo "    make format       - Форматировать код (black + isort)"
	@echo "    make typecheck    - Проверить типы (mypy)"
	@echo ""
	@echo "  Docker:"
	@echo "    make docker-build - Собрать Docker образ"

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

# Тесты с coverage
test-cov: test-db
	uv run pytest --cov=src --cov-report=html --cov-report=term -v

# Линтеры
lint:
	uv run ruff check src/

format:
	uv run black src/
	uv run isort src/

# Type checking
typecheck:
	uv run mypy src/

# Docker
docker-build:
	docker build -t senior-crm:latest .
