from django.contrib import admin
from django.urls import path

from contacts.api import api as contacts_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', contacts_api.urls),
]
