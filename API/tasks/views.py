from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer


class TaskViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    filterset_fields = ('name', 'start', 'created', 'finished')

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)\
            .select_related('owner')\
            .only('name', 'owner__username', 'content', 'finished', 'start')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        else:
            return TaskSerializer
