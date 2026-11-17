---
id: computing-software.cloud-infrastructure-engineering.thanos.store-request-limits
name: store-request-limits
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-store, store-limits, series-limit, samples-limit]
level: advanced
status: docs-checked
description: "Cap series, samples and downloaded bytes per request on Thanos Store to protect it from heavy queries."
sources: ["https://thanos.io/tip/components/store.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Store request limits

Thanos Store can reject expensive requests before they exhaust memory. All limits default to 0, meaning no limit.

- `--store.limits.request-series`: maximum series in a single Series request; the call fails if exceeded.
- `--store.limits.request-samples`: maximum samples in a single Series request. It is implemented internally as a chunks limit, with each chunk holding at most 120 samples.
- `--store.grpc.downloaded-bytes-limit`: maximum bytes downloaded (fetched or touched) in a single Series, LabelNames or LabelValues call.
- `--store.grpc.series-max-concurrency` (default 20): maximum concurrent Series calls.

`--store.grpc.touched-series-limit` and `--store.grpc.series-sample-limit` are deprecated in favour of the `--store.limits.*` flags.

Other tuning flags in the same list: `--block-sync-concurrency=20` (goroutines building index-cache from the bucket), `--block-meta-fetch-concurrency=32`, and `--block-discovery-strategy` (`concurrent`, the default, or `recursive`, which avoids N+1 listing calls but iterates more slowly).

## Checked

2026-11-03. Confirmed against the Thanos Store page (components/store.md): disk sizing (6 MB, 30MB), probes, index cache types and config, memcached and redis options, circuit breaker, caching bucket options, groupcache (v0.25, /_groupcache warning), hedging defaults, request limits and deprecations, time partitioning. Removed the claim about raw Prometheus blocks in the data dir. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
