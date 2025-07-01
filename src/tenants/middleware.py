import logging

from django.db import connection
from django.http import HttpResponseBadRequest, HttpResponseNotFound

from app.settings import TENANT_SCHEMA_PREFIX
from tenants.models import Tenant

logger = logging.getLogger(__name__)


class TenantMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Список путей, для которых не требуется X-SCHEMA
        public_paths = [
            '/admin/',
            '/api/contacts/docs',
            '/api/contacts/openapi.json',
            '/static/',
        ]

        path = request.path_info
        is_public_path = any(path.startswith(public_path) for public_path in public_paths)

        if is_public_path:
            self._set_schema('public')
            return self.get_response(request)

        schema_name = request.headers.get('X-SCHEMA')

        if not schema_name:
            return HttpResponseBadRequest('TENANT_NOT_FOUND: X-SCHEMA header is required')

        if not schema_name.startswith(TENANT_SCHEMA_PREFIX):
            schema_name = f"{TENANT_SCHEMA_PREFIX}{schema_name}"

        try:
            tenant = Tenant.objects.get(schema_name=schema_name)

            request.tenant = tenant
            request.tenant_schema = schema_name

            self._set_schema(schema_name)

            logger.debug(f"Setting schema for {schema_name}")

            response = self.get_response(request)

            # Django может сбросить между запросами
            self._set_schema(schema_name)

            return response

        except Tenant.DoesNotExist:
            return HttpResponseNotFound('TENANT_NOT_FOUND: Schema does not exist')
        except Exception as e:
            logger.error(f"Error in TenantMiddleware: {str(e)}")
            return HttpResponseBadRequest(f"Error in tenant routing: {str(e)}")

    def _set_schema(self, schema_name):
        with connection.cursor() as cursor:
            cursor.execute(f'SET search_path TO "{schema_name}", public')
