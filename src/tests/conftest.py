import pytest
from django.test import Client

from tenants.models import Tenant


@pytest.fixture
def setup_tenants(db):

    Tenant.objects.filter(schema_name__in=['test_tenant1', 'test_tenant2']).delete()

    tenant1 = Tenant.objects.create(schema_name='test_tenant1', name='Тестовый тенант 1')
    tenant2 = Tenant.objects.create(schema_name='test_tenant2', name='Тестовый тенант 2')
    
    return tenant1, tenant2


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
def invalid_schema_client():
    client = Client()
    client.defaults['HTTP_X_SCHEMA'] = 'nonexistent_schema'
    return client


@pytest.fixture
def create_contact():
    """
    Args:
        client: Django клиент с настроенным заголовком X-SCHEMA
        name: Имя контакта (по умолчанию "Test Contact")
        email: Email контакта (по умолчанию "test@example.com")
        phone: Телефон контакта (по умолчанию "+79991234567")
    """
    def _create_contact(client, name="Test Contact", email="test@example.com", phone="+79991234567"):
        return client.post('/api/contacts/', {
            'name': name,
            'email': email,
            'phone': phone
        }, content_type='application/json')
    
    return _create_contact
