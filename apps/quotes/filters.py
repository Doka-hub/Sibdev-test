from django_filters import rest_framework as filters
from django_filters.fields import DateTimeRangeField
from django_filters.widgets import DateRangeWidget

from .models import QuotedCurrencyValue


class CustomDateRangeWidget(DateRangeWidget):
    suffixes = ['from', 'to']


class CustomDateTimeRangeField(DateTimeRangeField):
    widget = CustomDateRangeWidget


class CustomDateTimeFromToRangeFilter(filters.DateTimeFromToRangeFilter):
    field_class = CustomDateTimeRangeField


class AnalyticQuotedCurrencyFilter(filters.FilterSet):
    date = CustomDateTimeFromToRangeFilter('cbr_date', widget=CustomDateRangeWidget)

    class Meta:
        model = QuotedCurrencyValue
        fields = [
            'date',
        ]
