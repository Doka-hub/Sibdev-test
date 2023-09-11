import pytest

from celery.result import AsyncResult

from apps.quotes.tasks import collect_daily_quotes, check_threshold, collect_archive_quotes


@pytest.mark.django_db(transaction=True)
def test_collect_daily_quotes(celery_app, celery_worker, db):
    task = collect_daily_quotes.delay()
    result = AsyncResult(task.id)
    result.get()
    assert result.state == 'SUCCESS'


@pytest.mark.django_db(transaction=True)
def test_check_threshold(celery_app, celery_worker, tracked_quoted_currencies):
    task = check_threshold.delay()
    result = AsyncResult(task.id)
    result.get()
    assert result.state == 'SUCCESS'


@pytest.mark.django_db(transaction=True)
def test_collect_archive_quotes(celery_app, celery_worker, db):
    task = collect_archive_quotes.delay()
    result = AsyncResult(task.id)
    result.get()
    assert result.state == 'SUCCESS'
