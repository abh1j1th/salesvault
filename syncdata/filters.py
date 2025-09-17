from rest_framework import filters
from django.db.models import Q

class CustomeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        field_names = [field.name for field in queryset.model._meta.fields]
        model_name = queryset.model.__name__
        search = request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(
                Q(deal_id=search) |
                Q(file_name__icontains=search) |
                Q(file_type__icontains=search)
            )
        return queryset
