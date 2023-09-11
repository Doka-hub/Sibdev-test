import decimal

from rest_framework.exceptions import ValidationError


def validate_decimal(field_name, value):
    try:
        decimal_value = decimal.Decimal(value)
    except (ValueError, TypeError, decimal.InvalidOperation):
        raise ValidationError({field_name: 'Укажите число!'})

    if decimal_value <= 0:
        raise ValidationError({field_name: 'Значение не может быть меньше 0!'})
