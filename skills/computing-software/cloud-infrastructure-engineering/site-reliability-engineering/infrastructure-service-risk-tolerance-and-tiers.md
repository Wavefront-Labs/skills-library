---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.infrastructure-service-risk-tolerance-and-tiers
name: infrastructure-service-risk-tolerance-and-tiers
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [infrastructure-risk-tolerance, service-tiers, embracing-risk, platform-sre, multi-tenant-infrastructure, availability-target]
level: advanced
status: docs-checked
description: "Set risk tolerance for shared infrastructure with conflicting clients by splitting into service tiers (low-latency vs throughput) with separate SLOs, pricing and capacity."
sources: ["https://sre.google/sre-book/embracing-risk/", "https://sre.google/workbook/implementing-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Infrastructure service risk tolerance and tiers

Shared infrastructure (storage, queues, databases, internal LBs) has many clients with contradictory needs.
The SRE Book's Bigtable example: online serving wants low latency and high availability; offline analytics
wants throughput and cheap capacity and tolerates unavailability. One SLO cannot serve both.

## Method
1. **Inventory clients** and classify each: latency-sensitive serving, throughput batch, archival.
2. **Measure their real requirement** from their own SLOs: a frontend cannot exceed the availability of a
   serial dependency without retries, caching or a fallback.
3. **Define tiers as separate offerings**, each with its own SLO, capacity and cost:

| Tier | SLO focus | Provisioning |
|---|---|---|
| Low-latency | low latency, high reliability | substantial slack capacity for less contention and more redundancy |
| Throughput/batch | throughput over latency | run very hot with less redundancy |

The book's Bigtable example uses these two cluster types and says the throughput clusters can cost far less to
run (perhaps as little as 10-50% of a low-latency cluster). Add a middle tier only if clients need it.

4. **Enforce the split technically**: separate clusters or priority classes, request criticality
   (see request criticality in the SRE Book Handling Overload chapter), separate quotas. A tier that shares queues with batch is not a tier.
5. **Publish** the tier contract (SLO, error budget policy, what clients must do: retries with backoff,
   timeouts, deadline propagation).

## Cost of the wrong single target
- Too high: everyone pays for low-latency capacity they do not need.
- Too low: serving clients build their own caches and replicas, duplicating infrastructure.

## Gotchas
- Clients pick the highest tier if it is free; tie tiers to quota or chargeback.
- Report SLO compliance per tier; an aggregate hides that batch traffic is starving serving.
- Exposing the cost of each level of service motivates clients to choose the cheapest level that meets their needs.

## Checked

2026-11-01. Confirmed against the SRE Book chapter Embracing Risk, section Identifying the Risk Tolerance of
Infrastructure Services (Bigtable low-latency versus throughput clusters, slack versus running hot, partitioning
into levels of service, cost externalised to clients, same hardware and software with different guarantees) and
Handling Overload (request criticality). Removed: the example SLO numbers, utilisation percentages and the price column.
Method: documentation only; no commands were run.

## Verify
- [ ] Each client mapped to a tier with a documented reason.
- [ ] Tiers isolated (separate capacity or priority) and load-tested under contention.
- [ ] Per-tier SLO dashboard and error budget exist.
