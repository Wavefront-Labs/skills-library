---
id: computing-software.data-science-and-analytics.apache-superset.sql-lab-results-backend
name: sql-lab-results-backend
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [results-backend, sql-lab, s3cache, msgpack, redis]
level: practitioner
status: docs-checked
description: "Configure RESULTS_BACKEND for Superset SQL Lab async results with S3 or Redis, MessagePack serialization and required cache libraries."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/async-queries-celery.mdx
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/cache.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: store async SQL Lab results where web servers can read them.

`RESULTS_BACKEND` must be an instance of a `BaseCache` derivative (from `flask_caching.backends.base`), not a Flask-Caching config dict. It applies when async queries are enabled; the page lists Memcached, Redis, S3, MinIO, memory (single server or testing) and the file system as options.

```python
# On S3
from s3cache.s3cache import S3Cache
S3_CACHE_BUCKET = 'foobar-superset'
S3_CACHE_KEY_PREFIX = 'sql_lab_result'
RESULTS_BACKEND = S3Cache(S3_CACHE_BUCKET, S3_CACHE_KEY_PREFIX)

# On Redis
from flask_caching.backends.rediscache import RedisCache
RESULTS_BACKEND = RedisCache(
    host='localhost', port=6379, key_prefix='superset_results')
```

Serialization uses MessagePack and PyArrow. Disable with `RESULTS_BACKEND_USE_MSGPACK = False`. Clear the existing results cache when upgrading.

Libraries to pip install per backend: `redis-py` (Redis), `pylibmc` (Memcached), `s3werkzeugcache` (S3), `minio-flask-cache` (MinIO or S3-compatible).

Related: SQL Lab only runs queries asynchronously when **Asynchronous Query Execution** is enabled on the database, and workers and web servers must share the same metadata database.

## Checked

2026-11-08. Confirmed against the Async Queries via Celery page. Corrected: RESULTS_BACKEND is a BaseCache derivative from flask_caching.backends.base, not a Flask-Caching config dict; listed the supported backends.
Method: documentation only; no commands were run.
