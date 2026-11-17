---
id: computing-software.database-administration.memcached.tune-extstore-for-loki
name: tune-extstore-for-loki
category: computing-software
field: database-administration
product: memcached
tags: [loki, grafana, extstore, ext-threads, chunk-cache]
level: advanced
status: docs-checked
description: "Pair Grafana Loki with extstore: -I 2m, ext_threads=10, ext_wbuf_size=32 and conservative Loki batch, timeout and writeback settings."
sources:
  - https://docs.memcached.org/advisories/grafanaloki/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Assumes Loki chunks of 1.5 MB and memcached 1.6.21+ (better extstore write speed).

Memcached:
```
memcached -m 6000 -I 2m -o ext_path=/path/to/extstore:500G,ext_wbuf_size=32,ext_threads=10,ext_max_sleep=10000,slab_automove_freeratio=0.10,ext_recache_rate=0
```
Most gain is from `ext_threads` (fully uses an SSD); fast SSDs may take 20-30. `-t` defaults to 4; do not exceed CPU count. Set `-m` and the path size for your host, leaving RAM and disk headroom.

Loki:
```
chunk_cache_config:
  memcached: {batch_size: 3, parallelism: 2}
  memcached_client: {addresses: 127.0.0.1:11211, timeout: 60s}
  background: {writeback_goroutines: 1, writeback_buffer: 1000, writeback_size_limit: 500MB}
```
Why: Loki defaults assume RAM-backed clusters of many nodes. `batch_size` can be 2x the server count; the timeout covers a whole batch fetched from SSD; writeback_goroutines defaults to 10 and floods memcached, raising `evictions` if flash cannot keep up.

Check no swapping or CPU exhaustion.

## Checked

2026-11-04. Confirmed against the Loki with Extstore advisory (flags, Loki config, rationale, 1.6.21 note). Removed: nothing.

Method: documentation only; no commands were run.
