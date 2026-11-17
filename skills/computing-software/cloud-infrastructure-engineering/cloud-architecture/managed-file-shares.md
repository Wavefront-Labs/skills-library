---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.managed-file-shares
name: managed-file-shares
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, storage-selection, managed-file-shares, nfs, smb, efs, azure-files, filestore, fsx]
level: practitioner
status: draft
description: "Select managed file shares (NFS/SMB): EFS, FSx variants, Azure Files/NetApp Files, Filestore; protocol, performance modes, identity, backup and cost trade-offs."
sources: ["https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html", "https://docs.aws.amazon.com/fsx/", "https://learn.microsoft.com/azure/storage/files/storage-files-planning", "https://cloud.google.com/filestore/docs/service-tiers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Managed file share selection (NFS / SMB)

## Steps
1. **Protocol and client OS**: Linux NFS (EFS, Azure Files NFS, Azure NetApp Files, Filestore,
   FSx for OpenZFS/ONTAP), Windows SMB with AD (FSx for Windows File Server, Azure Files SMB,
   FSx for ONTAP, Azure NetApp Files dual-protocol).
2. **Performance profile**: small-file metadata-heavy (home dirs, CMS) vs large sequential
   (media, HPC). HPC scratch needs parallel file systems (FSx for Lustre, Azure Managed Lustre,
   Google Managed Lustre/Parallelstore).
3. **Throughput model**: EFS elastic throughput vs provisioned; Azure Files premium (provisioned)
   vs standard (pay per transaction); Filestore tiers by capacity/performance. Check per-share
   IOPS and throughput limits against peak.
4. **Identity**: SMB with AD DS/Entra Kerberos; NFS with POSIX IDs or Kerberos where supported;
   access points for per-app root directories (EFS access points).
5. **Data protection**: snapshots, AWS Backup/Azure Backup, cross-region replication options.
6. **Cost**: per GB-month by tier, lifecycle to infrequent-access tiers (EFS IA/Archive),
   throughput charges.

## Gotchas
- File shares used as a database store or for lock-heavy apps (SQLite) perform badly and corrupt.
- Latency to shares across zones or regions hurts metadata-heavy workloads.

## Verify
- [ ] Peak IOPS/throughput within the share limits with headroom.
- [ ] Backups and restore of a single file tested.
