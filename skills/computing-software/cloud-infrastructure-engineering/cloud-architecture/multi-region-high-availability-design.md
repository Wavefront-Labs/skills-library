---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-region-high-availability-design
name: multi-region-high-availability-design
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, high-availability, ha, multi-region, multi-az, active-active, active-passive, warm-standby, pilot-light, failover, global-load-balancing, route53, azure-front-door, traffic-manager, cloud-load-balancing, aurora-global-database, dynamodb-global-tables, cosmos-db, spanner, data-replication, replication-lag, cell-based-architecture, static-stability, blast-radius, availability-zones, dns-failover]
level: advanced
status: draft
description: "Design multi-AZ and multi-region HA: active-active vs active-passive per tier, data write ownership, health-checked global routing, statically stable failover."
sources: ["AWS Well-Architected Reliability Pillar", "AWS Builders' Library - Static stability using Availability Zones", "Azure Architecture Center - Multi-region web app", "Google Cloud Architecture Center - Disaster recovery and multi-region patterns"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-region high-availability design — fail over without depending on what failed

**Goal:** a service that survives the loss of a zone with no human action and the loss of a
region within a stated, tested time, without paying for a second region it doesn't need.

## 1. Start with multi-AZ, not multi-region
Most outages are zonal or self-inflicted (bad deploys). Multi-AZ inside one region covers
zonal loss at modest cost; multi-region adds latency, data-consistency and operational
complexity. Go multi-region only when one of these is true: the availability target
exceeds what one region's history supports (roughly > 99.95% for the whole stack),
a regulator or customer demands regional independence, or users are global and latency matters.

**Static stability:** provision each AZ (and each region) to carry its share of peak
*after* a loss — e.g. 3 AZs at 50% of peak each — so recovery needs no scaling calls to a
control plane that may itself be impaired during the event.

## 2. Pick a topology per tier, not per system
| Pattern | RTO | Cost vs single region | Use for |
|---|---|---|---|
| Backup & restore | hours | ~1.1x | internal tools |
| Pilot light (data replicated, compute off) | 10s of min | ~1.2x | most line-of-business |
| Warm standby (scaled-down live stack) | minutes | ~1.5x | revenue paths |
| Active-active | ~0 (reroute) | 2x+ | global read-heavy, strict targets |

Stateless web/API tiers are easy to make active-active; the **data tier** decides the real pattern.

## 3. Data: decide who owns writes
- **Single-writer + async replicas** (Aurora Global Database, Azure SQL failover groups,
  Cloud SQL cross-region replicas): simple, RPO = replication lag (typically seconds, can
  spike under load). Failover promotes a replica; writes in flight are lost.
- **Multi-writer** (DynamoDB global tables, Cosmos DB multi-region writes): last-writer-wins
  or custom conflict resolution — fine for idempotent/commutative data, dangerous for
  balances and inventory.
- **Globally consistent** (Spanner, CockroachDB): synchronous quorum, higher write latency
  across regions; you pay latency for RPO 0.
- **Partition by home region** (users pinned to one region; cell-based): avoids conflicts,
  limits blast radius; failover of a cell is a planned move.

Object storage: cross-region replication is async and may lag for large objects — check
replication metrics, not just the config.

## 4. Routing
- Global entry: Route 53 health-checked failover/latency records, Azure Front Door or
  Traffic Manager, Google global external Application LB (anycast).
- Health checks must test a **deep** path (can this region serve a real request, including
  its data store) but must not fail all regions when a shared dependency hiccups — fail open
  if every region is unhealthy.
- DNS failover is bounded by TTL *and* client resolver caching that ignores TTL; keep TTL
  60 s and expect a long tail. Anycast LBs avoid this.

## 5. Failover control
- Prefer data-plane mechanisms (health checks, Route 53 ARC routing controls) over
  control-plane API calls during an incident.
- Decide automatic vs human-triggered regional failover. Automatic flapping between regions
  with async data is worse than a 10-minute human decision — many teams automate AZ
  failover and keep region failover one-click manual.
- Fail back deliberately: resync data, verify, then shift traffic in steps.

## Gotchas
- Hidden single-region dependencies: IAM/identity provider, CI/CD, secrets manager, container
  registry, DNS zone hosting, a SaaS queue. Inventory them; a standby that can't pull images is not a standby.
- Global services with a home region (some control planes historically pinned to one region) can block failover actions.
- Quotas in the standby region are often default-low — raise them before you need them.
- Cross-region data transfer is billed per GB; chatty active-active designs get expensive.
- Async replication + automatic failover = silent data loss unless writes are reconciled.

## Verify
- [ ] Each tier has a named pattern, RTO and RPO, written down.
- [ ] Capacity per AZ/region survives the loss of one with no scale-up.
- [ ] A dependency inventory shows no single-region component on the critical path (or accepts it explicitly).
- [ ] Replication lag is monitored and alerted against the RPO.
- [ ] A regional failover has been executed (game day) in the last 6 months with measured RTO.
- [ ] Standby region quotas match production.

Uncertain: cost multipliers above are rough planning ratios, not quotes — model your own bill.
Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.disaster-recovery-planning, computing-software.cloud-infrastructure-engineering.cloud-architecture.cost-vs-resilience-tradeoffs
