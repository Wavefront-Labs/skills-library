---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-site-active-active-dr
name: multi-site-active-active-dr
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, disaster-recovery, multi-site-active-active, active-active, global-routing, write-conflict-resolution]
level: practitioner
status: docs-checked
description: "Design multi-site active-active disaster recovery: per-tier active state, data write models and conflict handling, traffic steering, capacity headroom and failover drills."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html", "https://learn.microsoft.com/azure/well-architected/reliability/redundancy", "https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-site active-active DR

## Steps
1. **Justify it**: the AWS DR whitepaper calls multi-site active/active the most complex and costly
   DR approach; it can cut recovery time to near zero for most disasters, but data corruption may
   still need backups, so the recovery point is not zero. Google's planning guide makes the same
   cost point: smaller RTO and RPO usually cost more to run and add administrative overhead. Use it
   for the tiers whose RTO is minutes or less. If you do not want both sites serving users,
   warm standby is the more economical and simpler option.
2. **Data write model** decides everything. The AWS whitepaper names three:
   - Write global: all writes go to one Region; if it fails another is promoted (Aurora global
     database; the whitepaper says promotion takes under a minute and typical replication latency
     is under a second).
   - Write local: writes go to the closest Region (DynamoDB global tables, which reconcile
     concurrent updates with last writer wins).
   - Write partitioned: a partition key such as user ID assigns each write to one Region, which
     avoids write conflicts.
   - Azure: a globally distributed store such as Azure Cosmos DB gives multi-region read and write
     (it offers two options for conflicting writes; choose per workload). For relational
     databases, use readable replicas with read-only connection strings.
3. **Traffic steering**: Route 53 supports percentage, geoproximity and latency policies; Global
   Accelerator uses a traffic dial per endpoint and avoids DNS caching issues. Azure's guide says
   to use latency or weighted global routing.
4. **Capacity**: Azure describes two active-active shapes. At capacity: each stamp serves its own
   load and scales up to absorb another location's load, which costs less but can degrade user
   experience while scaling. Overprovisioned: each stamp is sized for the other locations' load
   as well; most resilient, higher cost. AWS adds that Auto Scaling is a control-plane activity,
   so relying on it lowers recovery resilience; a hot, statically stable standby avoids that.
   Set service quotas in the recovery Region high enough to reach production capacity.
5. **Failover mechanics**: AWS advises using only data-plane operations in failover, because data
   planes have higher availability goals than control planes. With active/active there is no
   failover as such; the work is routing away from the lost Region.
6. **Drill regularly**: AWS says to test how the workload reacts to loss of a Region (is traffic
   routed away, can the others take all the traffic) and to test a data disaster separately;
   backup and recovery are still required. Google says to test regularly, including user access
   to the recovery environment.

## Gotchas
- Active-active needs extra effort on security and preventing human error: AWS notes that data
  corruption, deletion or obfuscation always has a recovery time above zero.
- Azure notes higher operating cost and management burden from synchronising application state and
  data across live environments.

## Verify
- [ ] Data write model documented per store with RPO.
- [ ] Region-loss drill passed within target RTO; a separate data-disaster restore tested.
- [ ] Recovery-Region quotas allow full production capacity.

## Checked
2026-11-08. Confirmed against the AWS "Disaster recovery options in the cloud" whitepaper page
(cost and complexity, near-zero recovery time, write global/local/partitioned, Aurora global
database under-one-minute promotion and sub-second latency, DynamoDB last writer wins, Route 53
policies, Global Accelerator traffic dial, Auto Scaling as control plane, data-plane-only
failover, testing), the Azure Well-Architected redundancy page (the former multi-region design
URL redirects to it: active-active at capacity vs overprovisioned, Cosmos DB multi-region writes,
readable replicas, latency or weighted routing) and the Google Cloud DR planning guide (RTO/RPO
cost relationship, regular testing). Removed: the under-50% utilisation figure, short-TTL advice,
Spanner, sticky-session and uniqueness-constraint gotchas (none stated in the pages), and the
Cosmos DB last-writer-wins wording.
Method: documentation only; no commands were run.
