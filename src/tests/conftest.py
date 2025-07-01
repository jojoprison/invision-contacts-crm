import json

import pytest
from django.core.management import call_command
from django.db import connection
from django.test import Client

from app.settings import TENANT_SCHEMA_PREFIX
from tenants.models import Tenant

pytest_plugins = ['pytest_django']
pytest_mark_django_db_in = ['src/tests/']


@pytest.fixture(scope="session")
def django_db_setup():
    pass


@pytest.fixture
def setup_tenants(db):

    tenant1_name = 'test_tenant1'
    tenant2_name = 'test_tenant2'

    schema1 = f"{TENANT_SCHEMA_PREFIX}{tenant1_name}"
    schema2 = f"{TENANT_SCHEMA_PREFIX}{tenant2_name}"

    Tenant.objects.filter(schema_name__in=[schema1, schema2]).delete()

    with connection.cursor() as cursor:
        cursor.execute(f"DROP SCHEMA IF EXISTS {schema1} CASCADE;")
        cursor.execute(f"DROP SCHEMA IF EXISTS {schema2} CASCADE;")
        cursor.execute(f"CREATE SCHEMA {schema1};")
        cursor.execute(f"CREATE SCHEMA {schema2};")

    tenant1 = Tenant.objects.create(
        schema_name=schema1,
        name='Тестовый тенант 1',
        auto_drop_schema=True
    )
    tenant2 = Tenant.objects.create(
        schema_name=schema2,
        name='Тестовый тенант 2',
        auto_drop_schema=True
    )

    try:
        print(f"Создаем таблицы для модели Contact в схеме {schema1}")
        call_command('migrate_tenant_schema', schema1)
        print(f"Миграции успешно применены к схеме {schema1}")

        print(f"Создаем таблицы для модели Contact в схеме {schema2}")
        call_command('migrate_tenant_schema', schema2)
        print(f"Миграции успешно применены к схеме {schema2}")
    except Exception as e:
        print(f"Ошибка при настройке схемы: {str(e)}")
        raise

    yield tenant1, tenant2

    try:
        print(f"Очистка тестовых схем {schema1} и {schema2}")
        with connection.cursor() as cursor:
            cursor.execute(f"DROP SCHEMA IF EXISTS {schema1} CASCADE;")
            cursor.execute(f"DROP SCHEMA IF EXISTS {schema2} CASCADE;")
        Tenant.objects.filter(schema_name__in=[schema1, schema2]).delete()
        print("Тестовые схемы успешно удалены")
    except Exception as e:
        print(f"Ошибка при очистке схем: {str(e)}")


@pytest.fixture
def tenant1_client(setup_tenants):
    client = Client()
    client.defaults['HTTP_X_SCHEMA'] = 'test_tenant1'
    return client


@pytest.fixture
def tenant2_client(setup_tenants):
    client = Client()
    client.defaults['HTTP_X_SCHEMA'] = 'test_tenant2'
    return client


@pytest.fixture
def no_schema_client():
    return Client()


@pytest.fixture
def invalid_schema_client(db):
    client = Client()
    client.defaults['HTTP_X_SCHEMA'] = 'nonexistent_schema'
    return client


@pytest.fixture
def create_contact(db):

    def _create_contact(
            client, name="Test Contact", email="test@example.com", phone="+79991234567"
    ):
        data = {
            'name': name,
            'email': email,
            'phone': phone
        }
        return client.post(
            '/api/contacts/',
            json.dumps(data),
            content_type='application/json'
        )
    return _create_contact
