---
id: computing-software.messaging-and-integration.celery.beat-schedule-entries
name: beat-schedule-entries
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, beat, periodic-tasks, beat-schedule, add-periodic-task, timezone, celery-beat-schedule]
level: practitioner
status: docs-checked
description: "Define Celery beat periodic tasks with add_periodic_task or beat_schedule, entry fields, timezone and DST behaviour, relative schedules, and scheduling workflows."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: register periodic tasks for `celery beat`, which kicks off tasks that available workers then execute. Run only one scheduler per schedule or you get duplicates.

## add_periodic_task

```python
@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
    sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')
    sender.add_periodic_task(30.0, test.s('world'), expires=10)
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )
```

Giving an explicit `name` stops a second entry with the same signature replacing the first. Using `on_after_configure` avoids evaluating the app at module level for `test.s()`. It fires after the app is set up, so tasks outside the module declaring the app (e.g. `tasks.py` found by `autodiscover_tasks`) must use a later signal such as `on_after_finalize`.

## beat_schedule

```python
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}
app.conf.timezone = 'UTC'
```

A single-item `args` tuple needs the trailing comma. Fields: `task` (the registered task name, not the import path), `schedule` (seconds, `timedelta`, `crontab`, or a custom `schedule` subclass), `args`, `kwargs`, `options` (any `apply_async` argument such as `exchange`, `routing_key`, `expires`), and `relative`.

## Timing details

A `timedelta` schedule sends the first task that long after beat starts, then every interval after the last run. With default `relative=False`, numeric and `timedelta` schedules use elapsed time across DST: `timedelta(days=1)` is 24 hours. To run at the same local time daily, use `crontab(hour=12, minute=0)`. With `relative=True` the interval is rounded to the clock (day or more intervals advance by local calendar days to midnight).

Like cron, runs can overlap; use a locking strategy if that matters.

## Time zones

Default is UTC; set `timezone = 'Europe/London'` (on the app or in config). The default scheduler resets its schedule when the timezone changes; others, such as the Django database scheduler, do not and need a manual reset: `PeriodicTask.objects.update(last_run_at=None)` (from `django_celery_beat.models` for Celery 4.0+).

## Scheduling a group or chain

An entry stores only a task name and arguments, so you can't pass a group, chain or chord. Wrap it in a task and schedule that:

```python
@app.task
def run_add_group():
    group(add.s(i, i) for i in range(10)).apply_async()

sender.add_periodic_task(30.0, run_add_group.s(), name='add group every 30')
```

Only dispatch with `apply_async()`; don't call `get()` inside the task.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/periodic-tasks.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
