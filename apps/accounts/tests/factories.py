import factory

from factory.django import DjangoModelFactory

from apps.accounts.models import CustomUser


class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Faker('ascii_free_email')
    password = factory.django.Password('123test123')
