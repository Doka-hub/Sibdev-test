from django.urls import path

from .views import (
    AddQuotedCurrencyToTrackAPIView,
    QuotedCurrencyValuesListAPIView,
    AnalyticQuotedCurrencyAPIView,
)

urlpatterns = [
    path(
        'currency/user_currency/',
        AddQuotedCurrencyToTrackAPIView.as_view(),
        name='add-quoted-currency-to-track',
    ),
    path(
        'currency/<int:id>/analytics/',
        AnalyticQuotedCurrencyAPIView.as_view(),
        name='analytic-quoted-currencies',
    ),
    path('rates/', QuotedCurrencyValuesListAPIView.as_view(), name='rates'),
]
