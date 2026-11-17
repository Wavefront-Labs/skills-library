---
id: computing-software.messaging-and-integration.celery.celery-first-steps-setup
name: celery-first-steps-setup
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-first-steps, broker, rabbitmq, redis, result-backend, worker, troubleshooting]
level: intro
status: docs-checked
description: "Get Celery running: choose a broker, create tasks.py, start the worker, call a task, enable a result backend, use celeryconfig, and fix PENDING or worker-start problems."
sources:
  - https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html
  - https://docs.celeryq.dev/en/stable/getting-started/introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: a working Celery app with a worker and retrievable results.

## Broker
RabbitMQ is feature-complete, stable and durable (`sudo apt-get install rabbitmq-server` or `docker run -d -p 5672:5672 rabbitmq`). Redis is also feature-complete but more susceptible to data loss on abrupt termination (`docker run -d -p 6379:6379 redis`). Amazon SQS and others are experimental. `pip install -U Celery`.

## App and worker
`tasks.py`:
```python
from celery import Celery
app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y
```
First argument is the module name (for names generated in `__main__`). Broker URLs: `amqp://localhost` or `redis://localhost`. Run the worker: `celery -A tasks worker --loglevel=INFO`. In production daemonize via your platform or supervisord. Help: `celery worker --help`, `celery --help`.

## Call and keep results
`add.delay(4, 4)` returns an `AsyncResult`. Results are off by default; set a backend:
```python
app = Celery('tasks', backend='rpc://', broker='pyamqp://')
# or backend='redis://localhost'
```
Restart the worker and reimport. Then `result = add.delay(4, 4)`, `result.ready()` (False until done), `result.get(timeout=1)` (8; blocks, rarely used), `result.get(propagate=False)`, `result.traceback`. You must call `get()` or `forget()` on every `AsyncResult`.

## Config module
`app.config_from_object('celeryconfig')` with `celeryconfig.py` containing `broker_url = 'pyamqp://'`, `result_backend = 'rpc://'`, `task_serializer = 'json'`, `result_serializer = 'json'`, `accept_content = ['json']`, `timezone = 'Europe/Oslo'`, `enable_utc = True`. Check it has no syntax errors by importing it: `python -m celeryconfig`. Route a task: `task_routes = {'tasks.add': 'low-priority'}`; rate limit: `task_annotations = {'tasks.add': {'rate_limit': '10/m'}}`, or at runtime `celery -A tasks control rate_limit tasks.add 10/m` (RabbitMQ or Redis).

## Troubleshooting
- Worker will not start (Permission Error): on Debian-based systems `ln -s /run/shm /dev/shm`; otherwise `--pidfile`, `--logfile`, `--statedb` must be writable by the user.
- Always PENDING (the state really means unknown): check the task and `task_ignore_result` are not ignoring results, no old worker is still running (set an absolute `--pidfile`), and the client's backend matches (`print(result.backend)`).

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (getting-started/first-steps-with-celery.html, getting-started/introduction.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Removed or reworded: the Python-version, PyPy and Windows support sentence (not on the cited pages).

Method: documentation only; no commands were run.
