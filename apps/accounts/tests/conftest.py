import pytest

from django.urls import reverse


@pytest.fixture()
def register_url():
    return reverse('accounts:register')


@pytest.fixture()
def login_url():
    return reverse('accounts:login')
