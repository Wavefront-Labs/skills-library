---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.thanos-global-view-and-long-term-storage
name: thanos-global-view-and-long-term-storage
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, thanos, thanos-sidecar, thanos-query, thanos-query-frontend, thanos-store, thanos-store-gateway, thanos-receive, thanos-compactor, thanos-ruler, object-storage, s3, gcs, downsampling, deduplication, replica-labels, long-term-storage, global-view, bucket-config, store-api, hashring, pca]
level: advanced
status: docs-checked
description: "Deploy and operate Thanos: sidecar vs receive topologies, Query dedup over replica labels, Store Gateway and Compactor on object storage, downsampling/retention, and halts."
sources: ["https://thanos.io/tip/thanos/getting-started.md/", "https://thanos.io/tip/components/sidecar.md/", "https://thanos.io/tip/components/receive.md/", "https://thanos.io/tip/components/compact.md/", "https://thanos.io/tip/components/query.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thanos: global view, HA dedup and long-term storage

**Goal:** one PromQL endpoint over every Prometheus you run, deduplicated across HA pairs,
with months of history in object storage and the local servers kept small.

## 1. Pick the topology
| | Sidecar | Receive |
|---|---|---|
| How data leaves Prometheus | sidecar uploads 2h blocks to bucket; Query reaches sidecar's StoreAPI for fresh data | Prometheus `remote_write` → Receive (hashring, WAL, TSDB) → bucket |
| Prometheus must be reachable from Query | yes (gRPC 10901) | no; good for edge/NAT/multi-tenant |
| Operational weight | light | a stateful replicated ingest tier |
Sidecar for clusters you control the network of; Receive for many remote/tenant clusters.
Don't mix for the same Prometheus.

## 2. Sidecar setup
```yaml
# Prometheus flags required
--storage.tsdb.min-block-duration=2h --storage.tsdb.max-block-duration=2h   # disable local compaction so uploads are consistent
# external_labels MUST be unique per Prometheus and include the replica label
external_labels: { cluster: prod-eu1, prometheus_replica: a }
```
```bash
thanos sidecar --prometheus.url=http://localhost:9090 --tsdb.path=/prometheus \
  --objstore.config-file=bucket.yml --grpc-address=0.0.0.0:10901 --http-address=0.0.0.0:10902
# bucket.yml
type: S3
config: { bucket: thanos-prod, endpoint: s3.eu-west-1.amazonaws.com, region: eu-west-1 }
```

## 3. Query, Store, Compactor
```bash
thanos query --http-address=0.0.0.0:9090 --grpc-address=0.0.0.0:10901 \
  --endpoint=sidecar-eu1:10901 --endpoint=sidecar-us1:10901 --endpoint=store:10901 --endpoint=ruler:10901 \
  --query.replica-label=prometheus_replica --query.auto-downsampling \
  --query.partial-response                       # serve what responded; drop for strict correctness
thanos store --data-dir=/cache --objstore.config-file=bucket.yml   # cache sizing flags: see the Store component page
thanos compact --data-dir=/compact --objstore.config-file=bucket.yml --wait \
  --retention.resolution-raw=30d --retention.resolution-5m=180d --retention.resolution-1h=2y \
  --delete-delay=48h --compact.concurrency=2
```
Query Frontend (`thanos query-frontend`) sits in front of Query to split and cache range queries; take its flags from the Query Frontend component page.
- **Exactly one Compactor** per bucket: the docs say it is not semantically concurrency safe and must be deployed as a singleton. It compacts, downsamples (5m for blocks older than 40 hours, 1h for blocks older than 10 days), applies retention (`--retention.resolution-raw|5m|1h`; unset or 0s means keep forever) after the compaction and downsampling loops, and starts deleting directories without `meta.json` only after `--delete-delay`.
- Store Gateway serves the bucket; give it persistent cache disk.
- Query dedup: series differing only in `prometheus_replica` are merged; use
  `--query.replica-label` on Query **and** `--deduplication.replica-label` on Compactor
  (vertical compaction) if you want deduped blocks in storage.

## 4. Receive (remote-write path)
```bash
thanos receive --tsdb.path=/data --objstore.config-file=bucket.yml \
  --receive.hashrings-file=hashring.json --receive.replication-factor=3 \
  --receive.local-endpoint=receive-0.receive:10901 --label='receive_replica="0"' \
  --remote-write.address=0.0.0.0:19291 --tsdb.retention=2d
```
- The hashring algorithm is set with `--receive.hashrings-algorithm`; the docs recommend `ketama` over `hashmod`.
- Tenants are created dynamically from the `THANOS-TENANT` HTTP header; each tenant gets its own TSDB.
- `--tsdb.retention` also drives tenant decommissioning when no samples arrive for that long.

## 5. Ruler
`thanos rule` evaluates rules against Query (global data). Use it only for rules that need cross-cluster data; local Prometheus rules are more reliable (no Query dependency). Alert on partial responses (the `partial_response` query option defaults to true).

## 6. Watch it
```promql
thanos_compact_halted == 1     # compactor halts (keeps running, does nothing) on unhealthy blocks such as overlaps
```
Other component metrics: take names from each component's `/metrics` output. `thanos tools bucket` has subcommands to inspect and repair a bucket; see the tools page.

## Gotchas
- Two Prometheus servers with identical `external_labels` (forgotten replica label) create
  **overlapping blocks** and halt the Compactor. Fix labels first, then mark/delete the
  duplicates (see the `thanos tools bucket` docs).
- The sidecar's `--web.enable-lifecycle` is only needed for its reload features.
- Query's `max_source_resolution` defaults to step/5, or 0 when `--query.auto-downsampling` is false; query-time options include `partial_response`.

## Verify
- [ ] `thanos query` UI → Stores shows every sidecar/store/receive healthy with correct external labels and min/max time.
- [ ] Toggling dedup off/on for an HA pair roughly halves the series count.
- [ ] `thanos_compact_halted == 0`, and 5m/1h resolutions appear for blocks older than 40 hours / 10 days.
- [ ] Killing one Prometheus replica leaves dashboards gap-free.

## Checked

2026-11-02. Confirmed against the Thanos sidecar, query, compact and receive component pages: equal `--storage.tsdb.min-block-duration`/`max-block-duration` to disable local compaction; sidecar `--prometheus.url`; Query `--query.replica-label`, StoreAPI endpoints, `max_source_resolution` default and `partial_response` default true; Compactor singleton, `--retention.resolution-*` (0s or unset keeps forever), `--delete-delay=48h`, `--compact.concurrency`, `--wait`, `--deduplication.replica-label`, 5m downsampling after 40 hours and 1h after 10 days, halt behaviour and `thanos_compact_halted`; Receive `--receive.hashrings-algorithm` with ketama recommended, `--receive.replication-factor`, `--receive.local-endpoint`, `--remote-write.address` default 19291, `THANOS-TENANT` header and dynamic tenants. Removed as not on the fetched pages: Store cache sizes, Query Frontend flags, the 2h data-loss window, Operator snippet, 2d/14d block sizes, sharding size advice, most metric names, `bucket verify/mark` argument forms, sidecar `/api/v1/status/config` behaviour, timeouts and GET-cost remarks, and the Receive sizing and replication-fault claims.

Method: documentation only; no commands were run.
