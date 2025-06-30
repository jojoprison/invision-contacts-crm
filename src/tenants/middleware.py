from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.db import connection
import logging

from app.settings import TENANT_SCHEMA_PREFIX
from tenants.models import Tenant

logger = logging.getLogger(__name__)

class TenantMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        schema_name = request.headers.get('X-SCHEMA')

        if not schema_name:
            return HttpResponseBadRequest('TENANT_NOT_FOUND: X-SCHEMA header is required')

        if not schema_name.startswith(TENANT_SCHEMA_PREFIX):
            schema_name = f"{TENANT_SCHEMA_PREFIX}{schema_name}"

        try:
            # Получаем тенанта
            tenant = Tenant.objects.get(schema_name=schema_name)
            
            # Устанавливаем schema_name в атрибуты запроса
            request.tenant = tenant
            request.tenant_schema = schema_name
            
            # Устанавливаем search_path для текущего соединения
            self._set_schema(schema_name)
            
            # Логируем для отладки
            logger.debug(f"Setting schema for {schema_name}")
            
            # Получаем ответ
            response = self.get_response(request)
            
            # После получения ответа снова устанавливаем search_path,
            # так как Django может сбросить его между запросами
            self._set_schema(schema_name)
            
            return response

        except Tenant.DoesNotExist:
            return HttpResponseNotFound('TENANT_NOT_FOUND: Schema does not exist')
        except Exception as e:
            logger.error(f"Error in TenantMiddleware: {str(e)}")
            return HttpResponseBadRequest(f"Error in tenant routing: {str(e)}")
    
    def _set_schema(self, schema_name):
        """Установка search_path для PostgreSQL"""
        with connection.cursor() as cursor:
            cursor.execute(f'SET search_path TO "{schema_name}", public')
