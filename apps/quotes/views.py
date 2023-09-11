import decimal

from django.db.models import (
    ExpressionWrapper,
    Case,
    When,
    Value,
    Min,
    Max,
    BooleanField,
    CharField,
    FloatField,
    F,
)
from django.db.models.functions import Round, Concat, Cast
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .caches import QuotesRedisCache, get_cache_key, get_sorted_cached_data
from .filters import AnalyticQuotedCurrencyFilter
from .models import QuotedCurrencyValue
from .serializers import (
    QuotedCurrencyToTrackSerializer,
    QuotedCurrencyValueListSerializer,
    AnalyticQuotedCurrencyValueListSerializer,
)
from .validators import validate_decimal


@extend_schema(
    tags=['Currency'],
    summary='Добавление котируемой валюты в список отслеживаемых с установкой порогового значения',
)
class AddQuotedCurrencyToTrackAPIView(CreateAPIView):
    serializer_class = QuotedCurrencyToTrackSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=['Rates'],
    summary='Получение последних загруженных котировок',
    parameters=[
        OpenApiParameter(
            'order_by',
            enum=['-cbr_value', 'cbr_value'],
        ),
    ],
)
class QuotedCurrencyValuesListAPIView(ListAPIView):
    queryset = QuotedCurrencyValue.objects.all()
    serializer_class = QuotedCurrencyValueListSerializer

    def list(self, request, *args, **kwargs):
        cache = QuotesRedisCache()
        cache_key = get_cache_key(user=self.request.user)
        cached_data = cache.get_data_from_cache(cache_key)

        order_by = self.request.query_params.get('order_by', 'id')
        if cached_data is None:
            queryset = self.get_queryset().order_by(order_by)
            serializer = self.get_serializer(queryset, many=True)
            cache.set_data_to_cache(cache_key, list(queryset))
        else:
            sorted_cached_data = get_sorted_cached_data(cached_data, order_by)
            serializer = self.get_serializer(sorted_cached_data, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = QuotedCurrencyValue.objects.filter(
                quoted_currency__tracked_by_users__user=self.request.user,
            )
        else:
            queryset = self.queryset
        last_date = queryset.aggregate(last_date=Max('cbr_date'))['last_date']
        return queryset.filter(cbr_date=last_date).annotate(
            charcode=F('quoted_currency__name'),
            date=Cast('cbr_date', CharField()),
            value=Cast('cbr_value', FloatField()),
        ).values(
            'id',
            'charcode',
            'date',
            'value',
        )


@extend_schema(
    tags=['Currency'],
    summary='Получение аналитических данных по котирумой валюте за период',
    filters=True,
    parameters=[
        OpenApiParameter(
            'threshold',
            decimal.Decimal,
            required=True,
        ),
        OpenApiParameter(
            'date_from',
            description='Example : 2007-03-09T00:00:00.000Z',
        ),
        OpenApiParameter(
            'date_to',
            description='Example : 2007-03-09T00:00:00.000Z',
        ),
    ],
)
class AnalyticQuotedCurrencyAPIView(ListAPIView):
    queryset = QuotedCurrencyValue.objects.all()
    serializer_class = AnalyticQuotedCurrencyValueListSerializer

    filterset_class = AnalyticQuotedCurrencyFilter

    def list(self, request, *args, **kwargs):
        threshold = self.request.query_params.get('threshold')
        validate_decimal('threshold', threshold)

        queryset = self.filter_queryset(self.get_queryset())

        min_value = queryset.aggregate(min_value=Min('cbr_value'))['min_value']
        max_value = queryset.aggregate(max_value=Max('cbr_value'))['max_value']

        queryset = queryset.annotate(
            is_min_value=Case(
                When(
                    cbr_value=min_value,
                    then=True,
                ),
                default=False,
                output_field=BooleanField(),
            ),
            is_max_value=Case(
                When(
                    cbr_value=max_value,
                    then=True,
                ),
                default=False,
                output_field=BooleanField(),
            ),
            is_threshold_exceeded=Case(
                When(
                    cbr_value__gte=threshold,
                    then=True,
                ),
                default=False,
                output_field=BooleanField(),
            ),
            threshold_match_type=Case(
                When(
                    cbr_value=threshold,
                    then=Value('equal'),
                ),
                When(
                    cbr_value__lt=threshold,
                    then=Value('less'),
                ),
                When(
                    cbr_value__gt=threshold,
                    then=Value('exceeded'),
                ),
                output_field=CharField(max_length=10),
            ),
            percentage_ratio=Concat(
                Round(
                    ExpressionWrapper(
                        ((F('cbr_value') / threshold) * 100),
                        output_field=FloatField()
                    ),
                    2,
                ),
                Value('%'),
                output_field=CharField(),
            )
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset.filter(quoted_currency_id=self.kwargs['id'])
        return queryset
