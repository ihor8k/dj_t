from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
{%- if cookiecutter.use_drf_yasg == 'y' %}
from drf_yasg.openapi import Info, Contact
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
{%- endif %}

{%- if cookiecutter.use_drf_yasg == 'y' %}

schema_view = get_schema_view(
   Info(
      title='{{ cookiecutter.project_name }} API',
      default_version='v1',
      description='{{ cookiecutter.project_name }} project',
      contact=Contact(email='{{ cookiecutter.project_slug }}@example.com'),
   ),
   public=True,
   permission_classes=(AllowAny,),
)
{%- endif %}

urlpatterns = [
   path('admin/', admin.site.urls),
   {%- if cookiecutter.use_drf == 'y' %}
   path('api/v1/', include('config.urls_api_v1', namespace='api_v1')),
   {%- endif %}
   {%- if cookiecutter.use_drf_yasg == 'y' %}
   path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
   path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   {%- endif %}
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
