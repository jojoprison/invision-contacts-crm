# TODO: Доработки для Senior CRM

## Анализ ТЗ vs Текущая реализация

### ✅ Выполнено
- [x] Архитектура (api/services/repositories/models)
- [x] FastAPI async
- [x] SQLAlchemy 2.0 + Alembic
- [x] PostgreSQL + docker-compose
- [x] JWT access/refresh tokens
- [x] pydantic-settings
- [x] Кэширование аналитики (in-memory)
- [x] Все 7 моделей данных
- [x] Все бизнес-правила
- [x] Все API эндпоинты
- [x] RBAC (owner/admin/manager/member)
- [x] Базовые тесты

### ⚠️ Нужно доработать

#### 1. Инфраструктура и конфиги
- [ ] Dockerfile для приложения (production-ready)
- [ ] .env.sample (пример переменных окружения)
- [ ] .gitignore (специфичный для проекта)
- [ ] pytest.ini (конфиг pytest)
- [ ] mypy.ini или pyproject.toml секция (type checking)
- [ ] Расширить ruff конфиг в pyproject.toml
- [ ] .coveragerc (конфиг coverage)

#### 2. Тесты
- [ ] Полный интеграционный тест (полный сценарий из ТЗ):
      регистрация → создание организации → добавление участника → 
      создание контакта → сделки → задачи → аналитика
- [ ] Unit-тесты бизнес-правил (проверка ролей, валидаций)

#### 3. Улучшения кода
- [ ] py.typed marker файл (для typed package)
- [ ] Logging configuration
- [ ] CORS middleware (для фронтенда)

---

## Задачи (по порядку выполнения)

### Task 1: Инфраструктурные файлы
**Статус:** 🔄 В работе

### Task 2: Dockerfile  
**Статус:** ⏳ Ожидает

### Task 3: Полный интеграционный тест
**Статус:** ⏳ Ожидает

### Task 4: Финальные улучшения
**Статус:** ⏳ Ожидает
