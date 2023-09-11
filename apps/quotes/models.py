from django.db import models

from apps.accounts.models import CustomUser


class TrackedQuotedCurrency(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='tracked_quoted_currencies',
        verbose_name='Пользователь',
    )
    quoted_currency = models.ForeignKey(
        'QuotedCurrency',
        on_delete=models.CASCADE,
        related_name='tracked_by_users',
        verbose_name='Отслеживаемая Валюта',
    )
    threshold_value = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='Пороговое Значение',
    )


class QuotedCurrency(models.Model):
    name = models.CharField(max_length=3, unique=True, verbose_name='Название')

    def __str__(self):
        return self.name


class QuotedCurrencyValue(models.Model):
    quoted_currency = models.ForeignKey(
        QuotedCurrency,
        on_delete=models.CASCADE,
        related_name='values',
        verbose_name='Валюта',
    )
    cbr_id = models.CharField(max_length=10, verbose_name='ID ЦБ РФ')
    cbr_num_code = models.CharField(max_length=3, verbose_name='Числовой Код ЦБ РФ')
    cbr_nominal = models.IntegerField(verbose_name='Номинал ЦБ РФ')
    cbr_name = models.CharField(max_length=255, verbose_name='Название ЦБ РФ')
    cbr_value = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='Значение ЦБ РФ')
    cbr_previous_value = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        verbose_name='Предыдущее Значение ЦБ РФ',
    )
    cbr_date = models.DateTimeField(verbose_name='Дата')
    cbr_previous_date = models.DateTimeField(verbose_name='Предыдущая Дата')
