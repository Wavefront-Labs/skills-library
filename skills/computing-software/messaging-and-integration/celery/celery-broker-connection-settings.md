---
id: computing-software.messaging-and-integration.celery.celery-broker-connection-settings
name: celery-broker-connection-settings
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-broker, celery, broker-url, failover, heartbeat, ssl, connection-pool, retry, transport-options]
level: practitioner
status: docs-checked
description: "Set Celery broker_url, failover, heartbeat, SSL, connection pool and retry settings with exact defaults and gotchas."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
  - https://docs.celeryq.dev/en/stable/userguide/optimizing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Broker connection settings

Goal: configure how Celery connects, fails over and retries.

## URL
`broker_url` default `"amqp://"`, form `transport://userid:password@hostname:port/virtual_host`; only the scheme is required. Transports: `amqp` (librabbitmq if installed, else pyamqp), `redis://`, `sqs://`, `qpid://`, or a full class path. Multiple URLs of the same transport as a `;`-delimited string or list feed `broker_failover_strategy` (default `"round-robin"`, or a generator function). `broker_read_url` / `broker_write_url` default to `broker_url` and split consuming from producing.

## Heartbeat
`broker_heartbeat` (pyamqp, default 120.0 negotiated by server): used only by the worker; clients do not heartbeat. `broker_heartbeat_checkrate` (default 3.0): checked at heartbeat/rate (10 s gives about every 3.33 s).

## SSL (`broker_use_ssl`, pyamqp and redis; default disabled)
- pyamqp: `True` for defaults or a dict of `ssl.wrap_socket` options, e.g. `{'keyfile': ..., 'certfile': ..., 'ca_certs': ..., 'cert_reqs': ssl.CERT_REQUIRED}`. From 5.1, py-amqp always validates server certificates; `ssl.CERT_NONE` is insecure. The SSL port is usually separate.
- redis: dict with required `ssl_cert_reqs` (`ssl.CERT_NONE`, `CERT_OPTIONAL`, `CERT_REQUIRED`), optional `ssl_ca_certs`, `ssl_certfile`, `ssl_keyfile`.

## Pool and timeouts
- `broker_pool_limit` (default 10): connections in pool; `None` or 0 disables pooling (connect/close per use). Raise it for e.g. eventlet with 1000 greenlets.
- `broker_pool_acquire_timeout` (5.7+, `None` = block forever): seconds `send_task`/`apply_async` wait for a pooled connection before `OperationalError`.
- `broker_connection_timeout` (4.0 s): worker connect only, disabled with gevent; does not apply to producers, use `broker_transport_options`.

## Retry
- `broker_connection_retry` (enabled): reconnect after loss; backoff grows until `broker_connection_max_retries` (default 100; `None` retries forever). From Celery 6.0 it no longer governs startup.
- `broker_connection_retry_on_startup` (default `None`, falls back to `broker_connection_retry`).
- `broker_channel_error_retry` (5.3+, disabled): reconnect on an invalid response; needs `broker_connection_retry`.
- `broker_login_method` default `"AMQPLAIN"`.
- `broker_native_delayed_delivery_queue_type` (5.5+, pyamqp) default `"quorum"`; `"classic"` also possible.

## broker_transport_options (default `{}`)
```python
broker_transport_options = {'visibility_timeout': 18000}  # 5 hours; Redis and SQS
broker_transport_options = {'max_retries': 5}            # producers do not retry forever
broker_transport_options = {'confirm_publish': True}     # pyamqp; otherwise messages can be silently dropped at broker limits
```
`task_publish_retry` (default enabled) and `task_publish_retry_policy` control retrying task publishing on connection errors. `result_backend_transport_options` is the result-side equivalent.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/configuration.html, userguide/optimizing.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
