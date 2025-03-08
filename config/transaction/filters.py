from django_filters import rest_framework as filters

from transaction.models import Transaction

from django.forms.widgets import DateInput
from django.forms.widgets import MultiWidget


class CustomDateRangeWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            DateInput(attrs={'placeholder': '01.01.2020', 'class': 'form-control'}),
            DateInput(attrs={'placeholder': '01.01.2021', 'class': 'form-control'})
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.end]
        return [None, None]


class TransactionFilter(filters.FilterSet):
    date__range = filters.DateFromToRangeFilter(field_name='date',
                                                label = 'Дата записи',
                                                widget = CustomDateRangeWidget()
                                                )

    class Meta:
        model = Transaction
        fields = [
            'status', 'type', 'category', 'subcategory'
        ]

