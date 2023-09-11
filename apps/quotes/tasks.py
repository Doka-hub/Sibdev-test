from celery import shared_task

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail

from datetime import date, timedelta

from .cbr_api import CbrXmlAPI
from .models import TrackedQuotedCurrency, QuotedCurrency, QuotedCurrencyValue


@shared_task()
def send_email(user_id: int):
    """
    Отправляет данные на почту

    :param user_id:
    :return:
    """
    user = User.objects.get(id=user_id)
    send_mail(
        'Инфо',
        'Произвольое сообщение :)',
        settings.EMAIL_HOST_USER,
        [user.email],
    )


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
    api = CbrXmlAPI()
    last_quoted_currencies, status_code = api.get_last_quoted_currencies()
    if status_code == 200:
        create_quoted_currency_values(last_quoted_currencies)


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
            quoted_currency_values = create_quoted_currency_values(archive_quoted_currencies)
            tracked_quoted_currencies = TrackedQuotedCurrency.objects.filter(
                quoted_currency__values__in=quoted_currency_values,
            )
