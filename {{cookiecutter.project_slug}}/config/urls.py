from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from drf_yasg.openapi import Info, Contact
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
   Info(
      title='{{ cookiecutter.project_slug }} API',
      default_version='v1',
      description='{{ cookiecutter.project_slug }} project',
      contact=Contact(email='{{ cookiecutter.project_slug }}@example.com'),
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
   path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
