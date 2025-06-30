#!/bin/bash
set -e

cd /app

echo "Применение миграций к public схеме..."
python src/manage.py migrate

echo "Проверка существования тенанта по умолчанию..."
TENANT_COUNT=$(cd src && python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()
from tenants.models import Tenant
print(Tenant.objects.count())
")

if [ "$TENANT_COUNT" -eq "0" ]; then
    echo "Создание тенанта по умолчанию..."
    python src/manage.py create_tenant default "Тенант по умолчанию"
fi

exec "$@"
