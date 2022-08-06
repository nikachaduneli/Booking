from django_filters import FilterSet, RangeFilter
from .models import Place


class PlaceFilter(FilterSet):
    price = RangeFilter()

    class Meta:
        model = Place
        fields = ['city', 'price']
