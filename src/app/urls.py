from django.contrib import admin
from django.urls import path

from contacts.api import api as contacts_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/contacts/', contacts_api.urls),  # Изменили маршрут с 'api/' на 'api/contacts/'
]
