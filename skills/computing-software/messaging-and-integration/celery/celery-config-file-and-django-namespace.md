---
id: computing-software.messaging-and-integration.celery.celery-config-file-and-django-namespace
name: celery-config-file-and-django-namespace
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-file, celery, settings, lowercase-settings, django, celery-upgrade, timezone, utc]
level: practitioner
status: docs-checked
description: "Load Celery settings from celeryconfig.py or Django settings with the CELERY_ namespace, migrate old uppercase names, set timezone and UTC."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configure Celery from a config module or Django settings

Goal: get settings into the app using the 4.0+ lowercase names, including the Django `CELERY_` namespace.

## Config module
With the default loader, create `celeryconfig.py` and make sure it is on the Python path. The docs' starter file:

```python
broker_url = 'amqp://guest:guest@localhost:5672//'
imports = ('myapp.tasks',)
result_backend = 'db+sqlite:///results.db'
task_annotations = {'tasks.add': {'rate_limit': '10/s'}}
```

## Django namespace
Documented names are lowercase (`broker_url`, `task_always_eager`). With a namespace:

```python
app.config_from_object('django.conf:settings', namespace='CELERY')
```

write them uppercase with the prefix in `settings.py`:

```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_TASK_ALWAYS_EAGER = True
CELERY_WORKER_CONCURRENCY = 4
```

The namespace is recommended because it keeps Celery settings apart from Django and other apps' settings.

## Migrating old names
Version 4.0 introduced lowercase settings. Prefixes changed: `celery_beat_` became `beat_`, `celeryd_` became `worker_`, and most top-level `celery_` settings moved under `task_`.
Celery still reads old config files until Celery 6.0, after which support is removed. The `celery upgrade` command handles many cases, including Django settings with a namespace:

```console
$ celery upgrade settings proj/settings.py --django
```

## Time zone
- `enable_utc`: enabled by default since 3.0. Converts dates/times in messages to UTC. Workers below Celery 2.5 assume local timezone, so only enable if all workers are upgraded.
- `timezone`: default `"UTC"`; any zone supported by the `ZoneInfo` library. If `enable_utc` is false, the system local timezone is used instead.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/configuration.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Removed or reworded: the old-to-new setting-name example list (not on the page).

Method: documentation only; no commands were run.
