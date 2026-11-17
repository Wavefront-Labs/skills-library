---
id: computing-software.database-administration.couchdb.replicator-throughput-tuning
name: replicator-throughput-tuning
category: computing-software
field: database-administration
product: couchdb
tags: [replication, workers, checkpoints, compression, retries]
level: advanced
status: docs-checked
description: "Tune CouchDB replication workers, batch size, HTTP connections, timeouts, retries, gzip request compression and checkpoint settings."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/replicator.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In `[replicator]` (page example values):

- `worker_batch_size = 500`: lower values checkpoint more often and use less RAM.
- `worker_processes = 4`: more can raise network throughput but add disk and network I/O.
- `http_connections = 20`: per replication.
- `connection_timeout = 30000`: ms, divided by three for changes feed requests. Raise it if the remote database is busy.
- `retries_per_request = 5` (10 before 2.1.1): exponential backoff starting at 0.25 s (0.25, 0.5, 1, 2, 4). When exhausted the job stops and retries later.
- `request_compression` (3.6): `none` (default) or `gzip` for `_bulk_docs`, `_revs_diff`, `_bulk_get` bodies. Use only if the target accepts `Content-Encoding: gzip`. Per job via `"request_compression": "gzip"` in the replication document. `compress_min_size` (example 1024 bytes) sets the smallest body compressed.
- `checkpoint_interval = 5000` ms; `use_checkpoints = true`. Disabling is not recommended: the source changes feed is scanned from the beginning. Checkpoints are `_local` docs on source and target (write access needed).
- `use_bulk_get` (3.3): falls back to single GETs on error; disable to skip trying.

## Checked

2026-11-04. Confirmed against the CouchDB config/replicator page ([replicator] options): worker_batch_size, worker_processes, http_connections, connection_timeout divided by three, retries_per_request and backoff, request_compression and compress_min_size (3.6), checkpoint_interval, use_checkpoints warning and local docs note, use_bulk_get (3.3). Nothing removed.

Method: documentation only; no commands were run.
