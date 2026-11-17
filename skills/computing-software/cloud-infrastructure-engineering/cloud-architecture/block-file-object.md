---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.block-file-object
name: block-file-object
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, storage-selection, block-file-object, object-storage, file-storage, block-storage]
level: practitioner
status: docs-checked
description: "Choose block, file or object storage for a workload by access pattern, protocol, sharing, scale and redundancy, with Azure and Google Cloud service examples."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/data-management.html", "https://learn.microsoft.com/azure/architecture/guide/technology-choices/storage-options", "https://cloud.google.com/architecture/storage-advisor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Block vs file vs object storage

| | Block | File | Object |
|---|---|---|---|
| model | data in addressed blocks the application references; like SAN or direct-attached storage | files in folders, mounted by clients over NFS or SMB; like NAS | objects in a flat hierarchy of buckets or containers, each with an ID and metadata, accessed through REST APIs or client libraries |
| Azure | managed disks, Elastic SAN (iSCSI) | Azure Files (SMB, NFS), Azure NetApp Files, Azure Managed Lustre | Blob Storage, Data Lake Storage Gen2 |
| Google Cloud | Persistent Disk, Hyperdisk, Local SSD | Filestore, Managed Lustre, NetApp Volumes | Cloud Storage |
| fits | transaction processing and other high-IOPS workloads, databases, VM disks | lift-and-shift file systems, shared configuration, shared tooling, centralised logs, HPC | static content, backups and archives, media, data lakes, large downloadable objects |

## Steps
1. **Define requirements first**: data type, capacity now and later, automatic scaling, access from outside the cloud, read/write patterns, need for file access (and the NFS version), concurrent clients, encryption keys, residency, caching or scratch needs, replication, I/O rate and throughput, and which environments need which performance (Google Cloud storage guide). AWS Well-Architected lists the same drivers: data type (block, file, object), random or sequential access, throughput, frequency of access and update, availability and durability.
2. **Match the pattern**: low-latency, IOPS-heavy or locally attached storage points to block; shared files with NFS or SMB semantics to file; web access, backups, archives and analytics to object.
3. **Check sharing**: Google's comparison lists Local SSD as not shareable, and file services as mountable by many VMs. Azure Elastic SAN offers shared block over iSCSI for clustered nodes.
4. **Check redundancy and scope**: Persistent Disk and Hyperdisk are zonal with cross-zone synchronous and cross-region asynchronous replication options; Local SSD is ephemeral (data lost when the VM stops or is deleted); Cloud Storage stores data redundantly across zones with options across regions. Azure Storage offers LRS, ZRS, GRS, RA-GRS and RA-GZRS; Elastic SAN supports only LRS and ZRS.
5. **Check limits on the vendor page** before sizing. Examples stated by Google Cloud: Persistent Disk 64 TiB per disk, Filestore 100 TiB per instance (depends on tier), Cloud Storage 5 TiB per object with no bucket limit. Azure page blobs support a maximum of 8 TiB.
6. **Use storage tiers for cost**: Blob Storage has premium, hot, cool and archive tiers; archive has the lowest cost and may take hours to copy data to an accessible tier. Cloud Storage storage classes and lifecycle or retention policies control cost by duration. Compare costs with the vendor calculators; this skill keeps no prices.

## Gotchas
- Pick a purpose-built data store per access pattern rather than forcing one type to serve all (Well-Architected PERF03-BP01).
- Elastic SAN does not support encryption in transit; use managed disks if you need it.

## Verify
- [ ] Storage choice per data set documented with access pattern and redundancy requirement.

## Checked
2026-11-08. Confirmed on the Google Cloud storage strategy guide (block/file/object definitions, services, comparison table, requirement questionnaire), the Azure storage options guide (scenarios, Elastic SAN, redundancy, page blob 8 TiB, Blob tiers) and the AWS Well-Architected data management page (drivers, PERF03-BP01). Removed (not in the pages): the latency row (sub-ms, ms, tens of ms), PB-scale and cost-ranking claims, the S3 3,500/5,500 requests-per-second-per-prefix figures, s3fs and gcsfuse POSIX warnings, EFS throughput modes, AWS service names for the table, and orphaned-volume billing.
Method: documentation only; no commands were run.
