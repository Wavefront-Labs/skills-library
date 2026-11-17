---
id: computing-software.messaging-and-integration.celery.celery-other-result-backends
name: celery-other-result-backends
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-other-backends, celery, memcached, mongodb, couchbase, arangodb, couchdb, elasticsearch, filesystem, consul]
level: practitioner
status: docs-checked
description: "Configure Celery result backends for Memcached cache, MongoDB, Couchbase, ArangoDB, CouchDB, Elasticsearch, CosmosDB, file-system and Consul."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Memcached, MongoDB, Couchbase, ArangoDB, CouchDB, Elasticsearch, CosmosDB, filesystem, Consul

Goal: find the exact URL and settings for a less common result backend.

## Cache (Memcached) - 5.7 uses pymemcache only
`pip install celery[memcache]` (or `celery[pymemcache]`). `pylibmc` and `python-memcached` are no longer used; the `pylibmc://` scheme is still an alias of `memcache://`.
```python
result_backend = 'cache+memcached://127.0.0.1:11211/'
result_backend = 'cache+memcached://172.19.26.240:11211;172.19.26.242:11211/'
result_backend = 'cache'; cache_backend = 'memory'   # in-memory only
```
`cache_backend_options` (`{}`) go to pymemcache; `behaviors` and `binary` are ignored with a deprecation warning. Celery defaults `default_noreply=False` (failed writes raise; `True` hides them) and `connect_timeout`/`timeout` 5.0 s (`None` waits forever). Retries: `retry_attempts`, `retry_delay`, `retry_for`, `do_not_retry_for`. Several servers use `HashClient`, so keys may be distributed differently than with pylibmc.

## MongoDB
`mongodb_backend_settings` keys: `database` (default `celery`), `taskmeta_collection` (`celery_taskmeta`), `max_pool_size` (10), `options`. Example: `result_backend = 'mongodb://localhost:27017/'`. With pymongo>=4.14 options are case-sensitive.

## Couchbase / ArangoDB / CouchDB
- `couchbase://username:password@host:port/bucket`; `couchbase_backend_settings` keys `host` (localhost), `port` (8091), `bucket` (default), `username`, `password`.
- `arangodb://username:password@host:port/database/collection`; `arangodb_backend_settings` keys include `host`, `port` (8529), `database` and `collection` (both `celery`), `http_protocol` (`http`), `verify` (`False`).
- `couchdb://username:password@host:port/container` (needs `celery[couchdb]`).

## Elasticsearch
`elasticsearch://example.com:9200/index_name/doc_type`; `elasticsearch_retry_on_timeout` (False), `elasticsearch_max_retries` (3), `elasticsearch_timeout` (10.0), `elasticsearch_save_meta_as_text` (True).

## CosmosDB (experimental)
`cosmosdbsql://:{key}@{account}.documents.azure.com`; `cosmosdbsql_database_name` (celerydb), `cosmosdbsql_collection_name` (celerycol), `cosmosdbsql_consistency_level` (Session), `cosmosdbsql_max_retry_attempts` (9), `cosmosdbsql_max_retry_wait_time` (30).

## File-system and Consul
`result_backend = 'file:///var/celery/results'`: the directory must be shared and writable by all servers (NFS, GlusterFS, CIFS...). `consul://host:port[?one_client=1]` (`python-consul2`): `one_client` avoids HTTP 429 but makes storage unreliable.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/configuration.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
