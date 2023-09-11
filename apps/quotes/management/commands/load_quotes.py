from django.core.management.base import BaseCommand

from apps.quotes.tasks import collect_archive_quotes


class Command(BaseCommand):
    help = 'Загружает данные по котировкам за 30 дней'

    def handle(self, *args, **options):
        collect_archive_quotes.delay()
