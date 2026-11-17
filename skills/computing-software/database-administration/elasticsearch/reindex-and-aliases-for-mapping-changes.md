---
id: computing-software.database-administration.elasticsearch.reindex-and-aliases-for-mapping-changes
name: reindex-and-aliases-for-mapping-changes
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, elasticsearch-operations, reindex-api, index-alias, mapping-change, zero-downtime, slices]
level: practitioner
status: verified
description: "Change an Elasticsearch field mapping without downtime: create a new index, reindex with slices and throttling, catch up writes, then swap an alias atomically."
sources:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/aliases.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reindex and aliases for zero-downtime mapping changes

You cannot change the type or analyzer of an existing field. Create a new index with the right
mapping and move the data. Applications must address an **alias**, never the concrete index.

## Setup (do this from day one)
```
PUT products_v1 { "mappings": { ... } }
POST _aliases { "actions": [ { "add": { "index": "products_v1", "alias": "products", "is_write_index": true } } ] }
```

## Migration
1. Create the new index, tuned for bulk load:
   ```
   PUT products_v2
   { "settings": { "number_of_replicas": 0, "refresh_interval": "-1" }, "mappings": { ... new ... } }
   ```
2. Reindex as a background task:
   ```
   POST _reindex?wait_for_completion=false&slices=auto&requests_per_second=5000
   { "source": { "index": "products_v1", "size": 1000 },
     "dest":   { "index": "products_v2", "op_type": "index" },
     "conflicts": "proceed" }
   ```
   Returns a task id. `slices=auto` parallelizes by shard; `requests_per_second` throttles
   (change live with `POST _reindex/<task>/_rethrottle?requests_per_second=10000`).
   Use `"script"` or an ingest `pipeline` in `dest` to transform documents.
3. Monitor: `GET _tasks/<task_id>`; cancel with `POST _tasks/<task_id>/_cancel`.
4. Catch up writes made during the copy: reindex again with a query on an `updated_at` field
   (`"query": { "range": { "updated_at": { "gte": "<start time>" } } }`), or dual-write from the
   application during the migration window.
5. Restore settings: `PUT products_v2/_settings { "number_of_replicas": 1, "refresh_interval": "1s" }`
   and wait for green.
6. Atomic swap:
   ```
   POST _aliases { "actions": [
     { "remove": { "index": "products_v1", "alias": "products" } },
     { "add":    { "index": "products_v2", "alias": "products", "is_write_index": true } } ] }
   ```
7. Keep v1 until verified, then delete it.

## Remote reindex
`"source": { "remote": { "host": "https://old:9200", "username": "...", "password": "..." }, "index": "x" }`
requires `reindex.remote.whitelist` on the destination (without it: `[localhost:19200] not whitelisted in reindex.remote.whitelist`).

## Gotchas
- Deletes made in v1 during the copy are not replicated by a catch-up reindex: dual-write or
  short write freeze for exactness.
- Reindex does not copy settings, mappings or aliases; define them on the destination first.
- Large reindexes compete with production: throttle, run off-peak.

## Verify
`GET _cat/count/products_v1` and `products_v2` match (after catch-up), sample queries return
the same results, and `GET _alias/products` points only to v2.
