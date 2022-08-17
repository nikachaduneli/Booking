import django_filters
from django_filters import FilterSet
from .models import Place
from django_filters.widgets import RangeWidget


class MyRangeWidget(RangeWidget):
    template_name = "widgets/my_range_widget.html"


class PlaceFilter(FilterSet):
    city = django_filters.CharFilter(label='City', lookup_expr='icontains')
    price = django_filters.RangeFilter(label='Price Range', widget=MyRangeWidget)
    score = django_filters.RangeFilter(label='score Range', widget=MyRangeWidget)

    class Meta:
        model = Place
        fields = ['city', 'price', 'score']
