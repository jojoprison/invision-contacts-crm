# Requirements → Implementation Mapping

Этот документ показывает, как пункты тестового задания (Senior Python: мини-CRM) отражены в коде проекта **senior_crm**.

---

## 1. Архитектура и стек

### 1.1 Архитектурное мышление, слои, модули, зависимости
- **Требование:** разделение на слои: api / services / repositories / models; не смешивать HTTP и бизнес-логику.
- **Реализация:**
  - `src/api/` – HTTP-слой:
    - `src/api/deps.py` – зависимости (auth, org context).
    - `src/api/v1/*.py` – роутеры.
  - `src/services/` – бизнес-логика:
    - `auth.py`, `organization.py`, `contact.py`, `deal.py`, `task.py`, `activity.py`, `analytics.py`.
  - `src/repositories/` – доступ к БД: `base.py` + entity repos.
  - `src/models/` – ORM модели: `auth.py`, `crm.py`, `enums.py`.
  - `src/core/` – настройки, безопасность, исключения.

### 1.2 Стек: FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT
- **FastAPI (async):**
  - `src/main.py` – создание приложения, CORS, логирование, роуты.
  - Все эндпоинты в `src/api/v1/` – `async def`.

- **SQLAlchemy 2.0 (Async ORM):**
  - `src/core/database.py` – async engine, `AsyncSessionLocal`, `Base`.
  - `src/models/*.py` – Declarative ORM модели.

- **Alembic (миграции):**
  - `alembic/env.py`, `alembic.ini`, `alembic/versions/*` – конфигурация и миграции.

- **PostgreSQL:**
  - `docker-compose.yml` – сервис `db` (PostgreSQL на 5433).
  - URL берётся из `src/core/config.py` (`settings.SQLALCHEMY_DATABASE_URI`).

- **JWT-аутентификация (access/refresh):**
  - `src/core/security.py` – `create_access_token`, `create_refresh_token`, `decode_token`, hashing.
  - `src/services/auth.py` – логика регистрации, логина, refresh, текущий пользователь.
  - `src/api/v1/auth.py` – эндпоинты `/auth/register`, `/auth/login`, `/auth/refresh`.

- **Настройки через pydantic-settings:**
  - `src/core/config.py` – класс `Settings`, чтение ENV, DSN для БД, секреты JWT.

- **docker / docker-compose:**
  - `docker-compose.yml` – БД.
  - `Dockerfile` – production-образ приложения на базе `uv`.

- **Аннотации типов + mypy/ruff:**
  - Типы во всех публичных интерфейсах сервисов/репозиториев.
  - `pyproject.toml` – секции `[tool.mypy]`, `[tool.ruff]`, `[tool.pytest.ini_options]`.

- **Кэширование (in-memory):**
  - `src/services/analytics.py` – простой in-memory кэш аналитики на N секунд.

---

## 2. Модель данных

### 2.1 Organization
- **Требование:** id, name, created_at.
- **Реализация:** `src/models/auth.py::Organization`.

### 2.2 User
- **Требование:** id, email (уникальный), hashed_password, name, created_at.
- **Реализация:** `src/models/auth.py::User`.

### 2.3 OrganizationMember
- **Требование:** organization_id, user_id, role (owner, admin, manager, member), уникальность пары.
- **Реализация:**
  - Модель: `src/models/auth.py::OrganizationMember`.
  - Enum ролей: `src/models/enums.py::UserRole`.
  - Уникальный индекс: `UniqueConstraint('organization_id', 'user_id', ...)` внутри модели.

### 2.4 Contact
- **Требование:** organization_id, owner_id, name, email, phone, created_at.
- **Реализация:** `src/models/crm.py::Contact`.

### 2.5 Deal
- **Требование:** org, contact, owner, title, amount (decimal), currency, status, stage, created_at, updated_at.
- **Реализация:**
  - Модель: `src/models/crm.py::Deal`.
  - Enums: `src/models/enums.py::{DealStatus, DealStage}`.

### 2.6 Task
- **Требование:** deal_id, title, description, due_date, is_done, created_at.
- **Реализация:** `src/models/crm.py::Task`.

