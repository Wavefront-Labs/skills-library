---
id: computing-software.messaging-and-integration.celery.celery-monitoring-cli-flower-brokers
name: celery-monitoring-cli-flower-brokers
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-monitoring, celery, inspect, flower, rabbitmqctl, redis-cli, purge, queue-length]
level: practitioner
status: docs-checked
description: "Monitor a Celery cluster with celery inspect/control/purge, Flower, rabbitmqctl and redis-cli queue length checks, and know their gotchas."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/monitoring.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor a Celery cluster from the CLI, Flower and the broker

Goal: see workers, tasks and queue depth, and clear queues safely.

`celery --help` lists commands; `celery <command> --help` shows one. Useful commands (all take `-A proj`):
- `status`: list active nodes. `shell`: Python shell with `celery` (the app) and known tasks in locals (skip tasks with `--without-tasks`; force `--ipython`, `--bpython` or `--python`).
- `result -t tasks.add <task_id>`: show a result (task name can be omitted unless the task uses a custom result backend).
- `inspect active | scheduled | reserved | revoked | registered | stats`. `scheduled` shows tasks reserved because of `eta`/`countdown`; `reserved` shows prefetched tasks waiting to run (excluding ETA tasks).
- `inspect query_task id1 id2 ...`: info for tasks that are scheduled, reserved or active on any worker; since 5.7 scheduled ETA tasks are included.
- `control enable_events` / `disable_events`.
- `purge` removes all messages from queues in the queues setting, with no undo. Narrow it: `purge -Q celery,foo,bar` or exclude with `purge -X celery`.
- `migrate redis://localhost amqp://localhost` moves tasks between brokers (experimental; back up first).

All inspect/control commands accept `--timeout` (seconds to wait for replies; raise it if latency prevents replies) and `-d/--destination`, e.g. `celery -A proj inspect -d w1@e.com,w2@e.com reserved`.

Flower (recommended monitor): `pip install flower`, then `celery -A proj flower` (default http://localhost:5555, change with `--port=5555`). Broker via `celery --broker=amqp://guest:guest@localhost:5672// flower`. It offers real-time events monitoring, remote control, an HTTP API and OpenID auth, and Prometheus/Grafana integration is done through Flower (see its docs). `celery events` is a curses monitor started as a proof of concept; prefer Flower.

RabbitMQ: `rabbitmqctl list_queues name messages messages_ready messages_unacknowledged` (unacknowledged means received by a worker but in progress or reserved), `rabbitmqctl list_queues name consumers`, `rabbitmqctl list_queues name memory`. Add `-q` for parsable output and `-p my_vhost` for a custom virtual host.

Redis: `redis-cli -h HOST -p PORT -n DATABASE_NUMBER llen QUEUE_NAME` (default queue `celery`); list queues with `keys \*`. A missing key means an empty queue (empty lists are removed). Use a dedicated database number for Celery, but Flower events use pub/sub, which is global rather than per database.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/monitoring.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
