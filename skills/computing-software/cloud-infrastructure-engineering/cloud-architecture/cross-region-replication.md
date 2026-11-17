---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cross-region-replication
name: cross-region-replication
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, disaster-recovery, cross-region-replication, data-replication, replication-lag, rpo]
level: practitioner
status: draft
description: "Choose cross-region replication per data store: sync vs async, native options for databases, object and block storage, lag monitoring, cost and consistency effects."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html", "https://learn.microsoft.com/azure/storage/common/storage-redundancy", "https://cloud.google.com/storage/docs/locations", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cross-region data replication choices

## Steps
1. **Set RPO per data store**; that decides sync vs async. Synchronous cross-region adds
   round-trip latency to every write (tens of ms); almost everything is asynchronous.
2. **Pick the native mechanism**:
   - Object: S3 Cross-Region Replication (Replication Time Control for a 15-minute SLA),
     Azure GRS/GZRS/RA-GRS, GCS dual- and multi-region buckets (turbo replication option).
   - Relational: Aurora Global Database (typically sub-second lag, managed promotion),
     cross-region read replicas, Azure SQL failover groups, Cloud SQL cross-region replicas.
   - NoSQL: DynamoDB global tables, Cosmos DB multi-region.
   - Block/VM: snapshot copy schedules, AWS Elastic Disaster Recovery, Azure Site Recovery.
3. **Replicate deletes deliberately**: replicating deletes and corruption copies the
   disaster; keep versioning/point-in-time recovery and backups in addition to replication.
4. **Monitor lag** (ReplicaLag, ReplicationLatency metrics) and alert when it exceeds RPO.
5. **Encryption keys** must exist in the target region (multi-region keys or separate keys).
6. **Cost**: inter-region transfer per GB plus duplicate storage; estimate from write volume.

## Gotchas
- Replication is not backup; ransomware deletes replicate too.
- Azure GRS secondary is read-only unless RA-GRS, and failover is account-level.

## Verify
- [ ] RPO per store met by measured lag.
- [ ] Keys, versioning and backups present in the target region.
