from datetime import date
from typing import TypeVar
from urllib.parse import urljoin

import requests
from django.conf import settings

from .utils import make_archive_currencies_endpoint

responseJson = TypeVar('responseJson', bound=dict)
responseStatusCode = TypeVar('responseStatusCode', bound=int)


class CbrXmlAPI:
    BASE_API_URL = settings.CBR_XML_BASE_API_URL
    API_ENDPOINTS = {
        'archive': settings.CBR_XML_API_ENDPOINTS['archive'],
        'daily': settings.CBR_XML_API_ENDPOINTS['daily'],
    }

    def __init__(self, base_api_url: str = settings.CBR_XML_BASE_API_URL):
        if base_api_url is not None:
            self.BASE_API_URL = base_api_url

    def _build_url(self, endpoint):
        return urljoin(self.BASE_API_URL, endpoint)

    def _get(self, endpoint, params=None) -> tuple[responseJson, responseStatusCode]:
        url = self._build_url(endpoint)
        response = requests.get(url, params=params)
        return response.json(), response.status_code

    def get_archive_quoted_currencies(self, date_: date):
        endpoint = make_archive_currencies_endpoint(self.API_ENDPOINTS['archive'], date_)
        response = self._get(endpoint)
        return response

    def get_last_quoted_currencies(self):
        response = self._get(self.API_ENDPOINTS['daily'])
        return response
