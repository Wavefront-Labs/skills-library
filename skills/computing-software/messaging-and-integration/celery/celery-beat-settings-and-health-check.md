---
id: computing-software.messaging-and-integration.celery.celery-beat-settings-and-health-check
name: celery-beat-settings-and-health-check
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-beat, celery, beat-schedule, scheduler, cron, liveness-probe, remote-control, inspect-ping]
level: practitioner
status: docs-checked
description: "Configure celery beat settings: schedule, scheduler class, schedule file, cron deadline, and the 5.7 remote-control ping health check."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Beat settings and health-check

Goal: configure periodic scheduling and probe beat's health.

## Core settings
- `beat_schedule` (default `{}`): the periodic task schedule.
- `beat_scheduler` (default `"celery.beat:PersistentScheduler"`): e.g. `"django_celery_beat.schedulers:DatabaseScheduler"`; CLI `-S`.
- `beat_schedule_filename` (default `"celerybeat-schedule"`): file where `PersistentScheduler` stores last run times; the suffix `.db` may be appended; CLI `--schedule`.
- `beat_sync_every` (default 0): tasks sent before another sync; 0 syncs by timing (3 minutes by default via `scheduler.sync_every`); 1 syncs after every task message.
- `beat_max_loop_interval` (default 0): max seconds beat sleeps between schedule checks. Scheduler specific: 300 (5 minutes) for the default scheduler, 5 seconds for the django-celery-beat database scheduler because the schedule may change externally.
- `beat_cron_starting_deadline` (5.3+, default None): seconds beat looks back to decide whether a cron schedule is due. Only the most recent missed run is considered; inside the deadline it runs immediately, otherwise it waits for the next time. `None` means past-due cron jobs always run immediately. Setting it above 3600 is highly discouraged.
- `result_expires` cleanup (`celery.backend_cleanup`) depends on beat running.

## Daemon options (5.4+, all default None)
`beat_logfile`, `beat_pidfile`, `beat_uid`, `beat_gid`, `beat_umask`, `beat_executable`.

## Remote-control ping (5.7+)
`beat_enable_remote_control` (default disabled): beat joins the pidbox exchange as `celerybeat@hostname` (set with `--hostname`; per process `--enable-remote-control`) and answers `celery inspect ping` with `{'ok': 'pong'}`. Probe example for Kubernetes:

```console
$ celery -A proj inspect ping -t 5 -d celerybeat@$(hostname)
```
It exits non-zero when beat does not reply in time. `--timeout` defaults to one second, which a probe that must also open a broker connection can exceed, so pass `-t`.

Gotchas:
- Beat also shows up in destination-less `inspect ping` and `celery status`; only `ping` is implemented, other commands are ignored.
- Only standalone beat is affected; beat embedded in a worker (`-B`) never starts the node.
- It connects separately using `broker_connection_retry_on_startup` (else `broker_connection_retry`) and `broker_connection_max_retries`. Once it gives up it stays given up: the scheduler keeps firing tasks but remote control stays silent and an error is logged. A liveness probe makes the supervisor restart beat, which is the recovery; without one check beat's log.
- Works with RabbitMQ (AMQP) and Redis transports.
- `beat_remote_control_max_tick_age` (default `None` = twice the scheduler loop interval, never below a 60 second floor): stop answering ping when the scheduler pass has not completed that long; `0` always answers. Beat stays silent rather than replying with an error, because `inspect` only exits non-zero when no node replies; each refusal logs a warning (a probe each minute against a stalled beat logs one a minute). A beat that wedges before its first tick also goes stale.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/configuration.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
