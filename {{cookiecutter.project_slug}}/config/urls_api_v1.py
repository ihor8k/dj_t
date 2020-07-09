from django.urls import path, include


app_name = 'api_v1'

urlpatterns = [
    path('', include('apps.accounts.api.v1.urls', namespace='accounts'))
]
