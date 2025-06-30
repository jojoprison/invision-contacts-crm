from django.core.management.commands.migrate import Command as DjangoMigrate
from django_pgschemas.management.commands.migrateschema import Command as OrigMigrateSchema
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.backends.base.base import BaseDatabaseWrapper


class Command(OrigMigrateSchema, DjangoMigrate):
    """
    Патчим оригинальную MigrateSchemaCommand из django-pgschemas,
    добавляя требуемый Django 5.2+ атрибут autodetector.
    """
    connection: BaseDatabaseWrapper

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # здесь self.connection уже доступен благодаря родительскому классу
        loader = MigrationLoader(self.connection)
        self.autodetector = MigrationAutodetector(
            loader.project_state(),
            loader.graph
        )