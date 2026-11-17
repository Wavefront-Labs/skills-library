---
id: computing-software.cloud-infrastructure-engineering.thanos.store-gateway-overview
name: store-gateway-overview
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-store, store-gateway, storeapi, object-storage]
level: intro
status: docs-checked
description: "What thanos store does, what it keeps on local disk, and the per-block disk estimate."
sources: ["https://thanos.io/tip/components/store.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Store Gateway overview

`thanos store` (the Store Gateway) implements the Store API on top of historical data in an object storage bucket. It acts as an API gateway, joins a Thanos cluster on startup and advertises the data it can access, so it needs little local disk.

```
thanos store \
  --data-dir "/path/to/store/data" \
  --objstore.config-file "bucket.yml"
```

**Local state.** It keeps a small amount of information about every remote block on local disk and keeps it in sync with the bucket. This data is generally safe to delete across restarts, at the cost of a longer startup.

**Disk sizing.** Plan on an average of 6 MB of local disk per TSDB block in the bucket; high-cardinality blocks with large label sets can reach 30 MB or more. That space holds the pre-computed index (symbols, postings offsets) and metadata JSON.

**Defaults worth knowing.** `--data-dir` defaults to `./data`; HTTP listens on `0.0.0.0:10902` and gRPC (StoreAPI) on `0.0.0.0:10901`.

## Checked

2026-11-03. Confirmed against the Thanos Store page (components/store.md): disk sizing (6 MB, 30MB), probes, index cache types and config, memcached and redis options, circuit breaker, caching bucket options, groupcache (v0.25, /_groupcache warning), hedging defaults, request limits and deprecations, time partitioning. Removed the claim about raw Prometheus blocks in the data dir. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
