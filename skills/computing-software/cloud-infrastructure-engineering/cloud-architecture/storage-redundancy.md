---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.storage-redundancy
name: storage-redundancy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, storage-selection, storage-redundancy, lrs-zrs-grs, s3-replication, dual-region-buckets, durability-vs-availability, cross-region-storage]
level: practitioner
status: docs-checked
description: "Choose storage redundancy (local, zonal, regional, geo, dual/multi-region) per data set by durability, availability, RPO, residency and cost, and know what failover involves."
sources: ["https://learn.microsoft.com/azure/storage/common/storage-redundancy", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html", "https://cloud.google.com/storage/docs/locations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage redundancy options

## Azure Storage
| Option | Replication | Durability (per page) |
|---|---|---|
| LRS | Single physical datacenter in the primary region | at least 11 nines |
| ZRS | Synchronous across three or more availability zones | at least 12 nines |
| GRS | LRS in primary, asynchronous copy to a secondary region (LRS there) | at least 16 nines |
| GZRS | ZRS in primary, asynchronous copy to secondary (LRS there) | at least 16 nines |

- GRS and GZRS data in the secondary is not readable unless failover occurs; RA-GRS / RA-GZRS give read access (secondary
  endpoint is the account name plus `-secondary`, same keys). Azure Files does not support RA-GRS or RA-GZRS.
- Read availability SLA targets: at least 99.9% for LRS, ZRS, GRS, GZRS and at least 99.99% for RA-GRS / RA-GZRS (lower
  figures for cool/cold/archive tiers; see the page table).
- Outage scenarios: a lost datacenter loses LRS data; ZRS survives a zone but not a region; GRS/GZRS survive a regional
  outage but need account failover to restore write availability.
- Geo replication is asynchronous, so failure can lose recent writes; the gap is the RPO. Geo priority replication
  makes the RPO for block blobs 15 minutes or less.
- Redundancy protects against hardware failure, not against data-modifying operations: deletes and overwrites apply to
  all copies.
- The redundancy setting is per storage account; isolate data with different needs in separate accounts. The archive
  tier is not supported with ZRS, GZRS or RA-GZRS; unmanaged disks do not support ZRS or GZRS. The paired secondary
  region is fixed by the primary and cannot be changed.
- Microsoft recommends ZRS in the primary region for high availability, and GZRS for regional-disaster protection.

## Amazon S3 replication
- Live replication (CRR across Regions, SRR within a Region) is asynchronous and copies new and updated objects only;
  existing objects need S3 Batch Replication (on demand; also for replicas and previously FAILED objects).
- S3 Replication Time Control (RTC) replicates 99.99 percent of new objects within 15 minutes, backed by an SLA (the
  page's table also says 99.9 percent; check the current SLA). RTC does not apply to Batch Replication.
- Two-way replication rules plus replica modification sync keep objects and metadata in sync, and are needed before
  Multi-Region Access Point failover controls.
- Replication can retain metadata, change storage class and owner (owner override), and target multiple regions.

## Google Cloud Storage locations
- Zone (Rapid Bucket only, single zone, zonal outages might affect availability), region (redundant across zones),
  dual-region (asynchronous across two regions, turbo replication option for replication within 15 minutes), and
  multi-region (ASIA, EU, US). Dual-region and multi-region offer RTO = 0 automated failover per the page.
- Dual-regions are predefined (for example NAM4 = US-CENTRAL1 + US-EAST1) or configurable.
- Montreal, Osaka, Queretaro and Stockholm regions have three zones in one or two datacenters and data could be lost in
  a disaster; the page suggests a dual-region or backup to a second region.
- For pricing differences between location types see the pricing page; dual-region and multi-region incur replication
  charges on write.

## Verify
- [ ] Each data set has a documented redundancy choice with RPO.
- [ ] Failover procedure tested on a non-production account.
- [ ] Replication paired with versioning or backups, since replicas copy deletes.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against Azure Storage redundancy, S3 replication overview and Cloud Storage bucket locations. Removed: the
cross-provider comparison table (EBS, EFS, One Zone-IA, regional PD), "S3 11 nines", "geo-replication doubles storage"
and Azure failover details (account becomes LRS) which those pages do not state.
