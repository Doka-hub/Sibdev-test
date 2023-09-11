from celery import shared_task

from django.db.models import F, Max, CharField, FloatField
from django.db.models.functions import Cast

from datetime import date, timedelta

from .caches import QuotesRedisCache
from .cbr_api import CbrXmlAPI
from .models import TrackedQuotedCurrency, QuotedCurrency, QuotedCurrencyValue


def create_quoted_currency_values(data: dict):
    quoted_currency_values = []
    for name, valute_data in data['Valute'].items():
        quoted_currency, _ = QuotedCurrency.objects.get_or_create(name=name)
        quoted_currency_value, _ = QuotedCurrencyValue.objects.get_or_create(
            quoted_currency=quoted_currency,
            cbr_id=valute_data['ID'],
            cbr_num_code=valute_data['NumCode'],
            cbr_nominal=valute_data['Nominal'],
            cbr_name=valute_data['Name'],
            cbr_value=valute_data['Value'],
            cbr_previous_value=valute_data['Previous'],
            cbr_date=data['Date'],
            cbr_previous_date=data['PreviousDate'],
        )
        quoted_currency_values.append(quoted_currency_value)
    return quoted_currency_values


@shared_task(name='collect_daily_quotes')
def collect_daily_quotes():
    """
    Загружает ежедневные котировки
    :return:
    """
    cache = QuotesRedisCache()
    cache.delete_data_from_cache()

    api = CbrXmlAPI()
    last_quoted_currencies, status_code = api.get_last_quoted_currencies()
    if status_code == 200:
        create_quoted_currency_values(last_quoted_currencies)


@shared_task(name='check_threshold')
def check_threshold():
    """
    Проверяет превышение ПЗ и отправляет уведомление на почту
    :return:
    """
    tracked_quoted_currencies = TrackedQuotedCurrency.objects.all()
    last_date = QuotedCurrencyValue.objects.aggregate(last_date=Max('cbr_date'))['last_date']
    data = {}
    for tracked_quoted_currency in tracked_quoted_currencies:
        values = tracked_quoted_currency.quoted_currency.values.filter(
            cbr_date=last_date,
            cbr_value__gte=tracked_quoted_currency.threshold_value,
        ).annotate(
            charcode=F('quoted_currency__name'),
            date=Cast('cbr_date', CharField()),
            value=Cast('cbr_value', FloatField()),
        ).values(
            'id',
            'charcode',
            'date',
            'value',
        )
        if data.get(tracked_quoted_currency) is None:
            data[tracked_quoted_currency] = []
        data[tracked_quoted_currency].append(list(values))

    for tracked_quoted_currency in data:
        print(
            f'{tracked_quoted_currency.user.email}\n'
            f'Данные котировки превысили ПЗ ({tracked_quoted_currency.threshold_value}):\n'
            f'{data[tracked_quoted_currency]}',
        )


@shared_task(name='collect_archive_quotes')
def collect_archive_quotes():
    """
    Загружает ежедневные котировки
    :return:
    """
    api = CbrXmlAPI()
    date_generator = (date.today() - timedelta(days=i) for i in range(30))
    for date_ in date_generator:
        archive_quoted_currencies, status_code = api.get_archive_quoted_currencies(date_)
        if status_code == 200:
            create_quoted_currency_values(archive_quoted_currencies)
