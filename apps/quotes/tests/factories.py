import factory

from factory.django import DjangoModelFactory

from datetime import datetime

from apps.accounts.tests.factories import UserFactory


class QuotedCurrencyFactory(DjangoModelFactory):
    class Meta:
        model = 'quotes.QuotedCurrency'

    name = factory.Faker('currency_code')


class QuotedCurrencyValueFactory(DjangoModelFactory):
    class Meta:
        model = 'quotes.QuotedCurrencyValue'

    quoted_currency = factory.SubFactory(QuotedCurrencyFactory)
    cbr_id = factory.Sequence(lambda n: n + 1)
    cbr_num_code = factory.Sequence(lambda n: n + 1)
    cbr_nominal = factory.Sequence(lambda n: n + 1)
    cbr_name = factory.Sequence(lambda n: f'Name {n + 1}')
    cbr_value = factory.Faker('pydecimal', positive=True, max_value=10_000)
    cbr_previous_value = factory.Faker('pydecimal', positive=True, max_value=10_000)
    cbr_date = factory.LazyFunction(lambda: datetime(2023, 6, 10))
    cbr_previous_date = factory.LazyFunction(lambda: datetime(2023, 6, 9))


class TrackedQuotedCurrencyFactory(DjangoModelFactory):
    class Meta:
        model = 'quotes.TrackedQuotedCurrency'

    user = factory.SubFactory(UserFactory)
    quoted_currency = factory.SubFactory(QuotedCurrencyFactory)
    threshold_value = factory.Faker('pydecimal', positive=True, max_value=10_000)
