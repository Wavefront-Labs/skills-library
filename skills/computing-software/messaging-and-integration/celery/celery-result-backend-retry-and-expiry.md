---
id: computing-software.messaging-and-integration.celery.celery-result-backend-retry-and-expiry
name: celery-result-backend-retry-and-expiry
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-result-backend, celery, result-backend, result-expires, backend-retry, tombstones, transport-options, result-extended]
level: practitioner
status: docs-checked
description: "Pick a Celery result_backend and tune retries, result_expires, failure expiry, caching and extended results with exact defaults."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# result_backend choice, retries and expiry

Goal: select a backend and set how results are retried, cached and expired.

## Choosing result_backend (default: none enabled)
Names accepted: `rpc` (results as AMQP messages), `database` (SQLAlchemy), `redis`, `cache` (Memcached), `mongodb`, `cassandra`, `elasticsearch`, `ironcache`, `couchbase`, `arangodb`, `couchdb`, `cosmosdbsql (experimental)`, `filesystem`, `consul`, `azureblockblob`, `s3`, `gcs`. `override_backends` maps a name to a class path, e.g. `{"db": "custom_module.backend.class"}`, to store extra metadata or override retry policies.

## Retry settings
- `result_backend_always_retry` (default `False`): retry recoverable exceptions with exponential backoff instead of propagating. The database backend overrides this to `True` (since 5.7); `None` also gives `True`.
- `result_backend_max_retries` (default `Inf`): max retries; the database backend uses `3` (`None` also gives 3).
- `result_backend_base_sleep_between_retries_ms` (default 10) and `result_backend_max_sleep_between_retries_ms` (default 10000).
- `result_backend_thread_safe` (default `False`): share the backend object across threads, for a shared connection pool.
- `result_backend_transport_options` (default `{}`): passed to the transport, e.g. `{'visibility_timeout': 18000}  # 5 hours` (Redis and SQS).

## Expiry and caching
- `result_expires` (default 1 day): seconds or `timedelta`. A built-in periodic task `celery.backend_cleanup` deletes results, assuming `celery beat` is enabled; it runs daily at 4am. `None` or 0 means never expire (backend dependent). Works only with AMQP, database, cache, Couchbase, filesystem and Redis; with database or filesystem, beat must be running.
- `result_failure_expires` (5.7+, default same as `result_expires`): for `FAILURE` results only; `0` means never. Redis backend only.
- `result_cache_max` (disabled): client-side cache; 0 or `None` unlimited, `-1` disables. Useful for the old deprecated amqp backend, where a result is gone once consumed.
- `result_extended` (default `False`): writes name, args, kwargs, worker, retries, queue and stamps to the backend. With the database backend and `result_extended=True`, an existing `celery_taskmeta` table needs a `stamps` column (`ALTER TABLE celery_taskmeta ADD COLUMN stamps BLOB;`, `BYTEA` on PostgreSQL) or result writes fail.
- RPC backend: `result_persistent` (default disabled = transient). Too many old results can raise `celery.backends.rpc.BacklogLimitExceeded` when reading state.

## Checked

2026-11-07. Re-read the cited page(s) (configuration) against this skill: parameters, defaults, setting names, classes, methods and code samples were matched to the page text. The page is long; it was read in chunks and every section relevant to this skill was covered. Code snippet and include files were not opened separately.

Removed: nothing; every claim was confirmed.

Method: documentation only; no commands were run.
