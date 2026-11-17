---
id: computing-software.messaging-and-integration.celery.celery-publish-retry-and-connection-errors
name: celery-publish-retry-and-connection-errors
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-calling, publish-retry, retry-policy, operational-error, confirm-publish, connection-pool, kombu]
level: advanced
status: docs-checked
description: "Configure Celery message-sending retries with retry_policy, handle kombu OperationalError when the broker is down, and detect silently dropped RabbitMQ messages."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/calling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control what happens when publishing a task message fails.

## Retry sending
Celery retries sending after connection failure. Disable per call:
```python
add.apply_async((2, 2), retry=False)
```
Related settings: `task_publish_retry`, `task_publish_retry_policy`.

## Retry policy keys
Passed through to `kombu.Connection.ensure`:
- `max_retries`: default 3; `None` retries forever.
- `interval_start`: seconds before the first retry; default 0 (instant).
- `interval_step`: added to the delay on each retry; default 0.2.
- `interval_max`: maximum wait between retries; default 1.
- `retry_errors` (5.3): tuple of exception classes to retry; default None (ignored).

The default is equivalent to:
```python
add.apply_async((2, 2), retry=True, retry_policy={
    'max_retries': 3, 'interval_start': 0,
    'interval_step': 0.2, 'interval_max': 1, 'retry_errors': None})
```
Total retry time is at most 0.6 seconds; it is short deliberately, because a long wait with the broker down can pile up web server processes and block incoming requests. Example retrying only timeouts: `retry_policy={'max_retries': 3, 'retry_errors': (kombu.exceptions.TimeoutError,)}`.

Workers also retry when a broker refuses a link, chain step or chord-body publish, per message, using `task_publish_retry`/`task_publish_retry_policy` or the callback signature's `retry`/`retry_policy`. The pool slot (or the whole solo worker) stays busy until the policy gives up or the broker accepts. After exhaustion the task fails through normal failure and errback handling. Since 5.7 an unbounded `max_retries` uses the app's finite limit or three retries, and `apply()` returns a `FAILURE` result instead of raising.

## Connection errors
If the connection is lost or cannot start, `kombu.exceptions.OperationalError` is raised (after retries are exhausted, or immediately when disabled). Handle it:
```python
try:
    add.delay(2, 2)
except add.OperationalError as exc:
    logger.exception('Sending task raised: %r', exc)
```
With RabbitMQ this only means the broker is unreachable; messages can still be silently dropped when it hits resource limits. Enable `confirm_publish` in `broker_transport_options` to detect that.

## Connection reuse
Handle the connection manually by creating a publisher: `with add.app.pool.acquire(block=True) as connection: with add.get_publisher(connection) as publisher: add.apply_async((i, j), publisher=publisher)`. For batches a `group(add.s(i, j) for i, j in numbers).apply_async()` is better.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/calling.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Removed or reworded: the claim that connection pools are automatic since 2.5 and the broker_pool_limit pointer.

Method: documentation only; no commands were run.
