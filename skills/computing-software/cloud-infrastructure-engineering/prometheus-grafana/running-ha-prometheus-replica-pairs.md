---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.running-ha-prometheus-replica-pairs
name: running-ha-prometheus-replica-pairs
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-ha-pair, prometheus-replica-pairs, high-availability, external-labels, thanos-dedup, alertmanager-ha]
level: advanced
status: docs-checked
description: "Run identical Prometheus replicas for HA with replica external labels, deduplicate in Thanos Query or the Mimir HA tracker, and know the tracker defaults and failover behaviour."
sources: ["https://prometheus.io/docs/introduction/faq/#can-prometheus-be-made-highly-available", "https://thanos.io/tip/components/query.md/#deduplication", "https://grafana.com/docs/mimir/latest/configure/configure-high-availability-deduplication/", "https://prometheus-operator.dev/docs/api-reference/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HA Prometheus replica pairs

The Prometheus FAQ answer to "Can Prometheus be made highly available?" is yes: run identical Prometheus servers on two
or more separate machines. Systems like Thanos, and many external systems that support remote write, can deduplicate the
data. Prometheus does not replicate its database between the servers (Thanos docs), so each replica holds its own copy
with gaps in different places.

## Config
Give each replica the same configuration except for one external label identifying the replica:
```yaml
global:
  external_labels:
    cluster: prom-team1
    replica: replica1        # replica2 on the other server
```
- Thanos Query: pass the label name with `--query.replica-label` (repeatable); series differing only in that label are
  merged, which also hides gaps in one source. See the thanos-querier-deduplication skill.
- Prometheus Operator: the `replicaExternalLabelName` field names the external label denoting the replica; default
  `prometheus_replica`, and the label is not added when the field is set to the empty string.
- Mimir: the defaults for the HA tracker are the labels `cluster` and `__replica__`:
  ```yaml
  global:
    external_labels:
      cluster: prom-team1
      __replica__: replica1
  ```
  These are external labels, unrelated to the `remote_write` configuration. Mimir drops the replica label when ingesting
  but keeps the cluster label, so series do not change when replicas change.

## Mimir HA tracker
- Enable in the distributor with `-distributor.ha-tracker.enable=true`, plus `-distributor.ha-tracker.enable-for-all-users=true`
  (`accept_ha_samples`, default false) or enable per tenant in the runtime overrides.
- KV store: `-distributor.ha-tracker.store` defaults to memberlist (recommended from Mimir 3.0); Consul and etcd are
  alternatives with a documented migration path.
- Label names: `-distributor.ha-tracker.cluster` (default `cluster`) and `-distributor.ha-tracker.replica` (default
  `__replica__`); both overridable per tenant (`ha_cluster_label`, `ha_replica_label`).
- Behaviour: one replica per cluster is the elected leader; samples from other replicas are dropped (HTTP 202 with
  "replicas did not match"). If no samples arrive from the leader within the failover timeout
  (`-distributor.ha-tracker.failover-timeout`, default 30s) leadership moves. With 15s scrapes you will likely lose a
  single scrape on failover, so use a `rate()` interval of at least four times the scrape period (1m for 15s).
- Samples with only one or neither of the cluster and replica labels are accepted and never deduplicated. For
  performance the tracker checks only the first series of a request; if a request can mix labels (federation, a metrics
  proxy) the experimental `-distributor.ha-tracker.per-sample-dedupe` exists.

## Verify
- [ ] Stopping one replica produces no gap in Thanos or Mimir query results.
- [ ] A replica label that is missing on one replica shows up as duplicated series; check the external labels of both.

## Checked

Checked 2026-11-08 against the Prometheus FAQ, the Thanos Query deduplication section, the Mimir HA deduplication page,
the Mimir configuration reference (defaults) and the Prometheus Operator API reference (`replicaExternalLabelName`).
Removed because the pages do not state them: the Alertmanager `alert_relabel_configs` labeldrop snippet and the claim that
Alertmanager dedups identical alerts, load-balancer stickiness advice, anti-affinity advice, and the statements about
duplicated recording-rule series and counter differences between replicas.
Method: docs-only read of cited pages, 2026-11-08
