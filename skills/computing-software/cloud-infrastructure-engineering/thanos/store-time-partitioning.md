---
id: computing-software.cloud-infrastructure-engineering.thanos.store-time-partitioning
name: store-time-partitioning
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-store, time-partitioning, min-time, max-time]
level: practitioner
status: docs-checked
description: "Shard Store Gateways by time range with --min-time and --max-time, with the caveats about sync delay and chunk-level filtering."
sources: ["https://thanos.io/tip/components/store.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Store time-based partitioning

By default a Store Gateway serves everything in the bucket that matches a query's time range. `--min-time` and `--max-time` shard it by time instead.

```
thanos store --min-time=-6w --max-time=-2w ...
```

This serves data from now minus 6 weeks up to now minus 2 weeks. Values can be constant RFC3339 times (`--min-time=2018-01-01T00:00:00Z`) or durations relative to now; valid units are `ms, s, m, h, d, w, y`. Defaults are `0000-01-01T00:00:00Z` and `9999-12-31T23:59:59Z`.

**Caveats from the docs**
- Partitioning happens partly in the asynchronous block sync job (`--sync-block-duration`, default 15m in the flag list), so new blocks may not appear immediately. Some object stores are also only eventually consistent for read-after-write.
- Filtering is done at chunk level, so a store may still return samples outside the configured range.
- Overlapping ranges with the sidecar and other stores are recommended for resilience; the Querier merges overlapping series.

For sharding by external labels rather than time, use `--selector.relabel-config`.

## Checked

2026-11-03. Confirmed against the Thanos Store page (components/store.md): disk sizing (6 MB, 30MB), probes, index cache types and config, memcached and redis options, circuit breaker, caching bucket options, groupcache (v0.25, /_groupcache warning), hedging defaults, request limits and deprecations, time partitioning. Removed the claim about raw Prometheus blocks in the data dir. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
