# invision-contacts-crm

Contacts service for SaaS-CRM with schema-based multi-tenancy.

⸻

🚀 Prerequisites
•	Python 3.11 installed (python3.11 in PATH)
•	Poetry (>= 2.1)
•	PostgreSQL 14+ (local or Docker)
•	Docker & Docker Compose (optional, for full-stack)

⸻

📦 Installation & Setup

# 1. Clone the repository
git clone https://github.com/jojoprison/invision-contacts-crm.git
cd invision-contacts-crm

# 2. Ensure Python 3.11 is available
python3.11 --version   # should output 3.11.x

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
