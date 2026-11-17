---
id: computing-software.web-development.django.background-tasks-with-celery
name: background-tasks-with-celery
category: computing-software
field: web-development
product: django
tags: [django, celery, background-tasks, celery-beat, redis, task-retries, idempotency, python, web-development]
level: practitioner
status: docs-checked
description: "Running Django background work with Celery: app setup, task design (ids not objects, idempotent), retries and acks_late, on_commit enqueueing, beat schedules and monitoring."
sources:
  - https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
  - https://docs.celeryq.dev/en/stable/userguide/tasks.html
  - https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
  - https://docs.djangoproject.com/en/stable/topics/db/transactions/#performing-actions-after-commit
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
  - https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html
  - https://docs.djangoproject.com/en/stable/releases/6.0/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Background tasks with Celery

**Goal:** slow or unreliable work (emails, webhooks, reports) off the request path, with retries that don't duplicate effects.

## 1. Setup
```python
# config/celery.py
import os
from celery import Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# config/__init__.py
from .celery import app as celery_app
__all__ = ("celery_app",)

# settings.py
CELERY_BROKER_URL = env("REDIS_URL")
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_TIME_LIMIT = 300; CELERY_TASK_SOFT_TIME_LIMIT = 240
```
```bash
celery -A config worker --loglevel=INFO --concurrency=4
celery -A config beat --loglevel=INFO          # exactly one beat process
```

## 2. Task design
```python
@shared_task(bind=True, autoretry_for=(requests.RequestException,), retry_backoff=True,
             retry_backoff_max=600, retry_jitter=True, max_retries=8)
def send_invoice(self, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    if invoice.sent_at:                       # idempotent: safe to run twice
        return
    mailer.send(invoice)
    Invoice.objects.filter(pk=invoice_id, sent_at__isnull=True).update(sent_at=timezone.now())
```
- Pass ids, not model instances, so the task reads current data. The default serializer is JSON (since Celery 4.0).
- With `acks_late`, a worker crash re-delivers the task: design for at-least-once execution.
- Keep tasks small; chain/group for workflows (`chain(a.s(id), b.s())`).

## 3. Enqueue after commit
```python
with transaction.atomic():
    invoice = Invoice.objects.create(...)
    transaction.on_commit(lambda: send_invoice.delay(invoice.pk))
```
Enqueueing inside the transaction lets the worker run before the row is visible (`DoesNotExist`). Celery 5.4+ adds `delay_on_commit()`.

## 4. Periodic tasks
```python
CELERY_BEAT_SCHEDULE = {
    "nightly-report": {"task": "reports.tasks.nightly", "schedule": crontab(hour=2, minute=0)},
}
```
`django-celery-beat` stores schedules in the DB (editable in admin). Run a single beat instance.

## 5. Operations
- Redis broker: the visibility timeout (default 1 hour, set through `broker_transport_options`, or `CELERY_BROKER_TRANSPORT_OPTIONS` with the namespace) is how long the broker waits for an acknowledgement before redelivering a message to another worker; keep it above your longest task and see the Redis broker caveats.
- Monitor with Flower (see the Celery monitoring guide); alert on queue length and failure rate.
- Separate queues for slow vs fast tasks (`task_routes`) so reports don't block password-reset emails.
- Tests: `CELERY_TASK_ALWAYS_EAGER = True` runs tasks locally and blocks until they return, but Celery's testing guide says eager mode is by definition not suitable for unit tests; call the task function directly and use a real worker for integration tests.
- Django 6.0 adds a built-in tasks framework (`django.tasks`, `@task`, `.enqueue()`). It defines and queues tasks only; its two built-in backends are for development and testing, and running tasks needs external workers.

## Verify
- [ ] Killing a worker mid-task results in the task re-running without duplicate side effects.
- [ ] Tasks are enqueued via `on_commit` (grep for `.delay(` inside atomic blocks).
- [ ] Queue depth and failures visible in monitoring.

## Checked
Date: 2026-10-25. Documentation: Celery docs source (celery/celery main, commit of 2026-10-24: tasks, configuration, periodic-tasks, Django first steps, Redis broker, workers, testing, monitoring) and Django 6.0 release notes.
Confirmed: `config_from_object(..., namespace="CELERY")`, `autodiscover_tasks`, `autoretry_for`, `retry_backoff`, `retry_backoff_max` (default 600), `retry_jitter`, `max_retries`, `acks_late`, `worker_prefetch_multiplier`, `task_time_limit` and `task_soft_time_limit`, `delay_on_commit` (added in Celery 5.4), single beat scheduler and `django-celery-beat`, Redis visibility timeout default of 1 hour, JSON default serializer, `task_routes`, `--concurrency`, Django 6.0 `django.tasks`.
Corrected or removed: short `-l info` flags replaced with the documented `--loglevel`; unsupported pickle, metrics-exporter and alternative-library (django-rq, Dramatiq, Huey) claims; the eager-mode testing advice now follows Celery's testing guide.
Method: documentation only; no commands were run.
