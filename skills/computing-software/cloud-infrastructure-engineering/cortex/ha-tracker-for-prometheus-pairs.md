---
id: computing-software.cloud-infrastructure-engineering.cortex.ha-tracker-for-prometheus-pairs
name: ha-tracker-for-prometheus-pairs
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [ha-tracker, deduplication, consul, etcd, cluster-label]
level: practitioner
status: docs-checked
description: "Deduplicate samples from redundant Prometheus replicas with the distributor HA Tracker, including the labels and supported KV stores."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/architecture.md
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/ha-pair-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When two or more Prometheus replicas scrape the same targets, enable the distributor High Availability Tracker so Cortex stores only one copy of each series.

It deduplicates on two labels: a cluster label that identifies the group of redundant servers for a tenant, and a replica label that identifies the member within it. Samples from any replica that is not the currently elected one are dropped as duplicates. Samples carrying one or none of the two labels are accepted by default and never deduplicated.

Election state lives in a key-value store, and the distributor accepts samples only from the elected leader. Supported stores for the HA tracker are Consul and Etcd. Memberlist is not supported: gossip propagates updates too slowly, so different distributors could see different replicas as leader, which is undesirable.

Client side: set two external labels on each Prometheus. Defaults are `cluster` (the same on every replica of a group, for example `prom-team1`) and `__replica__` (unique per replica, such as the pod name). They are external labels and have nothing to do with the remote_write config. Both names are configurable per tenant, so pick a cluster label that does not clash with one your workloads already use (`team`, `cluster`, `prometheus`). Cortex drops the replica label on ingest but keeps the cluster label, so series do not change when replicas change.

Server side, the minimum is `-distributor.ha-tracker.enable=true`, a KV store for the tracker (only Consul and etcd; `multi` is for migration only), and `-distributor.ha-tracker.enable-for-all-users` or `accept_ha_samples: true` in limits.

Failover: if Cortex sees no new samples from the leader for a short period it elects the other replica, so a few minutes of outage on one replica does not lose data.

If you also use remote_read, do not put `__replica__` in external labels (Prometheus adds external labels to read queries and Cortex would return nothing); add it with `write_relabel_configs` on the remote_write section instead.

## Checked

2026-11-04. Claims were read against the Cortex docs page: HA pair handling guide (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.
