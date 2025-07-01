from django.contrib import admin
from .models import Tenant, Domain


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'schema_name', 'created_at', 'auto_drop_schema')
    list_filter = ('created_at', 'auto_drop_schema')
    search_fields = ('name', 'schema_name')
    readonly_fields = ('id', 'created_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('id', 'name', 'schema_name')
        }),
        ('Настройки', {
            'fields': ('auto_drop_schema', 'created_at')
        }),
    )


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary', 'folder')
    list_filter = ('is_primary', 'tenant')
    search_fields = ('domain', 'folder')
    readonly_fields = ('id',)
    autocomplete_fields = ('tenant',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('id', 'domain', 'tenant')
        }),
        ('Настройки', {
            'fields': ('is_primary', 'folder')
        }),
    )
