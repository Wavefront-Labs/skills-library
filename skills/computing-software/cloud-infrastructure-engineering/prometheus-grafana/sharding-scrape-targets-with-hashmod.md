---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.sharding-scrape-targets-with-hashmod
name: sharding-scrape-targets-with-hashmod
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [hashmod-sharding, scrape-target-sharding, hashmod-action, relabel-configs, prometheus, horizontal-scaling]
level: advanced
status: verified
description: "Split scrape targets across N Prometheus servers with hashmod relabeling, then query them together via Thanos, Mimir or federation."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config", "https://prometheus-operator.dev/docs/api-reference/api/", "https://thanos.io/tip/components/query.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharding scrape targets with hashmod

When one Prometheus cannot hold all series, shard targets so each server scrapes 1/N of them.

## Config on shard k of N
```yaml
scrape_configs:
  - job_name: node
    kubernetes_sd_configs: [{role: node}]
    relabel_configs:
      - source_labels: [__address__]
        modulus: 4                # N
        target_label: __tmp_hash
        action: hashmod
      - source_labels: [__tmp_hash]
        regex: "2"                # k (0..N-1), templated per server
        action: keep
```
`__tmp_` labels are dropped after relabeling (the kept targets showed no `__tmp_hash` label). Every shard gets the same config except `regex`.
The hash is the low 8 bytes (big-endian) of the md5 of the joined source labels, modulo `modulus`: the six test addresses `localhost:18082`,
`127.0.0.1:18082` and four `localhost:18082?a=N` ones split 4/2 in Python, and the live server kept exactly the two the formula predicted.

## Prometheus Operator
`spec.shards: 4` on the Prometheus CR distributes scraped targets over that many shards; `spec.replicas` multiplied by `spec.shards` is the number of Pods (Prometheus Operator API reference; not run, no cluster). Per that reference, scaling shards does not move existing data.

## Querying across shards
- Query across shards with a layer that fans out (the Operator reference names Thanos or remote write to a central store).
- Add an external label `shard: "k"` for debugging, but never aggregate by it.

## Choosing the hash input
- `__address__` spreads by target; a single huge target stays on one shard.
- Rules needing series from several targets (e.g. `sum by (job)`) only see their shard: evaluate those on the global layer.

## Gotchas
- Changing N reshuffles most targets: 161 of 200 sample addresses (80 %) changed shard going from `modulus: 4` to `modulus: 5` (computed with the md5 rule). A target that moves shard starts a new series history there; the old history stays on the old shard's storage.
- Uneven target sizes give uneven shards; monitor `prometheus_tsdb_head_series` per shard.

## Verify
- [ ] `count(up)` summed over shards equals the unsharded target count; no target scraped twice (`count by (instance, job) (up) > 1` is empty at the global layer).

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), client_golang 1.25.0 on Go 1.26, Python 3.14.
- A static-target job with the skill's two relabel rules (`modulus: 2`, `regex: "0"`, `action: keep`) kept two of six targets; Python `int.from_bytes(md5(addr).digest()[8:], 'big') % 2` predicted the same two addresses. The same function over 200 sample node addresses: 46/54/54/46 per shard at modulus 4, and 161 of 200 changed shard at modulus 5.
- `__tmp_hash` absent from the kept targets' labels (`/api/v1/targets`). `hashmod` action semantics and `modulus`/`target_label` keys: 3.15 configuration page.
- Prometheus Operator: `shards` field description (replicas x shards Pods, no resharding of data) in its API reference; no cluster, so the CR itself was not applied. Removed the StatefulSet name and the Thanos/Mimir ruler statements that could not be confirmed.
