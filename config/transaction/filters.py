from django_filters import rest_framework as filters

from transaction.models import Transaction


class TransactionFilter(filters.FilterSet):
    date__range = filters.DateFromToRangeFilter(field_name='date')

    class Meta:
        model = Transaction
        fields = [
            'status', 'type', 'category', 'subcategory'
        ]

