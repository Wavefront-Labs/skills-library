---
id: computing-software.systems-network-administration.backup-and-recovery.protection-tiers-and-sla-classes
name: protection-tiers-and-sla-classes
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [protection-tier, sla-classes, rpo, rto, tiering, service-catalogue]
level: practitioner
status: draft
description: "Define backup protection tiers: Gold/Silver/Bronze RPO, RTO, retention, copy and test rules, map systems to tiers from the BIA, and price them in a service catalogue."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
  - https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Protection tiers and SLA classes

Tiers stop every system getting bespoke treatment and make cost visible.

## Example tier table
| Tier | RPO | RTO | Method | Retention | Copies | Testing |
|---|---|---|---|---|---|---|
| Platinum | Minutes | < 1 h | Replication/CDP + backup | 30 d + monthly 12 m | Immutable + off-site | Quarterly failover |
| Gold | 4 h | 4-8 h | Backup every 4 h + logs every 15 min | 30 d + GFS 12 m/7 y | Immutable + off-site | Quarterly restore |
| Silver | 24 h | 24-48 h | Nightly backup | 14-30 d + monthly | Off-site copy | Semi-annual sample |
| Bronze | 7 d | Best effort / days | Weekly or rebuild from IaC | 4 weeks | One copy | Annual sample |

Put the numbers in your policy; these are illustrations.

## Assigning systems
- Start from the **BIA**: maximum tolerable downtime and data loss per business process map to RTO/RPO, then to the systems behind each process (including dependencies like AD, DNS, licensing servers).
- Dependencies inherit the highest tier of anything that needs them.
- Record the tier in the CMDB and in the backup tool (tag or job naming) so reports can check compliance per tier.

## Pricing
Show cost per GB per month per tier (storage, licences, replication capacity). Owners who demand Platinum for everything usually choose differently when charged.

## Gotchas
- RTO is achievable only if restore throughput supports it: 10 TB at 500 MB/s is about 6 hours of copy before any app work.
- Stateless or IaC-rebuildable servers may need only config/data backup, not image backup.
- Review tiers annually and after major application changes.

## Verify
Every in-scope system has a tier; test results per tier show measured RTO within target.
