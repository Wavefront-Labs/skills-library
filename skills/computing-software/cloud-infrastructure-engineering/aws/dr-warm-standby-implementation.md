---
id: computing-software.cloud-infrastructure-engineering.aws.dr-warm-standby-implementation
name: dr-warm-standby-implementation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, disaster-recovery, warm-standby, warm-standby-implementation, warm-standby-design, scaled-down-replica, aurora-global-database, write-forwarding, dynamodb-global-tables, synthetic-traffic, cross-region, rto, rpo]
level: advanced
status: draft
description: "Run a warm-standby DR Region on AWS: a scaled-down, fully working stack that serves test or read traffic, scales on failover and is proven by synthetic checks."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html", "https://aws.amazon.com/blogs/architecture/disaster-recovery-dr-architecture-on-aws-part-iii-pilot-light-and-warm-standby/", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database-write-forwarding.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Warm standby DR — implementation

**Goal:** RTO of minutes: the DR Region runs the whole application at reduced capacity all
the time, is exercised constantly so you *know* it works, and failover is mostly scaling
plus a routing switch.

## 1. Shape of the standby
| Layer | Warm standby setting |
|---|---|
| Aurora | Global Database secondary **with** reader instance(s) (smaller class OK); optional write forwarding for low-volume writes |
| DynamoDB | Global table replica (on-demand, or provisioned with auto scaling ready for primary peak) |
| Compute | ASGs/ECS services running at e.g. 10–25% of primary, `max` sized for full load |
| Caches | ElastiCache Global Datastore or a small cache that will warm |
| Queues/streams | Deployed; consumers running at low concurrency |
| Edge | ALB live, registered in routing (weight 0 or secondary) |
Same IaC and pipeline as the primary; deploy every release to both Regions in the same
pipeline run (DR first or last, but always).

## 2. Keep it honest
- **Synthetic traffic**: CloudWatch Synthetics canaries hit the DR endpoint directly
  (Region-specific hostname) every few minutes, exercising read and (if write forwarding
  or a test tenant exists) write paths. Alarm on failures exactly like production.
- Optionally serve real read-only traffic (latency routing for reads, or a small weighted
  share) — the best proof it works.
- Track **config parity**: same app version, same feature flags, same secrets versions;
  ARC readiness checks can assert resource/config parity across Regions.

## 3. Failover runbook
1. Decision (criteria + owner) — automatic only for unambiguous Region loss.
2. Data: `aws rds failover-global-cluster --global-cluster-identifier app-global --target-db-cluster-identifier <DR_ARN> --allow-data-loss`
   (unplanned) or `switchover-global-cluster` (planned); DynamoDB global tables are already
   writable everywhere — stop writes in the old Region to avoid conflicts.
3. Scale: raise ASG `min/desired` to primary peak, ECS desired counts, Lambda reserved
   concurrency, DynamoDB provisioned capacity (if not on-demand).
4. Route: ARC routing control / Route 53 failover or weights to 100% DR.
5. Watch: error rate, latency, scaling progress; canaries on the public hostname.

## 4. Sizing the standby
- Standby capacity must absorb traffic during scale-up: if scale-out takes 10 minutes and
  your RTO is 15, the standby needs enough capacity to serve a degraded but acceptable
  share for those 10 minutes (shed load / rate-limit non-critical features meanwhile).
- Typical cost: 20–40% of primary, mostly compute and database instances.

## Gotchas
- Scale-up relies on the DR Region's EC2 control plane and capacity — healthy by
  assumption, but capacity can be tight during large events. Use capacity reservations
  for the critical tier.
- Write forwarding adds latency and is not a substitute for failover; do not route
  write-heavy traffic through it.
- Shared global dependencies (a single IdP, a third-party API allowlisting only primary
  NAT IPs) silently break the standby. Allowlist DR egress IPs now.
- Standby left at a stale app version is the most common failure; enforce dual-Region deploys.

## Verify
- [ ] DR canaries green continuously; alarms page the same on-call as production.
- [ ] Version/parity check: DR and primary run the same build hash.
- [ ] Failover game day: traffic on DR within RTO; scaling reached target capacity; failback rehearsed separately.
- [ ] Replication lag alarms below RPO.
