from django.db.models import Q
from django_filters import rest_framework as filters

from job.models import Job


class JobFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", method="filter_title")
    job_type__in = filters.BaseInFilter(field_name="job_type", lookup_expr="in")
    location__in = filters.BaseInFilter(field_name="location", lookup_expr="in")

    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "job_type",
            "location",
            "occupied",
            "user",
            "job_type__in",
            "location__in"
        ]

    def filter_title(self, queryset, name, value):
        return queryset.filter(Q(title__contains=value) | Q(title__icontains=value))
