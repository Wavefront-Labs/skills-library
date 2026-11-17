---
id: computing-software.messaging-and-integration.celery.celery-redis-result-backend
name: celery-redis-result-backend
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-redis-backend, celery, redis, result-backend, rediss, tls, socket-timeout, health-check]
level: practitioner
status: docs-checked
description: "Configure the Celery Redis result backend: URL forms, TLS, credential provider, connection limits, timeouts and health checks."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Redis result backend

Goal: point `result_backend` at Redis and tune connection behavior. Requires `pip install celery[redis]`.

## URL forms
```python
result_backend = 'redis://username:password@host:port/db'
result_backend = 'redis://localhost/0'   # same as 'redis://'
result_backend = 'redis://:password@host:port/db'   # no username (older Redis/py-redis)
result_backend = 'socket:///path/to/redis.sock'
result_backend = 'rediss://username:password@host:port/db?ssl_cert_reqs=required'
```
Username needs Redis>=6.0 and py-redis>=3.4.0 (5.1.0+). Port default 6379; db default 0 (leading slash optional).

## TLS
With `rediss://`, you may pass all `broker_use_ssl` keys as query parameters; `ssl_cert_reqs` is required and certificate paths must be URL encoded (`ssl_ca_certs=%2Fvar%2Fssl%2Fmyca.pem`). `ssl_cert_reqs` is `required`, `optional` or `none` (`CERT_REQUIRED`, `CERT_OPTIONAL`, `CERT_NONE` are accepted for backwards compatibility, but only work for Celery, not Redis directly). Alternatively set `redis_backend_use_ssl` to a dict with the same keys as the `redis` section of `broker_use_ssl`.

## Settings
- `redis_backend_health_check_interval` (not configured): integer seconds between health checks; on ConnectionError or TimeoutError the connection is re-established and the command retried exactly once.
- `redis_backend_credential_provider` (disabled): class path string such as `mymodule.myfile.myclass`, or a class instance.
- `redis_max_connections` (no limit): pool size for results; Redis raises `ConnectionError` if concurrent connections exceed it.
- `redis_socket_connect_timeout` (4.0.1+, `None`) and `redis_socket_timeout` (default 120.0 s).
- `redis_retry_on_timeout` (4.4.1+, `False`): retry on TimeoutError; do not set when using a unix socket.
- `redis_socket_keepalive` (4.4.1+, `False`).
- `redis_client_name` (5.6+, `None`): shows in Redis monitoring tools.
- `result_failure_expires` and `result_chord_expires` work with Redis.
- `result_compression` is ignored (with a warning) when Redis uses `decode_responses=True`.

## Checked

2026-11-07. Re-read the cited page(s) (configuration) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Changed: removed version tags on the health check interval and credential provider settings, which the page does not state unambiguously.

Method: documentation only; no commands were run.
