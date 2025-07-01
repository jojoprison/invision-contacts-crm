from django.core.management.base import BaseCommand
from django.db import connection

from tenants.models import Tenant


class Command(BaseCommand):
    help = 'Применяет миграции к указанной схеме тенанта'

    def add_arguments(self, parser):
        parser.add_argument('schema_name', help='Имя схемы тенанта')
        parser.add_argument('--check', action='store_true', help='Только проверка наличия таблиц')

    def handle(self, *args, **options):
        schema_name = options['schema_name']
        check_only = options.get('check', False)

        try:
            _ = Tenant.objects.get(schema_name=schema_name)
        except Tenant.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Тенант {schema_name} не найден!'))
            return

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT schema_name
                   FROM information_schema.schemata
                   WHERE schema_name = %s""", [schema_name])
            if cursor.fetchone() is None:
                self.stdout.write(f'Схема {schema_name} не найдена, создаем...')
                cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')

            cursor.execute(
                """SELECT table_name
                   FROM information_schema.tables
                   WHERE table_schema = %s""", [schema_name])
            tables = [row[0] for row in cursor.fetchall()]

            if check_only:
                self.stdout.write(f'Таблицы в схеме {schema_name}:')
                for table in tables or ['-- нет таблиц --']:
                    self.stdout.write(f'  - {table}')
                return

            if 'contacts_contact' in tables:
                self.stdout.write('Таблица contacts_contact уже существует')
            else:
                self.stdout.write(f'Создаем таблицы для модели Contact в схеме {schema_name}')

                cursor.execute(f'SET search_path TO "{schema_name}", public')

                cursor.execute("""
                               CREATE TABLE contacts_contact
                               (
                                   id           uuid                     NOT NULL PRIMARY KEY,
                                   name         varchar(100)             NOT NULL,
                                   email        varchar(254)             NOT NULL UNIQUE,
                                   phone        varchar(20),
                                   date_created timestamp with time zone NOT NULL DEFAULT now()
                               )
                               """)

                cursor.execute("""
                               CREATE TABLE IF NOT EXISTS django_content_type
                               (
                                   id        serial       NOT NULL PRIMARY KEY,
                                   app_label varchar(100) NOT NULL,
                                   model     varchar(100) NOT NULL,
                                   CONSTRAINT django_content_type_app_label_model_key
                                   UNIQUE (app_label, model)
                               )
                               """)

                cursor.execute("""
                               INSERT INTO django_content_type
                               (app_label, model)
                               VALUES
                               ('contacts', 'contact')
                               ON CONFLICT (app_label, model) DO NOTHING
                               """)

                cursor.execute("""
                               CREATE TABLE IF NOT EXISTS django_migrations
                               (
                                   id      serial                   NOT NULL PRIMARY KEY,
                                   app     varchar(255)             NOT NULL,
                                   name    varchar(255)             NOT NULL,
                                   applied timestamp with time zone NOT NULL
                               )
                               """)

                cursor.execute("""
                               INSERT INTO django_migrations
                               (app, name, applied)
                               VALUES
                               ('contacts', '0001_initial', now())
                               ON CONFLICT DO NOTHING
                               """)

                cursor.execute('SET search_path TO public')

        self.stdout.write(self.style.SUCCESS(
            f'Миграции успешно применены к схеме {schema_name}'))
