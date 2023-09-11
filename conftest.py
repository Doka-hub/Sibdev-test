import random

import pytest
import factory

from pytest_redis.factories import redisdb, redis_proc

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.tests.factories import UserFactory


def authenticate_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture(autouse=True)
def override_django_settings(settings):
    """
    Переопределяет настройки Django для тестов.
    """
    settings.REDIS_HOST = '127.0.0.1'
    settings.REDIS_PORT = 6380


redis_my_proc = redis_proc()
redis_client = redisdb('redis_my_proc')


@pytest.fixture(autouse=True)
def reset_factory_boy_sequences():
    def get_all_subclasses(klass):

        all_subclasses = []
        for subclass in klass.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(get_all_subclasses(subclass))

        return all_subclasses

    for cls in get_all_subclasses(factory.django.DjangoModelFactory):
        cls.reset_sequence()


@pytest.fixture()
def schema_url():
    return reverse('schema')


@pytest.fixture(autouse=True)
def random_seed():
    random.seed(123)


@pytest.fixture(autouse=True)
def factory_faker_seed():
    factory.faker.Faker._get_faker().__class__.seed(12345)


@pytest.fixture()
def users(db):
    return UserFactory.create_batch(3)


@pytest.fixture()
def user(users):
    return users[0]


@pytest.fixture()
def anon_client():
    return APIClient()


@pytest.fixture()
def user_client(user):
    return authenticate_client(user)
