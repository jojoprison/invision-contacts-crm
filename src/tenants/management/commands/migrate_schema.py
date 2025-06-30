from django.core.management.commands.migrate import Command as DjangoMigrate
from django_pgschemas.management.commands.migrateschema import Command as OrigMigrateSchema
from django.db import connection
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.autodetector import MigrationAutodetector
from django.core.checks import Tags


class Command(OrigMigrateSchema, DjangoMigrate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        loader = MigrationLoader(connection)
        self.autodetector = MigrationAutodetector(
            loader.project_state(),
            loader.graph
        )
    
    def handle(self, *args, **options):
        # Переопределяем для отключения проверок
        options['skip_checks'] = True
        return super().handle(*args, **options)
