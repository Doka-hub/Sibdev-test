from datetime import date

from apps.quotes.cbr_api import CbrXmlAPI


def test_get_last_quoted_currencies():
    api = CbrXmlAPI()
    response, status_code = api.get_last_quoted_currencies()
    assert status_code == 200


def test_get_archive_quoted_currencies():
    api = CbrXmlAPI()
    response, status_code = api.get_archive_quoted_currencies(date(2023, 6, 10))
    assert status_code == 200