### 2.7 Activity
- **Требование:** deal_id, author_id (nullable), type, payload (JSONB), created_at.
- **Реализация:**
  - Модель: `src/models/crm.py::Activity`.
  - Enum типов: `src/models/enums.py::ActivityType`.

---

## 3. Multi-tenant и роли

### 3.1 Контекст организации (X-Organization-Id)
- **Требование:** пользователь работает в контексте одной организации; заголовок `X-Organization-Id`.
- **Реализация:**
  - `src/api/deps.py`:
    - `get_organization_id` – читает `X-Organization-Id`.
    - `get_organization_context` – проверяет membership пользователя в организации.
  - Все роуты, где нужен контекст организации, принимают `organization_id: OrgId`.

### 3.2 Роли и права
- **Требование:** owner/admin могут всё, manager – всё кроме настроек, member – только свои сущности; 403/404 при нарушении.
- **Реализация:**
  - `src/services/organization.py`:
    - `get_membership` – проверка, что пользователь – член организации.
    - `check_permission` – проверка ролей.
    - `can_manage_all`, `can_modify_settings` – хелперы.
  - `src/services/contact.py`, `deal.py`, `task.py` – проверки owner vs member через `can_manage_all` и сравнение `owner_id`.
  - Ошибки 403/404 реализованы через `src/core/exceptions.py` и маппинг в роутерах (HTTPException).

---

## 4. Правила по сделкам и задачам

### 4.1 Нельзя закрыть сделку как won, если amount <= 0
- **Реализация:**
  - `src/services/deal.py::DealService._validate_status_change` – проверка `amount > 0` при `new_status == DealStatus.WON`.
  - Тесты: `tests/test_deals.py::test_cannot_win_deal_with_zero_amount` и `tests/test_integration.py::test_business_rule_won_requires_positive_amount`.

### 4.2 Нельзя удалить контакт, если есть сделки
- **Реализация:**
  - `src/repositories/contact.py::has_deals` – проверка наличия сделок.
  - `src/services/contact.py::delete_contact` – выбрасывает `ConflictError` при наличии сделок.
  - Тесты: `tests/test_integration.py::test_full_crm_scenario` (конец сценария – ожидается 409).

### 4.3 member не может создать задачу для чужой сделки
- **Реализация:**
  - `src/services/task.py::create_task` – проверка роли и `deal.owner_id` против текущего пользователя.

### 4.4 due_date не может быть в прошлом
- **Реализация:**
  - `src/services/task.py::_validate_due_date` – сравнение с текущей датой.
  - Тесты: `tests/test_tasks.py::test_cannot_create_task_with_past_due_date` и `tests/test_integration.py::test_business_rule_task_due_date_not_in_past`.

### 4.5 Переход стадии сделки, запрет отката, Activity
- **Реализация:**
  - `src/services/deal.py::DealService._validate_stage_change` – запрет отката для ролей ниже admin/owner.
  - `DealService.update_deal` – создание записей в `ActivityRepository` при изменении статуса/стадии.
  - Тесты: `tests/test_deals.py::test_deal_status_change_creates_activity`, `tests/test_integration.py::test_full_crm_scenario` (проверка `stage_changed` и `status_changed`).

### 4.6 Организационный контекст (никаких cross-org ссылок)
- **Реализация:**
  - `DealService.create_deal` – проверка, что `contact.organization_id == organization_id`.
  - `TaskService.get_task` / `create_task` – проверка, что `deal.organization_id == organization_id`.
  - Все сервисы получают и проверяют `organization_id` явно.

---

## 5. Аналитика / отчёты

### 5.1 /analytics/deals/summary
- **Требование:**
  - количество сделок по статусам,
  - сумма amount по статусам,
  - средний amount по `won`,
  - количество новых за N дней.
- **Реализация:**
  - Репозиторий: `src/repositories/deal.py::get_summary`.
  - Сервис: `src/services/analytics.py::get_deals_summary` (форматирует ответ + кэширует).
  - API: `src/api/v1/analytics.py::get_deals_summary`.

