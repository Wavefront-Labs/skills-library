---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.mimir-ha-tracker-deduplication
name: mimir-ha-tracker-deduplication
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [ha-tracker, mimir, ha-pairs, cluster-replica-labels, prometheus-ha, deduplication, memberlist]
level: practitioner
status: docs-checked
description: "Deduplicate samples from HA Prometheus pairs in Mimir with the distributor HA tracker and the cluster and replica labels."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-high-availability-deduplication/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: two Prometheus replicas scraping the same targets without double data.

Mimir (enable for all tenants):
```yaml
limits:
  accept_ha_samples: true
distributor:
  ha_tracker:
    enable_ha_tracker: true
    kvstore:
      store: memberlist
```
Flags: `-distributor.ha-tracker.enable=true`, `-distributor.ha-tracker.enable-for-all-users=true`, `-distributor.ha-tracker.store` (default `memberlist` from Mimir 3.0; the docs have a migration guide from Consul or etcd).

Prometheus replicas each set external labels (defaults are `cluster` and `__replica__`):
```yaml
global:
  external_labels:
    cluster: prom-team1
    __replica__: replica1     # replica2 on the other one
```
The distributor elects one replica per cluster and drops samples from the others. Mimir drops the replica label at ingest and keeps the cluster label, so series do not change on failover. If no new samples arrive from the leader for 30 s (default `ha_tracker_failover_timeout`, a per-tenant limit) the leader switches.

Per-tenant: set `accept_ha_samples` (keep `enable-for-all-users=false`), and `ha_cluster_label` / `ha_replica_label` in runtime overrides. Global label names: `-distributor.ha-tracker.cluster`, `-distributor.ha-tracker.replica`.

Gotchas
- Samples with only one or neither of the two labels are accepted and never deduplicated.
- The tracker checks only the first series of a write request to decide for the whole request; with federation or a metrics proxy in between, use the experimental `-distributor.ha-tracker.per-sample-dedupe` (limit `ha_tracker_per_sample_dedupe`).
- Samples from a non-elected replica get HTTP `202` with `replicas did not match, rejecting sample`: this is expected. Too many clusters for a tenant gives `400` `err-mimir-tenant-too-many-ha-clusters`; the limit is `-distributor.ha-tracker.max-clusters`.
- Failover loses about one scrape at a 15 s scrape period; make `rate()` ranges at least four times the scrape period.

## Verify
`GET /distributor/ha_tracker` is the HA tracker status endpoint on the distributor.

## Checked
2026-11-03. Confirmed against the Mimir HA deduplication page, the configuration parameters reference (defaults for `ha_cluster_label`, `ha_replica_label`, `ha_tracker_failover_timeout`, `accept_ha_samples`, `enable_ha_tracker`) and the HTTP API index (`/distributor/ha_tracker`). Removed: etcd example and the claim that memberlist is unsupported (memberlist is now the default), `ha_tracker.failover_timeout` placement (it is a limit), the deduplicated-samples metric name and the `count(up)` check, and the ruler remark.
Method: documentation only; no commands were run.
