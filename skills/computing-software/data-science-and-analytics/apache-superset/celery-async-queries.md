---
id: computing-software.data-science-and-analytics.apache-superset.celery-async-queries
name: celery-async-queries
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [celery, async-queries, workers, beat, flower]
level: practitioner
status: docs-checked
description: "Run Superset async queries with Celery: CELERY_CONFIG, worker, beat and flower commands, RESULTS_BACKEND, one-beat rule and SQL Lab async toggle."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/async-queries-celery.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run long queries outside web requests.

Queries that run beyond a typical web request timeout (30-60 seconds) need an async backend: one or more Celery workers, a broker (Redis or RabbitMQ recommended) and a results backend where workers persist results. Define `CELERY_CONFIG` in `superset_config.py`; worker and web server processes must have the same configuration.

```python
class CeleryConfig(object):
    broker_url = "redis://localhost:6379/0"
    imports = ("superset.sql_lab", "superset.tasks.scheduler")
    result_backend = "redis://localhost:6379/0"
    worker_prefetch_multiplier = 10
    task_acks_late = True
    task_annotations = {"sql_lab.get_sql_results": {"rate_limit": "100/s"}}

CELERY_CONFIG = CeleryConfig
```

Commands:

```bash
celery --app=superset.tasks.celery_app:app worker --pool=prefork -O fair -c 4
celery --app=superset.tasks.celery_app:app beat
celery --app=superset.tasks.celery_app:app flower
```

Beat schedules periodic background jobs. Flower is a web tool for monitoring the cluster (`pip install flower`).

Results backend: set `RESULTS_BACKEND` to an instance of a `BaseCache` derivative, for example `RedisCache(host='localhost', port=6379, key_prefix='superset_results')` from `flask_caching.backends.rediscache`. Memcached, Redis, S3, MinIO, memory or the file system (single server or testing) are options, and each needs its Python library (redis-py, pylibmc, s3werkzeugcache, minio-flask-cache). Results serialization uses MessagePack and PyArrow; disable with `RESULTS_BACKEND_USE_MSGPACK = False` if issues arise, and clear the results cache when upgrading.

Rules:
- All workers and web servers must share one metadata database; SQLite will not work.
- Run only one Celery beat in the whole setup; otherwise jobs schedule multiple times (duplicate report delivery, extra load).
- SQL Lab runs asynchronously only if Asynchronous Query Execution is enabled in the database settings (Sources > Databases > Edit record).
- With Global Async Queries for charts, a failed, aborted or timed-out chart query shows its task failure message in the chart error panel; embedded guest viewers get the same redacted message, or a generic one if no detail exists.

## Checked

2026-11-08: read async-queries-celery.mdx in full. Added RESULTS_BACKEND details from the page.
Method: documentation only; no commands were run.
