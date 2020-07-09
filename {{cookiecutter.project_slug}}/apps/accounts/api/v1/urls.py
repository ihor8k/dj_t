from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.accounts.api.v1 import views


app_name = 'accounts'

router = SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('', include(router.urls))
]
