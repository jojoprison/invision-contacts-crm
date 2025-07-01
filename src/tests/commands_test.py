import pytest
from django.core.management import call_command
from django.db import connection
from tenants.models import Tenant
import uuid


@pytest.mark.django_db
def test_create_tenant_command():
    """Тестирует команду create_tenant"""
    test_name = f"cmd_{uuid.uuid4().hex[:8]}"
    schema_name = f"contact_{test_name}"
    
    # Проверяем, что можем вызвать команду без ошибок
    try:
        call_command('create_tenant', test_name, schema_name)
        command_success = True
    except Exception:
        command_success = False
    
    assert command_success, "Команда create_tenant должна выполняться без ошибок"
    
    # Проверяем, что схема создана
    with connection.cursor() as cursor:
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", 
                      [schema_name])
        assert cursor.fetchone() is not None
    
    # Очистка после теста
    with connection.cursor() as cursor:
        cursor.execute(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE")


@pytest.mark.django_db
def test_delete_tenant_command():
    """Тестирует команду delete_tenant"""
    # Создаем тестовый тенант
    test_name = f"del_{uuid.uuid4().hex[:8]}"
    schema_name = f"contact_{test_name}"
    
    tenant = Tenant.objects.create(name=test_name, schema_name=schema_name)
    
    # Создаем схему вручную
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
    
    # Проверяем, что схема существует
    with connection.cursor() as cursor:
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", 
                      [schema_name])
        assert cursor.fetchone() is not None
    
    # Удаляем тенант через команду
    try:
        call_command('delete_tenant', tenant.name)
        command_success = True
    except Exception:
        command_success = False
    
    assert command_success, "Команда delete_tenant должна выполняться без ошибок"
    
    # Проверяем, что схема удалена
    with connection.cursor() as cursor:
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", 
                      [schema_name])
        assert cursor.fetchone() is None


@pytest.mark.django_db
def test_migrate_schema_command():
    """Тестирует команду migrate_schema"""
    # Создаем тестовый тенант и схему
    test_name = f"mgr_{uuid.uuid4().hex[:8]}"
    test_schema = f"contact_{test_name}"
    
    # Создаем схему вручную
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {test_schema}")
    
    # Запускаем миграцию схемы
    try:
        call_command('migrate_schema', test_schema)
        command_success = True
    except Exception:
        command_success = False
    
    assert command_success, "Команда migrate_schema должна выполняться без ошибок"
    
    # Очистка после теста
    with connection.cursor() as cursor:
        cursor.execute(f"DROP SCHEMA IF EXISTS {test_schema} CASCADE")


@pytest.mark.django_db
def test_migrate_tenant_schema_command():
    """Тестирует команду migrate_tenant_schema"""
    # Создаем тестовый тенант
    test_name = f"mts_{uuid.uuid4().hex[:8]}"
    schema_name = f"contact_{test_name}"
    
    tenant = Tenant.objects.create(name=test_name, schema_name=schema_name)
    
    # Создаем схему вручную
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
    
    # Запускаем миграцию для тенанта
    try:
        call_command('migrate_tenant_schema', test_name)
        command_success = True
    except Exception:
        command_success = False
    
    assert command_success, "Команда migrate_tenant_schema должна выполняться без ошибок"
    
    # Очистка после теста
    with connection.cursor() as cursor:
        cursor.execute(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE")
    tenant.delete()


@pytest.mark.django_db
def test_setup_environment_command():
    """Тестирует команду setup_environment"""
    # Запускаем команду настройки окружения
    try:
        call_command('setup_environment')
        command_success = True
    except Exception:
        command_success = False
    
    assert command_success, "Команда setup_environment должна выполняться без ошибок"
    
    # Проверяем, что основная схема существует
    with connection.cursor() as cursor:
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'public'")
        assert cursor.fetchone() is not None
        
        # Проверяем, что таблица tenants существует
        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'tenants')")
        assert cursor.fetchone()[0] is True
