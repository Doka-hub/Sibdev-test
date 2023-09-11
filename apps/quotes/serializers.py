from rest_framework import serializers

from .models import TrackedQuotedCurrency, QuotedCurrencyValue


class QuotedCurrencyToTrackSerializer(serializers.ModelSerializer):
    currency = serializers.IntegerField(source='quoted_currency_id')
    threshold = serializers.FloatField(source='threshold_value')

    class Meta:
        model = TrackedQuotedCurrency
        fields = (
            'currency',
            'threshold',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        instance = TrackedQuotedCurrency.objects.create(
            user=user,
            quoted_currency_id=validated_data['quoted_currency_id'],
            threshold_value=validated_data['threshold_value'],
        )
        return instance

    def update(self, instance, validated_data):
        pass


class QuotedCurrencyValueListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    charcode = serializers.CharField()
    date = serializers.CharField()
    value = serializers.FloatField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class AnalyticQuotedCurrencyValueListSerializer(serializers.ModelSerializer):
    threshold = serializers.DecimalField(10, 2, write_only=True)

    charcode = serializers.CharField(source='quoted_currency.name')
    date = serializers.DateTimeField(source='cbr_date')
    value = serializers.FloatField(source='cbr_value')
    is_threshold_exceeded = serializers.BooleanField(read_only=True)
    is_min_value = serializers.BooleanField(read_only=True)
    is_max_value = serializers.BooleanField(read_only=True)

    threshold_match_type = serializers.CharField()
    percentage_ratio = serializers.CharField()

    class Meta:
        model = QuotedCurrencyValue
        fields = (
            'id',
            'date',
            'charcode',
            'value',

            'threshold',

            'is_threshold_exceeded',
            'threshold_match_type',
            'is_min_value',
            'is_max_value',
            'percentage_ratio',
        )
