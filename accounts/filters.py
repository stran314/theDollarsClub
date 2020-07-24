import django_filters
from django_filters import DateFilter, CharFilter
from django.forms.widgets import TextInput, Select

from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr='gte',
    widget = TextInput(attrs={'class': 'filter-control', 'placeholder' : 'From: MM/DD/YYYY'}))

    end_date = DateFilter(field_name="date_created", lookup_expr='lte',
    widget = TextInput(attrs={'class': 'filter-control', 'placeholder' : 'To: MM/DD/YYYY'}))

    note = CharFilter(field_name='note', lookup_expr='icontains',
    widget = TextInput(attrs={'class': 'filter-control', 'placeholder' : 'Note'}))

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['date_created']

    def __init__(self, *args, **kwargs):
        super(OrderFilter, self).__init__(*args, **kwargs)
        self.filters['customer'].field.widget.attrs.update({'class': 'filter-control'})
        self.filters['product'].field.widget.attrs.update({'class': 'filter-control'})
        self.filters['status'].field.widget.attrs.update({'class': 'filter-control'})
