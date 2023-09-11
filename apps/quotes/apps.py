from django.apps import AppConfig


class QuotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.quotes'

    def ready(self):
        from django_celery_beat.models import PeriodicTask
        from django_celery_beat.schedulers import CrontabSchedule

        crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
            hour=12,
            minute=0,
            timezone='Europe/Moscow',
        )
        PeriodicTask.objects.get_or_create(
            name='',
            task='apps.quotes.tasks.collect_daily_quotes',
            crontab=crontab_schedule,
        )
