from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django_pgschemas.utils import create_schema

from app.settings import TENANT_SCHEMA_PREFIX
from tenants.models import Tenant, Domain
from django.core.management import call_command

class Command(BaseCommand):

    help = 'Создание нового арендатора со своей схемой PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument('schema', help='Имя схемы (без префикса)')
        parser.add_argument('name', help='Название организации')
        parser.add_argument('--domain', help='Домен для привязки к тенанту (опционально)')
        parser.add_argument('--no-sync-schema', action='store_true',
                            help='Не выполнять автоматические миграции в схему')

    def handle(self, *args, **options):
        try:
            schema = options['schema']
            name = options['name']
            custom_domain = options.get('domain')
            sync_schema = not options.get('no_sync_schema', False)

            prefix = TENANT_SCHEMA_PREFIX
            schema_name = f"{prefix}{schema}" if not schema.startswith(prefix) else schema

            if Tenant.objects.filter(schema_name=schema_name).exists():
                raise CommandError(f'Тенант со схемой {schema_name} уже существует!')

            # Создаем запись тенанта
            tenant = Tenant.objects.create(
                schema_name=schema_name,
                name=name,
                auto_drop_schema=True  # Для совместимости с django-pgschemas
            )

            # Создаем домен
            domain_name = custom_domain or f"{schema}.example.com"
            domain = Domain.objects.create(
                domain=domain_name,
                tenant=tenant,
                is_primary=True  # Отмечаем как основной домен
            )

            self.stdout.write(self.style.SUCCESS(
                f'Создан тенант [{name}] со схемой [{schema_name}]'))
            self.stdout.write(self.style.SUCCESS(
                f'Привязан домен: {domain_name}'))

            # Создаем схему и применяем миграции при необходимости
            try:
                self.stdout.write(f'Создаем схему {schema_name}...')
                create_schema(schema_name, check_if_exists=True, sync_schema=sync_schema)
                
                if sync_schema:
                    self.stdout.write(self.style.SUCCESS(
                        f'Схема {schema_name} создана и миграции применены автоматически'))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Схема {schema_name} создана без применения миграций\n'
                        f'Для применения миграций выполните команду:\n'
                        f'python manage.py migrate_tenant_schema {schema_name}'))

                # TODO в общем автоматические миграции от 'create_schema' (sync_schema) не работают
                # TODO надеюсь скоро пофиксят. пришлось вот это городить - потом надо убрать
                self.stdout.write(f"Применяем migrate_tenant_schema для создания таблиц...")
                call_command('migrate_tenant_schema', schema_name)
                self.stdout.write(self.style.SUCCESS(f"Таблицы в схеме {schema_name} созданы успешно"))

            except Exception as e:
                # Если произошла ошибка при создании схемы, удаляем запись тенанта
                tenant.delete()
                raise CommandError(f'Ошибка при создании схемы: {str(e)}')
                
        except Exception as e:
            raise CommandError(f'Ошибка при создании тенанта: {str(e)}')
