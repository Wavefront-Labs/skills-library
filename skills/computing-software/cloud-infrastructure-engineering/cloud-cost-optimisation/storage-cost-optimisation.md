---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.storage-cost-optimisation
name: storage-cost-optimisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-aware-architecture, storage-cost-optimisation, block-storage-costs, gp3, premium-ssd-v2, snapshot-sprawl, object-storage-costs, request-costs, storage-lens]
level: practitioner
status: draft
description: "Cut storage cost across block, file, object and backups: volume type migrations, snapshot sprawl, request-heavy buckets, versioning leftovers, and storage analytics tools."
sources: ["https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html", "https://learn.microsoft.com/azure/virtual-machines/disks-types", "https://www.finops.org/framework/capabilities/architecting-for-cloud/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Storage cost architecture

## Block storage
- Migrate AWS **gp2 → gp3** (cheaper per GB, baseline 3000 IOPS/125 MB/s independent of size;
  online modification). Azure: evaluate Premium SSD v2 (IOPS/throughput decoupled from size) vs
  Premium SSD; GCP: Hyperdisk / pd-balanced vs pd-ssd.
- Overprovisioned provisioned IOPS (io1/io2, Ultra) — compare to CloudWatch `VolumeReadOps/WriteOps` peaks.
- Unattached volumes (state `available`) and oversized volumes.

## Snapshots and backups
- Snapshot sprawl: AMIs/snapshots kept forever. Use lifecycle policies (Data Lifecycle Manager,
  AWS Backup plans, Azure Backup policies) and delete orphaned snapshots of deleted volumes/AMIs.
- Archive tiers for long-term (EBS Snapshots Archive, Azure archive tier for backups).

## Object storage
- Storage class by access pattern (see storage lifecycle policies); Intelligent-Tiering for unknown patterns.
- **Request costs**: millions of small PUT/GET can cost more than storage — batch small objects,
  cache reads behind a CDN.
- **Versioning leftovers**: noncurrent versions and delete markers accumulate; add
  `NoncurrentVersionExpiration` and abort incomplete multipart uploads (`AbortIncompleteMultipartUpload` after 7 days).
- Analytics: S3 Storage Lens (free metrics + advanced), Azure Storage insights/blob inventory, GCS Storage Insights.

## File storage
EFS/Azure Files/Filestore: use lifecycle to IA tiers; throughput mode choice (elastic vs provisioned).

## Verify
- [ ] No gp2 volumes remaining (or documented exceptions).
- [ ] Every bucket with versioning has noncurrent-version expiration.
- [ ] Orphan snapshot report runs monthly.
