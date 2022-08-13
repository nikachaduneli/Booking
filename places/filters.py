import django_filters
from django_filters import FilterSet, RangeFilter, ModelChoiceFilter
from .models import Place


class PlaceFilter(FilterSet):
    city = django_filters.CharFilter(label='City', lookup_expr='icontains')
    price = django_filters.RangeFilter(label='Price Range')
    score = django_filters.RangeFilter(label='score Range')

    class Meta:
        model = Place
        fields = ['city', 'price', 'score']