### 5.2 /analytics/deals/funnel
- **Требование:**
  - кол-во сделок по стадиям в разрезе статусов,
  - конверсия из предыдущей стадии в следующую.
- **Реализация:**
  - Репозиторий: `src/repositories/deal.py::get_funnel`.
  - Сервис: `src/services/analytics.py::get_deals_funnel`.
  - API: `src/api/v1/analytics.py::get_deals_funnel`.

---

## 6. Структура API (пример из ТЗ)

### 6.1 Аутентификация
- **Требование:** `/auth/register`, `/auth/login`, `/auth/refresh`.
- **Реализация:**
  - API: `src/api/v1/auth.py`.
  - Сервисы: `src/services/auth.py`.
  - Схемы: `src/schemas/auth.py`.

### 6.2 Организации и участники
- **Требование:** `/organizations/me`.
- **Реализация:**
  - API: `src/api/v1/organizations.py`.
  - Сервис: `src/services/organization.py::get_user_organizations`.

### 6.3 Контакты
- **Требование:** `/contacts` c page, page_size, search, owner_id.
- **Реализация:**
  - API: `src/api/v1/contacts.py` (Query-параметры, pagination + search).
  - Сервис: `src/services/contact.py::get_contacts` (фильтрация, owner_id с учётом ролей).
  - Репозиторий: `src/repositories/contact.py`.

### 6.4 Сделки
- **Требование:** `/deals` с page/page_size/status/stage/owner_id/min/max/order_by/order.
- **Реализация:**
  - API: `src/api/v1/deals.py::get_deals` (все параметры из ТЗ).
  - Сервис: `src/services/deal.py::get_deals`.
  - Репозиторий: `src/repositories/deal.py::get_by_organization`.

### 6.5 Задачи
- **Требование:** `/tasks` с deal_id, only_open, due_before, due_after.
- **Реализация:**
  - API: `src/api/v1/tasks.py::get_tasks`.
  - Сервис: `src/services/task.py::get_tasks`.
  - Репозиторий: `src/repositories/task.py`.

### 6.6 Активности
- **Требование:** `/deals/{id}/activities` GET/POST (только type="comment" руками).
- **Реализация:**
  - API: `src/api/v1/activities.py`.
  - Сервис: `src/services/activity.py`.
  - Restriction "only comment" – проверка в `create_activity` (400 при другом type).

---

## 7. Тесты и качество кода

### 7.1 Unit-тесты и интеграционные тесты
- **Unit / rules:**
  - `tests/test_deals.py` – правила по amount/status/stage, activity.
  - `tests/test_tasks.py` – due_date, изменение статуса задачи.

- **Интеграционные:**
  - `tests/test_integration.py::test_full_crm_scenario` – полный сценарий (регистрация → орг → контакт → сделка → задача → активность → аналитика → конфликт удаления контакта).
  - Доп. проверки правил: `test_business_rule_won_requires_positive_amount`, `test_business_rule_task_due_date_not_in_past`.

- **Фикстуры:**
  - `tests/conftest.py` – async-клиент, временная тестовая БД, переопределение `get_db`.

### 7.2 Линтеры, типизация, coverage
- **Линтеры:**
  - `pyproject.toml` – `tool.ruff`, `tool.isort`.
  - Makefile: `make lint`, `make format`.

- **Типизация / mypy:**
  - `pyproject.toml` – `[tool.mypy]`.
  - `src/py.typed` – пакет помечен как typed.

- **Coverage:**
  - `.coveragerc`, `[tool.coverage.run]` в `pyproject.toml`.
  - Makefile: `make test-cov`.

---

## 8. Утилиты и DX (Developer Experience)

- **Makefile:** удобные команды (см. README, секция "Useful Commands").
- **Seed script:** `src/scripts/seed.py` + `make seed` – быстрый старт для ревьюера.
- **Wait for DB:** `src/scripts/wait_for_db.py` + `make wait-db`.
- **Документация:** `README.md`, `FINAL_CHECKLIST.md`, `TODO.md`, `REQUIREMENTS_MAPPING.md`.
