---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-zone-aware-replication
name: grafana-mimir-zone-aware-replication
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [zone-aware, replication, availability-zones, ingesters, rollout-operator]
level: advanced
status: docs-checked
description: "Describes enabling Mimir zone-aware replication for Alertmanager, ingesters and store-gateways, minimum zone counts, balance, costs and the rollout operator."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-zone-aware-replication/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zone-aware replication

Zones are failure domains (availability zones, data centres, racks, anti-affinity groups). Without zone awareness, replicas for data can land in one zone, so a zone outage can lose data. Your deployment tooling must also be zone-aware: roll out one zone at a time.

## Alertmanager

Set `-alertmanager.sharding-ring.instance-availability-zone` per replica, roll out, then `-alertmanager.sharding-ring.zone-awareness-enabled=true`. Alerts replicate to `-alertmanager.sharding-ring.replication-factor` replicas, one per zone.

## Ingesters

Set `-ingester.ring.instance-availability-zone`, roll out, then `-ingester.ring.zone-awareness-enabled=true` on distributors, ingesters and queriers.

- **Ingest storage**: distributors write each series to one Kafka partition (Kafka replicates). Zone-aware replication is achieved by deploying the ingesters of one partition, typically two, in different zones. `-ingester.ring.replication-factor` is not used.
- **Classic**: also set `-ingester.ring.replication-factor`. Use at least as many zones as the replication factor (3 by default). Fewer zones can miss writes or fail them. A deployment needs `floor(replication factor / 2) + 1` healthy zones.

## Store-gateways

Follow the zone awareness section of the store-gateway docs.

## Operating notes

Run the same replica count per zone; unbalanced zones run hotter. Cross-zone traffic is usually billed; in classic mode set `-ingester.client.grpc-compression` to `snappy` or `gzip` on distributors to cut it. The Kubernetes Rollout Operator automates multi-zone rollouts, even for a single physical zone.

## Checked

Confirmed against the page: zone examples, Alertmanager, ingest storage and classic ingester steps, minimum zones and the floor(RF/2)+1 rule, unbalanced zones, compression flag and the Rollout Operator. Nothing removed.

Method: docs-checked 2026-11-09 against the raw markdown of the Mimir configure-zone-aware-replication page (grafana/mimir main), read in full.
