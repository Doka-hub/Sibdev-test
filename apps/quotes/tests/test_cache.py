from django.db.models import F, CharField, FloatField
from django.db.models.functions import Cast

from apps.quotes.caches import QuotesRedisCache
from apps.quotes.models import QuotedCurrencyValue


def test_delete_cached_data(redis_client, quoted_currencies):
    quotes = QuotedCurrencyValue.objects.annotate(
        charcode=F('quoted_currency__name'),
        date=Cast('cbr_date', CharField()),
        value=Cast('cbr_value', FloatField()),
    ).values(
        'id',
        'charcode',
        'date',
        'value',
    )
    cache = QuotesRedisCache()
    cache.set_data_to_cache('values_list', list(quotes))

    assert len(redis_client.keys(f'{cache.BASE_KEY}*')) > 0
    assert len(redis_client.get(f'{cache.BASE_KEY}:values_list')) > 0

    cache.delete_data_from_cache()

    assert len(redis_client.keys(f'{cache.BASE_KEY}*')) == 0
