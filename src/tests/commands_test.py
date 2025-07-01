import uuid

import pytest
from django.core.management import call_command
from django.db import connection

from tenants.models import Tenant


@pytest.mark.django_db
def test_create_tenant_command():

    test_name = f"cmd_{uuid.uuid4().hex[:8]}"
    schema_name = f"contact_{test_name}"

    try:
        call_command('create_tenant', test_name, schema_name)
        command_success = True
    except Exception:
        command_success = False

    assert command_success, "Команда create_tenant должна выполняться без ошибок"

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s",
            [schema_name]
        )
        assert cursor.fetchone() is not None

    with connection.cursor() as cursor:
        cursor.execute(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE")


@pytest.mark.django_db
def test_delete_tenant_command():

    test_name = f"del_{uuid.uuid4().hex[:8]}"
    schema_name = f"contact_{test_name}"

    tenant = Tenant.objects.create(name=test_name, schema_name=schema_name)

    with connection.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")

    with connection.cursor() as cursor:

        cursor.execute(
            "SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s",
            [schema_name]
        )
        assert cursor.fetchone() is not None

    try:
        call_command('delete_tenant', tenant.name)
        command_success = True
    except Exception:
        command_success = False

    assert command_success, "Команда delete_tenant должна выполняться без ошибок"

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s",
            [schema_name]
        )
        assert cursor.fetchone() is None


@pytest.mark.django_db
def test_migrate_tenant_schema_command():

    test_name = f"mts_{uuid.uuid4().hex[:8]}"
    schema_name = f"contact_{test_name}"

    tenant = Tenant.objects.create(name=test_name, schema_name=schema_name)

    with connection.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")

    try:
        call_command('migrate_tenant_schema', test_name)
        command_success = True
    except Exception:
        command_success = False

    assert command_success, "Команда migrate_tenant_schema должна выполняться без ошибок"

    with connection.cursor() as cursor:
        cursor.execute(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE")
    tenant.delete()


@pytest.mark.django_db
def test_setup_environment_command():

    try:
        call_command('setup_environment')
        command_success = True
    except Exception:
        command_success = False

    assert command_success, "Команда setup_environment должна выполняться без ошибок"

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'public'"
        )
        assert cursor.fetchone() is not None
