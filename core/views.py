from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from rest_framework import filters


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', 'description', 'created_at', ]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if "completed" in self.request.GET:
            queryset = queryset.filter(completed=self.request.GET.get("completed") == "true")

        return queryset
