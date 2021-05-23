from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter, DateRangeFilter
from .models import Response
from ads.models import Ad
from django.forms import TextInput, Select, DateInput


class ResponseFilter(FilterSet):
    title = CharFilter(field_name='ad__title', lookup_expr='icontains', label='Поиск по заголовкам объявлений', 
                       widget=TextInput(attrs={'placeholder': 'Заголовок объявлений', 'class': 'form-control'}))

    class Meta:
        model = Response
        fields = ['title']
