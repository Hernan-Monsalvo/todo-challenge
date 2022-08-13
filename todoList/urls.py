from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("auth.urls")),
    path('', include("core.urls")),
]

