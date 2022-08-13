from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r'tasks', TaskViewSet, basename="Task")

urlpatterns = [
    path('todo/', include(router.urls)),
]