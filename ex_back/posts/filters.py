from django.db.models import Q
from django.forms import CharField
from django_filters.rest_framework import (
    FilterSet,
    DateFilter,
    CharFilter,
)

from .models import Post, PostTag


class PostFilterSet(FilterSet):
    keyword = CharFilter(method='keyword_filter', label='Search')

    date = DateFilter(method='date_filter', label='Date')
    date__gte = DateFilter('datetime', 'gte')
    date__lte = DateFilter(method='date_lte_filter')

    tag = CharFilter(method='tag_filter', label='Tag')

    class Meta:
        model = Post
        fields = ('keyword', 'date')

    def keyword_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(body__icontains=value)
        )

    def date_filter(self, queryset, name, value):
        return queryset.filter(
            datetime__year=value.year,
            datetime__month=value.month,
            datetime__day=value.day
        )

    def date_lte_filter(self, queryset, name, value):
        return queryset.filter(
            datetime__year__lte=value.year,
            datetime__month__lte=value.month,
            datetime__day__lte=value.day
        )

    def tag_filter(self, queryset, name, value):
        tags = value.strip(',').split(',')
        return queryset.filter(tags__name__in=tags).distinct()
