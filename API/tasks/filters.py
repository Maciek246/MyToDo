from django_filters import rest_framework as filters

from .models import Task


class TaskFilter(filters.FilterSet):

    start = filters.DateFilter(method='filter_by_date')
    created = filters.DateFilter(method='filter_by_date')
    finished = filters.DateFilter(method='filter_by_date')

    class Meta:
        model = Task
        fields = ('name', 'start', 'created', 'finished')

    def filter_by_date(self, queryset, name, value):
        date_filter = "__".join([name, 'date'])
        return queryset.filter(**{date_filter: value})


