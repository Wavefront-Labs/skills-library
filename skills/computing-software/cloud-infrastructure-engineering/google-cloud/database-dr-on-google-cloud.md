---
id: computing-software.cloud-infrastructure-engineering.google-cloud.database-dr-on-google-cloud
name: database-dr-on-google-cloud
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, ha-dr-design, database-dr, dr-for-databases, cross-region-replicas, rpo-rto]
level: advanced
status: docs-checked
description: "Design and drill database DR on GCP: Cloud SQL cross-region replicas, replica promotion and advanced DR switchover, AlloyDB secondary clusters, backups and failover drills."
sources: ["https://cloud.google.com/architecture/dr-scenarios-for-data", "https://cloud.google.com/sql/docs/postgres/intro-to-cloud-sql-disaster-recovery", "https://cloud.google.com/alloydb/docs/cross-region-replication/about-cross-region-replication", "https://cloud.google.com/spanner/docs/instance-configurations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database DR on Google Cloud

## 1. Map engine to options
| Engine | Regional failure option |
|---|---|
| Cloud SQL | Cross-region read replica and **replica promotion**, or advanced DR with a designated DR replica (switchover, replica failover) |
| AlloyDB | Cross-region secondary cluster (asynchronous, read-only) that you promote to a primary cluster |
| Spanner | Dual-region or multi-region instance configuration (see the instance configurations page) |
Other engines (Firestore, Bigtable, Memorystore): read that product's own DR page; not covered here.
Replication copies bad writes too, so also keep backups for logical corruption.

## 2. Cloud SQL cross-region replica
```bash
gcloud sql instances create orders-dr --master-instance-name=orders --region=us-west1 --tier=<SAME_TIER>
# disaster: promote
gcloud sql instances promote-replica orders-dr
```
Promoting the cross-region replica is the failover; transactions not yet replicated are unavailable on the new primary
(replication is asynchronous). Take a backup of the new primary immediately after failover, before clients connect.

Advanced DR: designate a DR replica. `gcloud sql instances switchover` is the planned path (primary goes read-only,
the DR replica catches up to zero lag, then is promoted; zero data loss) and also serves for routine DR drills.
Replica failover is the unplanned path and can lose data if the DR replica lags. Afterwards the old primary becomes a
replica of the promoted instance, and a switchover restores the original topology. A write endpoint (global DNS name)
follows the primary, so apps need no connection change.

## 3. Application side
- Use the write endpoint where available, otherwise point at the new primary's address.
- Writes during failover: idempotent retries; know which in-flight transactions may be lost (async replication).

## 4. Drill
Use switchover to rehearse; measure actual recovery time and replication lag at cutover; restore a backup to a new
instance and run checksums. Record numbers against your targets.

## Verify
- [ ] Last drill's measured recovery time and data loss are within target and documented; backups exist beyond the primary region.

## Checked
2026-11-01. Confirmed against the Cloud SQL disaster recovery intro (replica promotion, asynchronous loss of
unreplicated transactions, backup after failover, advanced DR switchover vs replica failover, old primary becoming a
replica, write endpoint, drills via switchover), the AlloyDB cross-region replication page (asynchronous read-only
secondary cluster, promote) and the three gcloud sql commands via the command reference. Removed: per-engine RPO/RTO
figures, Firestore/Bigtable/Memorystore rows, Spanner config names, quarterly drill cadence, tier/PSA gotchas, the
`--failover` flag (not confirmed).
Method: documentation only; no commands were run.
