---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dr-plan-zone-outage-runbook-and-multi-region-patterns
name: dr-plan-zone-outage-runbook-and-multi-region-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, disaster-recovery, dr-plan-document, dr-strategy, zone-outage-runbook, multi-region-architecture-patterns, rto-rpo, failover]
level: advanced
status: docs-checked
description: "Write a Google Cloud DR plan with RTO/RPO tiers and scenarios, a zone-outage runbook for zonal resources, and choose multi-region patterns from cold standby to active-active."
sources: ["https://cloud.google.com/architecture/dr-scenarios-planning-guide", "https://cloud.google.com/architecture/disaster-recovery", "https://cloud.google.com/architecture/infra-reliability-guide", "https://cloud.google.com/compute/docs/regions-zones"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DR plan, zone-outage runbook and multi-region patterns

## 1. DR plan document (per service, one page each)
- **Tier** with RTO/RPO per application criticality. Google's guide frames requirements as three scenarios (zonal outage, regional outage, extremely unlikely multi-region outage) and gives each tier its own RTO/RPO for zone and region outages; set your own numbers from business impact.
- **Scenarios**: zone loss, region loss, data corruption/deletion, ransomware or credential compromise, dependency outage (SaaS, Google API), human error.
- **Pattern** chosen per scenario (table below) and where the data copies live.
- **Runbook links**, owners, communication plan, and a **test schedule** set by tier.
- Dependencies: DNS, identity, secrets, CI/CD, quotas in the DR region (pre-request them).

## 2. Patterns
| Pattern | RTO | Data | GCP building blocks |
|---|---|---|---|
| Backup & restore (cold) | longest | backups and images copied to another region | redeploy infrastructure from code and images in region 2 only after a regional outage |
| Warm standby | shorter | async replicas | Cloud SQL cross-region replica (promote), GCS dual-region or multi-region, regional MIG with minimal resources, load balancer in each region, Cloud DNS for orchestrated but manual regional failover |
| Active-active | near zero | synchronous / multi-region data | multi-region databases, load balancing across regions, stateless services in 2+ regions |
Corruption or deletion needs **point-in-time** recovery, not only replicas: for example Spanner PITR protects against logical corruption and accidental deletion, and replicas copy the damage. Pre-check each product's DR section in the Disaster recovery building blocks guide; BigQuery multi-region does not give cross-region replication.

## 3. Zone-outage runbook
1. Confirm via Personalized Service Health (it communicates incidents and planned maintenance relevant to your projects) and your own per-zone metrics.
2. Regional services (regional MIGs, Cloud Run, which serves from other zones) keep running; verify capacity in remaining zones and that autoscaling can place instances.
3. Zonal resources (for example sole-tenant nodes, which are zonal): recreate them in a healthy zone from templates, images or backups; check each product's zonal-outage section in the building blocks guide.
4. Pin new deployments away from the zone (zone lists in templates and node pools) until all-clear.
5. After recovery: rebalance and remove temporary capacity.

## Gotchas
- DR regions without quota or reservations for GPUs/large shapes = no DR. Pre-request quota.
- Untested DR plans fail on IAM, DNS TTLs and hardcoded regions; test end to end.
- Cross-region replication adds network cost; include it in the business case.

## Checked
2026-10-31. Confirmed in the Disaster recovery building blocks guide and the DR scenarios planning guide (fetched this batch): three outage scenarios, per-tier RTO/RPO, Cloud SQL cross-region replica, dual-region and multi-region Cloud Storage, warm-standby pattern with Cloud DNS manual failover, Spanner PITR, Personalized Service Health, BigQuery multi-region note, sole-tenant nodes zonal. Removed: example RTO/RPO figures, test-frequency figures, Cloud DNS failover routing policy, Backup and DR vaults, Filestore Basic and PD snapshot restore steps, hot-standby row (unconfirmed).
Method: documentation only; no commands were run.

## Verify
- [ ] Last DR test date, achieved RTO/RPO and issues recorded per Tier 1 service.
- [ ] Zone-outage game day: one zone's capacity removed in staging, SLO held.
