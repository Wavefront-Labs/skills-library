---
id: computing-software.cloud-infrastructure-engineering.azure.event-hubs-geo-replication-and-geo-dr
name: event-hubs-geo-replication-and-geo-dr
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, event-hubs, eh-geo-replication, eh-geo-dr, geo-disaster-recovery, metadata-replication, alias, promote-secondary, replication-lag, synchronous-replication, asynchronous-replication, premium-tier, dedicated-cluster]
level: advanced
status: docs-checked
description: "Protect Event Hubs across regions: Geo-DR alias (metadata only) vs geo-replication (data + metadata), consistency modes, planned and forced promotion, and client handling."
sources: ["https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-geo-dr", "https://learn.microsoft.com/en-us/azure/event-hubs/geo-replication", "https://learn.microsoft.com/en-us/azure/event-hubs/use-geo-replication", "https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-quotas", "https://learn.microsoft.com/en-us/azure/event-hubs/monitor-event-hubs-reference", "https://learn.microsoft.com/en-us/cli/azure/eventhubs/georecovery-alias"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event Hubs geo-replication and Geo-DR

**Goal:** an Event Hubs namespace that keeps accepting events after a regional outage, with a
known RPO for in-flight data and clients that follow the failover.

## 1. Two features, different guarantees
| | **Geo-disaster recovery (alias)** | **Geo-replication** |
|---|---|---|
| Replicates | **metadata only** (entities, consumer groups, settings) | metadata **and event data**, offsets, consumer checkpoints in-service |
| Tiers | Standard, Premium, Dedicated | Premium, Dedicated |
| Endpoint | alias FQDN switches to the secondary namespace | namespace FQDN stays; primary role moves between regions |
| Failover | one-time move; pairing is broken after failover | customer-managed promotion of a secondary (graceful or forced) |
| Data in flight at failure | not replicated; stays in the old primary | depends on replication mode |

## 2. Geo-replication (Premium/Dedicated)
- Add a secondary region to the namespace (portal *Geo-replication* settings); the maximum replication lag is set for asynchronous mode.
- **Synchronous**: the secondary commits before the primary acknowledges → no data loss, longer latency; availability depends on both regions.
- **Asynchronous**: the primary acknowledges before replication, bounded by the configured *max replication lag*; if lag grows beyond it,
  the primary throttles incoming requests. Data loss is possible on forced promotion.
- Monitor `ReplicationLagDuration` / `ReplicationLagCount`; alert approaching the maximum.
- **Promote**: a graceful promotion completes replication first; a forced (non-graceful) promotion may lose events not yet copied and can leave offsets different between regions. Promotion repoints the namespace FQDN to the selected secondary and demotes the old primary to a secondary; no client changes are needed.

## 3. Geo-DR alias (metadata only)
```bash
az eventhubs georecovery-alias set -g rg-uks --namespace-name evhns-uks -a evhns-prod-alias --partner-namespace <evhns-ukw-id>
az eventhubs georecovery-alias show -g rg-uks --namespace-name evhns-uks -a evhns-prod-alias --query "{role:role,state:provisioningState,pending:pendingReplicationOperationsCount}"
az eventhubs georecovery-alias fail-over -g rg-ukw --namespace-name evhns-ukw -a evhns-prod-alias     # run against the SECONDARY
```
- Clients must use the **alias** connection (`<alias>.servicebus.windows.net`). Entra RBAC assignments are not replicated; create them on the secondary too.
- After failover: producers write to the new primary, but **events left in the old primary are not
  moved**; consumers start from new offsets — design consumers to tolerate duplicates/gaps.
- After failover the pairing is broken; set up pairing again to a new secondary once the incident ends.

## 4. Client and consumer considerations
- For AMQP clients the checkpoint store (for example Blob storage) must be available to the secondary region so clients can read checkpoints after failover. For Kafka, offsets are committed to Event Hubs and replicated.
- Use a private DNS zone `privatelink.servicebus.windows.net` per region linked to that region's virtual network, with a private endpoint in each region.

## Gotchas
- Geo-DR alias does not replicate data — teams often assume it does.
- Synchronous replication lengthens latency (distributed commit); measure before choosing.
- Forced promotion with async mode can lose data not yet replicated; document the maximum replication lag as your RPO target.
- Private DNS for the alias/namespace must resolve in the DR region's networks too.

## Verify
- [ ] Replication state healthy; `ReplicationLagDuration` well below the configured max under peak.
- [ ] Planned promotion drill: producers and consumers continue on the same FQDN; event counts reconcile.
- [ ] (Alias) `fail-over` drill in non-prod documented, including re-pairing steps.

## Checked
Checked 2026-10-24 against azure-docs Event Hubs geo-disaster recovery and geo-replication pages, the tier features include, and the azure-docs-cli eventhubs georecovery-alias reference (set, show, fail-over, break-pair exist). Confirmed: geo-DR replicates metadata only and is available on Standard, Premium and Dedicated; geo-replication replicates data and metadata on Premium and Dedicated only; synchronous versus asynchronous behaviour and throttling past the maximum lag; forced promotion can lose data; promotion repoints the namespace FQDN; ReplicationLagDuration and ReplicationLagCount metrics. Removed unconfirmed: ARM property names for geo-replication, the claim that regions can swap back for free, Kafka client tuning values, GZRS advice.

Method: documentation only; no commands were run.
