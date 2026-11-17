---
id: computing-software.messaging-and-integration.celery.beat-run-health-checks
name: beat-run-health-checks
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, beat, health-check, liveness-probe, kubernetes, scheduler, django-celery-beat, celery-beat-operations]
level: practitioner
status: docs-checked
description: "Start celery beat, choose the schedule file, enable remote-control health checks and a Kubernetes liveness probe, and use custom or django-celery-beat schedulers."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run beat reliably and detect a wedged scheduler.

## Start

```console
$ celery -A proj beat
$ celery -A proj worker -B          # embedded; not recommended for production
$ celery -A proj beat -s /path/to/run/celerybeat-schedule
```

Beat stores last run times in a local file (`celerybeat-schedule` by default), so it needs write access to the current directory or the file given with `-s`. To daemonize see the daemonizing guide.

## Health checks (5.7+)

Set `beat_enable_remote_control` (or `--enable-remote-control`). Beat joins the remote-control exchange as node `celerybeat@hostname` and answers ping:

```console
$ celery -A proj inspect ping -t 5 -d celerybeat@$(hostname)
->  celerybeat@example.com: OK
        pong
```

It exits non-zero if nobody replies in the timeout (default one second; allow room, since the probe must make its own broker connection). Beat stops answering when the scheduler has not completed a pass for `beat_remote_control_max_tick_age` seconds (default twice the interval the scheduler settled on); `0` answers regardless. Silence is deliberate because `celery inspect` only exits non-zero when no node replies.

Kubernetes: use a liveness probe (a readiness probe restarts nothing because beat sits behind no Service). Because the check goes over the broker, give it a tolerant threshold:

```yaml
livenessProbe:
  exec:
    command: [/bin/sh, -c, "celery -A proj inspect ping -t 10 -d celerybeat@$(hostname)"]
  initialDelaySeconds: 60
  periodSeconds: 60
  failureThreshold: 5
```

A wedged beat then restarts about fifteen minutes after its last tick. A heartbeat file touched each tick has no broker dependency but is only visible inside the container.

Gotchas: beat shows in destination-less `inspect ping` and `celery status`, changing node counts; it implements only `ping` (`celery control shutdown` leaves beat running); embedded beat (`-B`) starts no control node; node names must be unique, so use `--hostname` if two beats share one; remote control needs fanout exchanges (RabbitMQ or Redis), otherwise beat logs one warning and carries on; if the control node gives up on the broker it does not come back until restart.

## Schedulers

`--scheduler` picks the class. The default `celery.beat.PersistentScheduler` keeps last run times in a `shelve` file. Since 5.7 an `is_due()` exception is logged and retried after `max_interval` while other entries run; entries that can no longer be loaded trigger a warning and the store is recreated from `beat_schedule`, losing all last-run times.

django-celery-beat: `pip install django-celery-beat`, add `'django_celery_beat'` (underscores) to `INSTALLED_APPS`, run `python manage.py migrate`, then:

```console
$ celery -A proj beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

This can also be set as `beat_scheduler`. Manage tasks in the Django admin.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/periodic-tasks.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
