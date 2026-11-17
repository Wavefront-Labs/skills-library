---
id: computing-software.messaging-and-integration.celery.celery-django-integration-first-steps
name: celery-django-integration-first-steps
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-django, celery, django, shared-task, autodiscover-tasks, on-commit, django-celery-results, namespace]
level: practitioner
status: docs-checked
description: "Integrate Celery with Django: celery.py app module, CELERY_ settings namespace, autodiscover_tasks, @shared_task, delay_on_commit, django-celery-results."
sources:
  - https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integrate Celery with Django

Goal: wire a Django project to Celery with Django settings as config.

Celery 5.5.x supports Django 2.2 LTS or newer (use 5.2.x for older Django, 4.4.x below Django 1.11). No separate library is needed since 3.1.

Layout: `proj/manage.py`, `proj/proj/{__init__.py,settings.py,urls.py}`. Create `proj/proj/celery.py` defining the app. Key lines from the page's walkthrough:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')   # before creating the app
app = Celery('proj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

Import that app in `proj/proj/__init__.py` so it loads when Django starts and `@shared_task` uses it.

`namespace='CELERY'` means every option is uppercase and prefixed `CELERY_`: `task_always_eager` becomes `CELERY_TASK_ALWAYS_EAGER`, `broker_url` becomes `CELERY_BROKER_URL`, `worker_concurrency` becomes `CELERY_WORKER_CONCURRENCY`. Example in settings.py: `CELERY_TIMEZONE = "Australia/Tasmania"`, `CELERY_TASK_TRACK_STARTED = True`, `CELERY_TASK_TIME_LIMIT = 30 * 60`. Passing a string (not the settings object) means the worker does not have to serialize the object.

`app.autodiscover_tasks()` finds `tasks.py` in each installed app, so you need not list modules in `imports`. Reusable apps cannot import the project's app, so write tasks with `@shared_task` in `demoapp/tasks.py`.

Transaction pitfall: `send_email.delay(user.pk)` right after `User.objects.create(...)` may run before the commit, so the task may not find the user. Use `transaction.on_commit(lambda: send_email.delay(user.pk))`, or since 5.4 `send_email.delay_on_commit(user.pk)` (a `DjangoTask` method). `delay_on_commit` does NOT return the task ID because nothing is sent until the transaction finishes; use `delay` if you need the id. With a custom task base class, inherit from `DjangoTask` instead of `Task`.

Django 5.1+ connection pooling: if enabled in `DATABASES`, Celery closes the pool in worker processes via `close_pool`, since connections cannot be shared across processes.

django-celery-results: `pip install django-celery-results`, add `'django_celery_results'` to `INSTALLED_APPS` (underscores, no dash), run `python manage.py migrate django_celery_results`, set `CELERY_RESULT_BACKEND = 'django-db'` or `'django-cache'` (with `CELERY_CACHE_BACKEND = 'default'` naming a `CACHES` entry). For DB-backed periodic tasks see django-celery-beat.

Run a dev worker: `celery -A proj worker -l INFO`; use a daemon in production.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (django/first-steps-with-django.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Removed or reworded: the DjangoTask import path (page names only the class).

Method: documentation only; no commands were run.
