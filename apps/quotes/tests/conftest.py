import pytest
from django.urls import reverse

from .factories import (
    QuotedCurrencyFactory,
    QuotedCurrencyValueFactory,
    TrackedQuotedCurrencyFactory,
)


@pytest.fixture()
def quotes_list_url():
    return reverse('rates')


@pytest.fixture()
def add_quote_to_track_url():
    return reverse('add-quoted-currency-to-track')


@pytest.fixture()
def quoted_currencies(db):
    quoted_currencies = QuotedCurrencyFactory.create_batch(3)
    for quoted_currency in quoted_currencies:
        QuotedCurrencyValueFactory.create_batch(3, quoted_currency=quoted_currency)
    return quoted_currencies


@pytest.fixture()
def quoted_currency(quoted_currencies):
    return quoted_currencies[0]


@pytest.fixture()
def tracked_quoted_currencies(db, quoted_currencies, user):
    tracked_quoted_currencies = []
    for quoted_currency in quoted_currencies:
        tracked_quoted_currencies.append(
            TrackedQuotedCurrencyFactory.create(
                user=user,
                quoted_currency=quoted_currency,
            ),
        )
    return tracked_quoted_currencies


@pytest.fixture()
def tracked_quoted_currency(tracked_quoted_currencies):
    return tracked_quoted_currencies[0]
