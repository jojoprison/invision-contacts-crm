# Senior CRM — Progress & Cheatsheet

## Шпаргалка команд

```bash
cd senior_crm

# База данных
docker-compose up -d          # Поднять PostgreSQL
docker-compose down           # Остановить PostgreSQL
docker-compose down -v        # Остановить и удалить данные

# Миграции
uv run alembic revision --autogenerate -m "Описание"  # Создать миграцию
uv run alembic upgrade head                            # Применить миграции
uv run alembic downgrade -1                            # Откатить последнюю

# Сервер
uv run uvicorn src.main:app --reload                   # Запустить dev-сервер

# Тесты
uv run pytest                                          # Запустить все тесты
uv run pytest -v                                       # Verbose
uv run pytest tests/test_services.py -v               # Конкретный файл

# Линтеры
uv run ruff check src/                                 # Проверка кода
uv run black src/                                      # Форматирование
```

---

## План разработки

### Шаг 1: Инфраструктура и Модели ✅
- [x] Структура проекта (api, services, repositories, models, core)
- [x] pyproject.toml (uv, зависимости)
- [x] docker-compose.yml (PostgreSQL на порту 5433)
- [x] Alembic конфигурация (async)
- [x] SQLAlchemy модели:
  - [x] User
  - [x] Organization
  - [x] OrganizationMember
  - [x] Contact
  - [x] Deal
  - [x] Task
  - [x] Activity
- [x] Enums (UserRole, DealStatus, DealStage, ActivityType)
- [x] Первая миграция применена

### Шаг 2: Репозитории (Data Access Layer) ✅
- [x] BaseRepository (generic CRUD)
- [x] UserRepository
- [x] OrganizationRepository
- [x] ContactRepository
- [x] DealRepository (+ analytics queries)
- [x] TaskRepository
- [x] ActivityRepository

### Шаг 3: Сервисы (Business Logic) ✅
- [x] AuthService (регистрация, логин, JWT)
- [x] OrganizationService (RBAC, membership)
- [x] ContactService (CRUD + ownership checks)
- [x] DealService (валидации: amount>0 для won, запрет отката stage)
- [x] TaskService (валидация due_date не в прошлом)
- [x] ActivityService (автосоздание при смене статуса)
- [x] AnalyticsService (summary, funnel + in-memory cache)
- [x] core/security.py (JWT, password hashing)
- [x] core/exceptions.py (custom exceptions)

### Шаг 4: API Layer ✅
- [x] Pydantic Schemas (Request/Response)
- [x] Dependencies (get_current_user, get_organization_context)
- [x] Auth endpoints (register, login, refresh)
- [x] Organizations endpoints (/me)
- [x] Contacts endpoints (CRUD + search + pagination)
- [x] Deals endpoints (CRUD + filters + sorting)
- [x] Tasks endpoints
- [x] Activities endpoints (timeline + comments)
- [x] Analytics endpoints (summary, funnel)
- [x] Error handler (AppException)
- [x] main.py (FastAPI app)

### Шаг 5: Безопасность и Роли ✅ (integrated in services)
- [x] JWT access/refresh tokens
- [x] Role-based access control (RBAC)
- [x] X-Organization-Id header validation
- [x] Permission checks (owner/admin/manager/member)

### Шаг 6: Тесты ✅
- [x] conftest.py (fixtures, test DB)
- [x] test_auth.py (register, login)
- [x] test_deals.py (create, status validation, activity creation)
- [x] test_tasks.py (create, due_date validation)

### Шаг 7: Финализация ✅
- [x] Кэширование (in-memory для аналитики) — в AnalyticsService
- [x] Error handling (унифицированный формат) — AppException handler
- [x] README.md (архитектура, API docs, бизнес-правила)
- [x] Финальная проверка — сервер запускается

---

## Текущий статус

**Статус:** ✅ ГОТОВО

**Что сделано:**
- Полный backend для multi-tenant CRM
- 7 таблиц в PostgreSQL
- JWT авторизация с ролями
- Все бизнес-правила реализованы
- Тесты написаны
- Документация готова

**Сервер:** http://localhost:8001/docs
