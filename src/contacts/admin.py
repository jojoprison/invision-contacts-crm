from django.contrib import admin
from .models import Contact

# Register your models here.

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
