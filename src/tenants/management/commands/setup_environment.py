from django.core.management import call_command
from django.core.management.base import BaseCommand

from tenants.models import Tenant


class Command(BaseCommand):
    help = 'Настраивает окружение проекта: применяет миграции и создаёт тенанта по умолчанию'

    def handle(self, *args, **options):
        self.stdout.write('Применяем миграции к схеме public...')
        call_command('migrate')

        tenant_count = Tenant.objects.count()
        if tenant_count == 0:
            self.stdout.write('Создаем тенанта по умолчанию...')
            call_command('create_tenant', 'default', 'Тенант по умолчанию')
            self.stdout.write(self.style.SUCCESS('Тенант по умолчанию создан успешно.'))
        else:
            self.stdout.write(f'Найдено существующих тенантов: {tenant_count}')

        self.stdout.write(self.style.SUCCESS('Настройка окружения успешно завершена.'))
