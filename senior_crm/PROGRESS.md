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

### Шаг 3: Сервисы (Business Logic) 🔄
- [ ] AuthService (регистрация, логин, JWT)
- [ ] OrganizationService
- [ ] ContactService
- [ ] DealService (валидации: amount>0 для won, запрет отката stage)
- [ ] TaskService (валидация due_date не в прошлом)
- [ ] ActivityService (автосоздание при смене статуса)
- [ ] AnalyticsService (summary, funnel)

### Шаг 4: API Layer ⏳
- [ ] Pydantic Schemas (Request/Response)
- [ ] Dependencies (get_current_user, get_organization_context)
- [ ] Auth endpoints (register, login, refresh)
- [ ] Organizations endpoints
- [ ] Contacts endpoints (CRUD + search + pagination)
- [ ] Deals endpoints (CRUD + filters + sorting)
- [ ] Tasks endpoints
- [ ] Activities endpoints
- [ ] Analytics endpoints

### Шаг 5: Безопасность и Роли ⏳
- [ ] JWT access/refresh tokens
- [ ] Role-based access control (RBAC)
- [ ] X-Organization-Id header validation
- [ ] Permission checks (owner/admin/manager/member)

### Шаг 6: Тесты ⏳
- [ ] Unit-тесты сервисов
- [ ] Integration-тесты API (полный сценарий)
- [ ] Fixtures для тестовой БД

### Шаг 7: Финализация ⏳
- [ ] Кэширование (in-memory для аналитики)
- [ ] Error handling (унифицированный формат)
- [ ] README.md (архитектура, запуск)
- [ ] Финальная проверка

---

## Текущий статус

**Активный шаг:** 2 — Репозитории

**Последнее действие:** Применена Initial migration, все таблицы созданы.
