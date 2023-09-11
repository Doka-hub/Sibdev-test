from django.contrib import admin

from .models import QuotedCurrency, QuotedCurrencyValue, TrackedQuotedCurrency


class QuotedCurrencyValueInline(admin.TabularInline):
    model = QuotedCurrencyValue
    extra = 0


class QuotedCurrencyAdmin(admin.ModelAdmin):
    inlines = [QuotedCurrencyValueInline]


class TrackedQuotedCurrencyAdmin(admin.ModelAdmin):
    pass


admin.site.register(QuotedCurrency, QuotedCurrencyAdmin)
admin.site.register(TrackedQuotedCurrency, TrackedQuotedCurrencyAdmin)
