---
id: computing-software.database-administration.time-series-databases.thanos-sidecar-store
name: thanos-sidecar-store
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-thanos, thanos-sidecar-store, prometheus, thanos]
level: practitioner
status: draft
description: "Add Thanos to existing Prometheus for global query and object-store retention."
sources:
  - https://thanos.io/tip/thanos/getting-started.md/
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://prometheus.io/docs/introduction/overview/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thanos sidecar and store gateway

**Goal:** Add Thanos to existing Prometheus for global query and object-store retention.

## Steps
- Run the sidecar next to each Prometheus: `thanos sidecar --tsdb.path /prometheus --prometheus.url http://localhost:9090 --objstore.config-file bucket.yml`.
- Prometheus needs `--storage.tsdb.min-block-duration=2h --storage.tsdb.max-block-duration=2h` and external labels (`external_labels: {cluster: a, replica: 0}`).
- Sidecar uploads finished 2h blocks to S3, GCS or Azure.
- Store Gateway serves blocks from the bucket: `thanos store --data-dir /var/thanos/store --objstore.config-file bucket.yml`.
- Querier federates sidecars and stores: `thanos query --store=sidecar:10901 --store=store:10901 --query.replica-label=replica`.
- Deduplicate HA pairs using `--query.replica-label`.

**Gotcha:** Missing or duplicated external labels cause blocks from different Prometheus servers to collide in the bucket.

## Verify
- `thanos tools bucket ls` lists uploaded blocks.
- A query spanning past local retention returns data via Querier.
