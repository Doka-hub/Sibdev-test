import json

from django.urls import reverse

from apps.quotes.models import TrackedQuotedCurrency
from .factories import TrackedQuotedCurrencyFactory


def test_quotes_list_by_anon(
    redis_client,
    anon_client,
    quotes_list_url,
    quoted_currencies,
    snapshot,
):
    response = anon_client.get(quotes_list_url)
    snapshot.assert_match(response.json())


def test_cached_quotes_list_by_anon(
    redis_client,
    anon_client,
    quotes_list_url,
    quoted_currencies,
    snapshot,
):
    anon_client.get(quotes_list_url)
    cached_data = json.loads(redis_client.get('quotes_cache:values_list'))

    response = anon_client.get(quotes_list_url)

    assert response.json() == cached_data
    snapshot.assert_match(response.json())


def test_quotes_list_by_user(
    user,
    user_client,
    quotes_list_url,
    quoted_currencies,
    snapshot,
):
    quoted_currency = quoted_currencies[0]
    TrackedQuotedCurrencyFactory.create_batch(3, user=user, quoted_currency=quoted_currency)
    response = user_client.get(quotes_list_url)
    snapshot.assert_match(response.json())


def test_add_quote_to_track_by_user(
    user,
    user_client,
    add_quote_to_track_url,
    quoted_currency,
):
    tracked_quoted_currencies = TrackedQuotedCurrency.objects.filter(
        user=user,
        quoted_currency=quoted_currency,
    )
    assert tracked_quoted_currencies.exists() is False

    response = user_client.post(
        add_quote_to_track_url,
        {
            'currency': quoted_currency.id,
            'threshold': quoted_currency.values.first().cbr_value - 10
        },
    )

    assert response.status_code == 201
    assert tracked_quoted_currencies.exists() is True


def test_analytic_quoted_currency(
    user_client,
    quoted_currency,
    snapshot,
):
    url = reverse(
        'analytic-quoted-currencies',
        args=(quoted_currency.id,),
    )
    threshold = quoted_currency.values.last().cbr_value
    response = user_client.get(url, data={'threshold': threshold})

    assert response.status_code == 200
    response_data = response.json()

    snapshot.assert_match(response.json())
    for quoted_currency_data in response_data:
        if quoted_currency_data['value'] > threshold:
            assert quoted_currency_data['is_threshold_exceeded'] is True
