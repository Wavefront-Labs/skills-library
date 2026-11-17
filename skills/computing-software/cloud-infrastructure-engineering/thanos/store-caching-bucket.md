---
id: computing-software.cloud-infrastructure-engineering.thanos.store-caching-bucket
name: store-caching-bucket
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-store, caching-bucket, chunk-cache, metadata-cache]
level: advanced
status: docs-checked
description: "Cache chunks and block metadata in front of object storage with the Thanos Store caching bucket."
sources: ["https://thanos.io/tip/components/store.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Store caching bucket

A caching bucket caches chunks and metadata to speed up loading from TSDB blocks. Configure it with `--store.caching-bucket.config=<yaml>` or `--store.caching-bucket.config-file=<file>`. Backends are memcached, in-memory and redis (plus an experimental groupcache).

```yaml
type: MEMCACHED   # case-insensitive
config:
  addresses: ["dnssrvnoa+memcached.monitoring.svc:11211"]
  timeout: 500ms
  max_item_size: 1MiB
chunk_subrange_size: 16000
max_chunks_get_range_requests: 3
chunk_object_attrs_ttl: 24h
chunk_subrange_ttl: 24h
blocks_iter_ttl: 5m
metafile_exists_ttl: 2h
metafile_doesnt_exist_ttl: 15m
metafile_content_ttl: 24h
metafile_max_size: 1MiB
```

**Chunk options.** `chunk_subrange_size` is the smallest cached unit of a chunk file; `max_chunks_get_range_requests` limits "get range" sub-requests used to fetch missing subranges; `chunk_object_attrs_ttl` and `chunk_subrange_ttl` set lifetimes.

**Metadata options** (meta.json, deletion marks, iteration results): `blocks_iter_ttl`, `metafile_exists_ttl`, `metafile_doesnt_exist_ttl`, `metafile_content_ttl`, and `metafile_max_size` (larger files are not cached).

## Checked

2026-11-03. Confirmed against the Thanos Store page (components/store.md): disk sizing (6 MB, 30MB), probes, index cache types and config, memcached and redis options, circuit breaker, caching bucket options, groupcache (v0.25, /_groupcache warning), hedging defaults, request limits and deprecations, time partitioning. Removed the claim about raw Prometheus blocks in the data dir. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
