from django.contrib import admin
from django.db import connection
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import Contact
from tenants.models import Tenant


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('id', 'date_created')
    fieldsets = (
        ('Основная информация', {
            'fields': ('id', 'name', 'email')
        }),
        ('Дополнительная информация', {
            'fields': ('phone', 'date_created')
        }),
    )
    
    # Эти атрибуты нужны для предотвращения ошибок при работе с изначальным списком объектов
    actions = None
    show_full_result_count = False
    
    def changelist_view(self, request, extra_context=None):
        # Перенаправляем на страницу выбора тенанта
        if not request.GET.get('tenant'):
            return HttpResponseRedirect(reverse('admin:select_tenant') + '?next=' + request.path)
            
        # Если указан тенант, переключаем схему
        tenant_schema = request.GET.get('tenant')
        try:
            tenant = Tenant.objects.get(schema_name=tenant_schema)
            with connection.cursor() as cursor:
                cursor.execute(f'SET search_path TO {tenant_schema}, public;')
            # Добавляем контекст с именем тенанта
            if extra_context is None:
                extra_context = {}
            extra_context['tenant_name'] = tenant.name
            return super().changelist_view(request, extra_context)
        except Tenant.DoesNotExist:
            messages.error(request, f'Тенант {tenant_schema} не существует')
            return HttpResponseRedirect(reverse('admin:select_tenant') + '?next=' + request.path)
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # Проверяем, указан ли тенант
        tenant_schema = request.GET.get('tenant')
        if not tenant_schema:
            return HttpResponseRedirect(reverse('admin:select_tenant') + '?next=' + request.path)
            
        # Переключаем схему
        try:
            tenant = Tenant.objects.get(schema_name=tenant_schema)
            with connection.cursor() as cursor:
                cursor.execute(f'SET search_path TO {tenant_schema}, public;')
            # Добавляем контекст с именем тенанта
            if extra_context is None:
                extra_context = {}
            extra_context['tenant_name'] = tenant.name
            return super().changeform_view(request, object_id, form_url, extra_context)
        except Tenant.DoesNotExist:
            messages.error(request, f'Тенант {tenant_schema} не существует')
            return HttpResponseRedirect(reverse('admin:select_tenant') + '?next=' + request.path)
