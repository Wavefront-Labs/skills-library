---
id: computing-software.data-engineering.apache-kafka.kafka-disaster-recovery-topologies
name: kafka-disaster-recovery-topologies
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, geo-replication, kafka-disaster-recovery, active-passive, active-active, stretch-cluster, rpo-rto, failover, failback, multi-region]
level: sme
status: docs-checked
description: "Choose and run a Kafka DR topology: stretch cluster vs active-passive vs active-active, RPO/RTO each gives, client failover mechanics, and a DR drill checklist."
sources:
  - https://kafka.apache.org/documentation/#georeplication-use-cases
  - https://kafka.apache.org/39/documentation/#datacenters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka disaster recovery topologies

**Goal:** a written, tested answer to "region X is gone, what happens to our event streams?"

## Options
| Topology | How | RPO | RTO | Costs/risks |
|---|---|---|---|---|
| **Stretch cluster** | One cluster across 3 AZs/DCs (rack-aware, RF 3, min ISR 2, `acks=all`) | 0 within the stretch | ~0 (automatic leader election) | Needs a low-latency link between sites; the docs advise against one cluster spanning datacenters over a high-latency link |
| **Active-passive** | Primary + DR cluster, async replication (MirrorMaker 2 or a vendor replication product) | Replication lag (seconds-minutes) | Minutes: switch clients, translate offsets | Simple; DR idle; failback needs reverse replication |
| **Active-active** | Producers write locally in each region; each region replicates to the other with prefixed topics | Lag of the failed region's un-replicated tail | Low: consumers already read both | Consumers must merge `orders` + `remote.orders`; ordering only per region; dedupe across regions |
A common design: stretch across AZs within a region + active-passive to a second region for regional disasters.

## Client failover mechanics
- Bootstrap via DNS names you control (`kafka.prod.acme.internal`) so failover = DNS change + client restart, or keep per-region config profiles switchable via config service.
- Producers: switch to DR cluster; with IdentityReplicationPolicy they write to the same topic names.
- Consumers: stop, translate offsets (see consumer-offset-translation), start on DR. Expect a reprocessing window.
- Schema Registry must also be replicated/available in DR (schema IDs must match: use registry replication/exporters, or a single global registry).
- Connectors and Streams apps need deployments ready in DR (state stores rebuild from changelog topics if those are replicated).

## Data you lose
In async topologies, records acknowledged by the primary but not yet replicated are lost or stranded until the primary returns. Decide per topic whether that is acceptable; payment-critical flows may need the stretch design or synchronous writes to two clusters (rare, complex).

## DR drill checklist
1. Announce; freeze deploys.
2. Measure replication lag at drill start.
3. Fail over a non-critical producer and consumer group; record RTO.
4. Verify data continuity: counts by key/time window on DR vs expectations.
5. Fail back; confirm no duplicates beyond the idempotency window.
6. Write up actual RPO/RTO vs targets.

## Verify
- [ ] Each critical topic has a documented RPO/RTO and topology.
- [ ] A DR drill was executed in the last 6-12 months with measured results.
- [ ] Schema registry, ACLs, quotas, and connectors exist in DR.

## Checked
2026-11-01. Confirmed in the Kafka 3.9 docs (operations: datacenters, geo-replication with MirrorMaker 2: remote topics renamed by a replication policy, `DefaultReplicationPolicy` default; `IdentityReplicationPolicy` in the upgrade notes). Removed unconfirmed latency and quorum figures and vendor-specific claims.
Method: documentation only; no commands were run.
