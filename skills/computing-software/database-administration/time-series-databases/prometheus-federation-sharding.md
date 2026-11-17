---
id: computing-software.database-administration.time-series-databases.prometheus-federation-sharding
name: prometheus-federation-sharding
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-ha, prometheus-federation-sharding, prometheus]
level: practitioner
status: docs-checked
description: "Scale Prometheus horizontally by sharding scrape with hashmod relabeling or federating selected series with honor_labels."
sources:
  - https://prometheus.io/docs/prometheus/latest/federation/
  - https://prometheus.io/docs/prometheus/latest/configuration/configuration/
  - https://prometheus.io/docs/prometheus/latest/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Federation and sharding

**Goal:** Scale Prometheus horizontally by sharding scrape or federating selected series.

## Steps
- Hierarchical federation: per-datacenter servers collect detailed data and global servers scrape and store only aggregated (job-level) series from them.
- Hash sharding for one huge job: the `hashmod` relabel action sets `target_label` to the modulus of a hash of the concatenated `source_labels`; give `modulus` the shard count, then `keep` only the targets whose hash matches this shard.
  ```
  relabel_configs:
    - source_labels: [__address__]
      modulus: 4
      target_label: __tmp_hash
      action: hashmod
    - source_labels: [__tmp_hash]
      regex: "0"
      action: keep
  ```
- Federation: the global server scrapes `/federate` on each leaf server with at least one `match[]` parameter, and sets `honor_labels: true` so labels exposed by the source are not overwritten:
  ```
  scrape_configs:
    - job_name: federate
      honor_labels: true
      metrics_path: /federate
      params:
        "match[]":
          - '{__name__=~"job:.*"}'
      static_configs:
        - targets: ["source-prometheus-1:9090"]
  ```
- Select aggregated recording-rule series (names like `job:...`) rather than raw series.
- Local storage is not clustered or replicated; for a durable global view the storage docs point to remote read/write integrations.

**Gotcha:** Each `match[]` must be an instant vector selector; if several are given, the union is returned, so a broad selector pulls in every matching raw series.

## Verify
- Each shard scrapes a roughly equal share of targets (Status > Targets).
- The global server holds only the aggregated series you selected.

## Checked
2026-11-03. Confirmed against the Prometheus federation page (/federate, match[], honor_labels, hierarchical use, example config), the configuration reference (hashmod action, modulus field, keep) and the storage page (local storage not clustered). Removed: the Prometheus Operator `shards:` claim, "doubles storage", and the unsupported mention of Mimir/Thanos for global views.
Method: documentation only; no commands were run.
