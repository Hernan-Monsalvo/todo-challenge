from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views
from .views import RegisterView

urlpatterns = [
    path('login', views.obtain_auth_token),
    path('register', RegisterView.as_view())
]
