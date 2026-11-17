---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-ha-deduplication
name: grafana-mimir-ha-deduplication
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [high-availability, ha-tracker, deduplication, prometheus-replicas, external-labels]
level: advanced
status: docs-checked
description: "Explains Mimir HA tracker deduplication for Prometheus HA pairs: cluster and replica labels, leader election, failover timing and distributor configuration."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-high-availability-deduplication/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HA deduplication

Run redundant Prometheus pairs without ingesting everything twice. Mimir elects one leader replica per cluster and drops samples from the others. If no samples arrive from the leader for 30 seconds (default), the leader switches. With a 15 s scrape interval you typically lose one scrape on failover, so use a `rate()` range at least four times the scrape period (1 minute for 15 s).

## Prometheus side

Set two external labels, defaults `cluster` and `__replica__`:

```yaml
global:
  external_labels:
    cluster: prom-team1
    __replica__: replica1
```

Mimir drops the replica label at ingest and keeps the cluster label, so series do not change when replicas do.

## Mimir side

1. Enable the tracker on distributors: `-distributor.ha-tracker.enable=true`. For all tenants add `-distributor.ha-tracker.enable-for-all-users=true`, or set `accept_ha_samples` per tenant.
2. Configure the KV store: `-distributor.ha-tracker.store` (default memberlist from Mimir 3.0; consul and etcd can migrate to memberlist without downtime).
3. Label names: `-distributor.ha-tracker.cluster`, `-distributor.ha-tracker.replica`, per tenant `ha_cluster_label` and `ha_replica_label`.

```yaml
limits:
  accept_ha_samples: true
distributor:
  ha_tracker:
    enable_ha_tracker: true
    kvstore:
      store: memberlist
```

## Behaviour and errors

- Requests with only one or none of the labels are accepted and never deduplicated.
- The tracker checks only the first series of a request. If series in one request can have different labels, enable experimental `-distributor.ha-tracker.per-sample-dedupe`.
- Non-elected replica: HTTP 202 with `replicas did not match`.
- Too many HA clusters for a tenant: HTTP 400 with `err-mimir-tenant-too-many-ha-clusters`.

## Checked

2026-11-04. Confirmed against the Mimir page "Configure Grafana Mimir high-availability deduplication": failover timeout, rate() guidance, labels, enable flags, KV store default, example YAML and both error responses. Nothing removed.
Method: documentation only; no commands were run.
