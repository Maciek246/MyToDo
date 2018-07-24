from django.db.models import Count

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer
from .filters import TaskFilter


class TaskViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    filterset_class = TaskFilter

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

    @action(methods=['GET'], detail=False)
    def dates(self, request, *args, **kwargs):
        qs = self.get_queryset()\
            .extra(select={'start': 'Date(start)'})\
            .values('start')\
            .annotate(tasks=Count('start'))
        return Response(qs, 200)
