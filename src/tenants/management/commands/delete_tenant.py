from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from tenants.models import Tenant, Domain


class Command(BaseCommand):
    help = 'Удаляет тенанта и его схему'

    def add_arguments(self, parser):
        parser.add_argument('schema_name', help='Имя схемы тенанта для удаления')
        parser.add_argument('--force', action='store_true', 
                            help='Удалить даже если схема не существует в базе')

    def handle(self, *args, **options):
        schema_name = options['schema_name']
        force = options.get('force', False)
        
        # Проверяем существование тенанта
        try:
            tenant = Tenant.objects.get(schema_name=schema_name)
        except Tenant.DoesNotExist:
            if not force:
                raise CommandError(f'Тенант с схемой {schema_name} не найден!')
            else:
                self.stdout.write(self.style.WARNING(f'Тенант {schema_name} не найден в базе, но --force указан'))
                return

        # Удаляем домены, связанные с тенантом
        domain_count = Domain.objects.filter(tenant=tenant).delete()[0]
        self.stdout.write(self.style.SUCCESS(f'Удалено {domain_count} доменов'))

        # Удаляем схему в PostgreSQL
        with connection.cursor() as cursor:
            cursor.execute(f'DROP SCHEMA IF EXISTS {schema_name} CASCADE;')
            
        # Удаляем тенанта из базы
        tenant.delete()
        
        self.stdout.write(self.style.SUCCESS(
            f'Успешно удалён тенант и схема {schema_name}'))
