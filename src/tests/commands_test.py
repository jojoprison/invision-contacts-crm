import pytest
from django.core.management import call_command
from django.db import connection
from tenants.models import Tenant
import uuid


@pytest.mark.django_db
def test_create_tenant_command():
    """Тестирует команду create_tenant"""
    test_name = f"cmd_{uuid.uuid4().hex[:8]}"
    test_email = f"{test_name}@example.com"
    
    call_command('create_tenant', test_name, 'Тестовый Тенант', test_email)
    
    # Проверяем, что тенант создан в БД
    tenant = Tenant.objects.get(name=test_name)
    assert tenant.display_name == 'Тестовый Тенант'
    assert tenant.email == test_email
    
    # Проверяем, что схема создана
    with connection.cursor() as cursor:
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", 
                      [f"contact_{test_name}"])
        assert cursor.fetchone() is not None
    
    # Очистка после теста
    with connection.cursor() as cursor:
        cursor.execute(f"DROP SCHEMA IF EXISTS contact_{test_name} CASCADE")
    tenant.delete()


@pytest.mark.django_db
def test_delete_tenant_command():
    """Тестирует команду delete_tenant"""
    # Создаем тестовый тенант
    test_name = f"del_{uuid.uuid4().hex[:8]}"
    test_email = f"{test_name}@example.com"
    
    tenant = Tenant.objects.create(name=test_name, display_name='Для удаления', email=test_email)
    
    # Создаем схему вручную
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS contact_{test_name}")
    
    # Проверяем, что схема существует
    with connection.cursor() as cursor:
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", 
                      [f"contact_{test_name}"])
        assert cursor.fetchone() is not None
    
    # Удаляем тенант через команду
    call_command('delete_tenant', test_name)
    
    # Проверяем, что тенант удален
    assert not Tenant.objects.filter(name=test_name).exists()
    
    # Проверяем, что схема удалена
    with connection.cursor() as cursor:
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", 
                      [f"contact_{test_name}"])
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
    call_command('migrate_schema', test_schema)
    
    # Проверяем наличие таблиц после миграции
    with connection.cursor() as cursor:
        cursor.execute(f"SET search_path TO {test_schema}")
        cursor.execute("SELECT EXISTS(SELECT FROM pg_tables WHERE schemaname = %s AND tablename = 'contacts_contact')", 
                      [test_schema])
        assert cursor.fetchone()[0] is True
    
    # Очистка после теста
    with connection.cursor() as cursor:
        cursor.execute(f"DROP SCHEMA IF EXISTS {test_schema} CASCADE")


@pytest.mark.django_db
def test_migrate_tenant_schema_command():
    """Тестирует команду migrate_tenant_schema"""
    # Создаем тестовый тенант
    test_name = f"mts_{uuid.uuid4().hex[:8]}"
    test_email = f"{test_name}@example.com"
    
    tenant = Tenant.objects.create(name=test_name, display_name='Тест Миграции', email=test_email)
    
    # Создаем схему вручную
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS contact_{test_name}")
    
    # Запускаем миграцию для тенанта
    call_command('migrate_tenant_schema', test_name)
    
    # Проверяем наличие таблицы contacts_contact в схеме тенанта
    with connection.cursor() as cursor:
        cursor.execute(f"SET search_path TO contact_{test_name}")
        cursor.execute("SELECT EXISTS(SELECT FROM pg_tables WHERE schemaname = %s AND tablename = 'contacts_contact')", 
                      [f"contact_{test_name}"])
        assert cursor.fetchone()[0] is True
    
    # Очистка после теста
    with connection.cursor() as cursor:
        cursor.execute(f"DROP SCHEMA IF EXISTS contact_{test_name} CASCADE")
    tenant.delete()


@pytest.mark.django_db
def test_setup_environment_command():
    """Тестирует команду setup_environment"""
    # Запускаем команду настройки окружения
    call_command('setup_environment')
    
    # Проверяем, что основная схема существует
    with connection.cursor() as cursor:
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'public'")
        assert cursor.fetchone() is not None
        
        # Проверяем создание тестовых тенантов (если они создаются в команде)
        # Здесь предполагаем, что команда создает тестового тенанта с именем "demo"
        cursor.execute("SELECT COUNT(*) FROM tenants_tenant")
        tenant_count = cursor.fetchone()[0]
        assert tenant_count > 0  # Убеждаемся, что хоть какие-то тенанты созданы
