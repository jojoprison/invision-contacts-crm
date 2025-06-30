from django.db import models
import uuid


class Tenant(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schema_name = models.CharField(max_length=63, unique=True, help_text='Имя схемы PostgreSQL')
    name = models.CharField(max_length=100, help_text='Название организации')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # explicitly 'public'
        db_table = 'public.tenants'

    def __str__(self):
        return f'{self.name} ({self.schema_name})'


class Domain(models.Model):
    """
    Требуется для совместимости с django-pgschemas.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    domain = models.CharField(max_length=253, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    class Meta:
        # explicitly 'public'
        db_table = 'public.domains'

    def __str__(self):
        return self.domain
