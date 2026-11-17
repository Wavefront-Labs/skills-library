---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.thanos-read-path-caching
name: thanos-read-path-caching
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [thanos, thanos-store, store-gateway-sharding, index-cache, bucket-cache, query-splitting, response-caching, query-frontend, memcached]
level: advanced
status: docs-checked
description: "Speed up Thanos long-range queries: store gateway time/hash sharding, index and bucket caches (memcached/redis), and query-frontend splitting with results caching."
sources: ["https://thanos.io/tip/components/store.md/", "https://thanos.io/tip/components/query-frontend.md/", "https://thanos.io/tip/thanos/sharding.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thanos read-path caching and sharding

## Store gateway
```bash
thanos store --objstore.config-file=objstore.yml --data-dir=/var/thanos/store \
  --index-cache.config-file=index-cache.yml \
  --store.caching-bucket.config-file=bucket-cache.yml \
  --min-time=-30d --max-time=-2h \
  --selector.relabel-config-file=shard.yml
```
`--min-time/--max-time` is a time-based shard (this replica serves 2 h..30 d ago); the selector file is a
hash-based shard over blocks.
```yaml
# index-cache.yml (postings and series; most valuable cache)
type: MEMCACHED
config: {addresses: [dnssrv+_client._tcp.memcached-index.thanos.svc], max_item_size: 5MiB, timeout: 2s}
# bucket-cache.yml (chunks, object metadata, iter results)
type: MEMCACHED
config: {addresses: [dnssrv+_client._tcp.memcached-bucket.thanos.svc]}
chunk_subrange_size: 16000
max_chunks_get_range_requests: 3
```
`shard.yml` (hashmod over `__block_id`, keep shard N) splits blocks across store replicas.
Default in-memory index cache (250 MB) is fine only for small buckets.

## Query frontend
```bash
thanos query-frontend --http-address=0.0.0.0:9090 \
  --query-frontend.downstream-url=http://thanos-query:9090 \
  --query-range.split-interval=24h \
  --query-range.align-range-with-step \
  --query-range.max-retries-per-request=3 \
  --query-range.response-cache-config-file=results-cache.yml \
  --query-frontend.compress-responses \
  --labels.split-interval=24h
```
Point Grafana at the frontend, not at Query.

## Measure
Compare query latency on the same dashboard before and after enabling each cache, and watch the cache hit and miss metrics each component exposes (list them from the component's `/metrics`).

## Gotchas
- Set `max_item_size` to the same value as memcached's `-I` flag (memcached defaults to 1MB), otherwise round trips are wasted storing items memcached will refuse.
- `--store.grpc.series-sample-limit` / `touched-series-limit` protect stores from runaway queries.

## Verify
- [ ] Repeat of a 30-day dashboard loads noticeably faster on second view.
- [ ] Store gateway memory stable and cache hits rising after warm-up.

## Checked
- 2026-10-28. Confirmed against the Thanos Store page (`--min-time`/`--max-time`, `--selector.relabel-config-file`, `--index-cache.config-file`, `--store.caching-bucket.config-file`, memcached `max_item_size`, `chunk_subrange_size`, `max_chunks_get_range_requests`, 250MB in-memory index cache default, `--store.grpc.series-sample-limit`, `--store.grpc.touched-series-limit`), the Query Frontend page (`--query-frontend.downstream-url`, `--query-range.split-interval`, `--query-range.max-retries-per-request`, `--labels.split-interval`) and the Sharding page (`hashmod` over `__block_id`).
- Removed: cache metric names, the 80 % and 5x thresholds, the cache-key explanation, the time-shard boundary remark, and the memcached `-I` direction (the docs say set them equal).
Method: documentation only; no commands were run.
