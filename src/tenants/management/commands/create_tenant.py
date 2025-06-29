from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from app.settings import TENANT_SCHEMA_PREFIX
from tenants.models import Tenant, Domain


class Command(BaseCommand):

    help = 'Создание нового арендатора со своей схемой PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument('schema', help='Имя схемы (без префикса)')
        parser.add_argument('name', help='Название организации')

    def handle(self, *args, **options):

        schema = options['schema']
        name = options['name']

        prefix = TENANT_SCHEMA_PREFIX
        schema_name = f"{prefix}{schema}" if not schema.startswith(prefix) else schema

        if Tenant.objects.filter(schema_name=schema_name).exists():
            raise CommandError(f'Тенант со схемой {schema_name} уже существует!')

        tenant = Tenant.objects.create(
            schema_name=schema_name,
            name=name
        )

        domain = Domain.objects.create(
            domain=f"{schema}.example.com",
            tenant=tenant
        )

        self.stdout.write(self.style.SUCCESS(f'Создан тенант [{name}] со схемой [{schema_name}]'))

        with connection.cursor() as cursor:
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
            cursor.execute(f'SET search_path TO "{schema_name}", public')

        self.stdout.write(
            self.style.WARNING(
                f'Схема создана. Теперь выполните команду:\n'
                f'python manage.py migrate --schema={schema_name}'
            )
        )
