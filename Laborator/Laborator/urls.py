from django.contrib import admin
from django.urls import path, include
from .router import router
from rest_framework.authtoken import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('farmacie.urls')),
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path(
        'login/',
        LoginView.as_view(
            template_name='farmacie/login.html'
            ), name='login'),
]
