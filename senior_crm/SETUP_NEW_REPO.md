# Инструкция: Перенос в отдельный Git-репозиторий

Эта инструкция описывает, как вынести `senior_crm` в отдельный репозиторий.

---

## Шаг 1: Создать новый репозиторий

### На GitHub/GitLab:
1. Зайди на GitHub → **New repository**
2. Название: `senior-crm` (или `mini-crm-senior-test`)
3. **Не добавляй** README, .gitignore, LICENSE (у нас уже всё есть)
4. Скопируй URL репозитория, например:
   ```
   git@github.com:YOUR_USERNAME/senior-crm.git
   ```

---

## Шаг 2: Подготовить папку

### Вариант A: Скопировать в новое место (рекомендуется)
```bash
# Из текущей директории проекта
cp -r senior_crm ~/projects/senior-crm
cd ~/projects/senior-crm
```

### Вариант B: Переместить
```bash
mv senior_crm ~/projects/senior-crm
cd ~/projects/senior-crm
```

---

## Шаг 3: Инициализировать Git

```bash
# Убедись, что ты в папке senior-crm
pwd  # должно показать .../senior-crm

# Инициализация нового репозитория
git init

# Добавить все файлы
git add .

# Первый коммит
git commit -m "Initial commit: Senior CRM implementation"

# Подключить remote
git remote add origin git@github.com:YOUR_USERNAME/senior-crm.git

# Запушить
git branch -M main
git push -u origin main
```

---

## Шаг 4: Настроить окружение

```bash
# 1. Скопировать .env
cp .env.sample .env

# 2. (Опционально) Отредактировать .env
#    - SECRET_KEY: сгенерировать надёжный ключ
#    - Остальное можно оставить для локальной разработки

# 3. Установить зависимости
make install
# или: uv sync

# 4. Запустить PostgreSQL
make db
# или: docker-compose up -d

# 5. Подождать готовности БД
make wait-db

# 6. Применить миграции
make migrate

# 7. (Опционально) Заполнить демо-данными
make seed

# 8. Запустить сервер
make run
```

---

## Шаг 5: Проверить

1. Открыть http://localhost:8001/docs
2. Попробовать:
   - POST `/api/v1/auth/register` — зарегистрировать пользователя
   - POST `/api/v1/auth/login` — получить токен
   - Использовать токен для других запросов

Если запускал `make seed`, можно сразу логиниться:
- Email: `admin@example.com`
- Password: `admin`

---

## Шаг 6: Запустить тесты

```bash
make test
```

---

## Структура файлов после переноса

```
senior-crm/
├── .env              ← Твои локальные настройки (НЕ коммитить!)
├── .env.sample       ← Пример для других разработчиков
├── .gitignore
├── .coveragerc
├── Dockerfile
├── Makefile
├── README.md
├── REQUIREMENTS_MAPPING.md
├── alembic/
├── docker-compose.yml
├── pyproject.toml
├── pytest.ini
├── src/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── scripts/
│   ├── services/
│   └── main.py
└── tests/
```

---

## Быстрый старт для ревьюера (скопировать в README)

```bash
# Clone
git clone git@github.com:YOUR_USERNAME/senior-crm.git
cd senior-crm

# Setup
cp .env.sample .env
make install
make db
make wait-db
make migrate
make seed

# Run
make run

# Open http://localhost:8001/docs
# Login: admin@example.com / admin
```
