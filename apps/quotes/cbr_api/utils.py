from datetime import date


def make_archive_currencies_endpoint(endpoint: str,  date_: date):
    """
    Формирует специфический ендпоинт для получения архивных записей.

    :param endpoint:
    :param date_:
    :return:
    """
    year, month, day = date_.year, date_.month, date_.day

    month = f'0{month}' if month < 10 else month
    day = f'0{day}' if day < 10 else day
    endpoint = endpoint.format(year=year, month=month, day=day)
    return endpoint
