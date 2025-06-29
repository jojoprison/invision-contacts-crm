from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.db import connection

from app.settings import TENANT_SCHEMA_PREFIX
from tenants.models import Tenant


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
            tenant = Tenant.objects.get(schema_name=schema_name)

            with connection.cursor() as cursor:
                cursor.execute(f'SET search_path TO "{schema_name}", public')

            request.tenant = tenant

        except Tenant.DoesNotExist:
            return HttpResponseNotFound('TENANT_NOT_FOUND: Schema does not exist')

        response = self.get_response(request)
        return response
