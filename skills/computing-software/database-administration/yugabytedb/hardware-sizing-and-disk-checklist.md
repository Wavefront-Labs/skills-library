---
id: computing-software.database-administration.yugabytedb.hardware-sizing-and-disk-checklist
name: hardware-sizing-and-disk-checklist
category: computing-software
field: database-administration
product: yugabytedb
tags: [sizing, hardware, checklist, disks, xfs, jbod, ephemeral-disks, production-readiness]
level: practitioner
status: docs-checked
description: "Production hardware and storage checklist for YugabyteDB: CPU, RAM, SSD, XFS, JBOD, free-space headroom, supported OS, and rules for ephemeral-disk clouds."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/checklist.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hardware sizing and disk checklist

Minimums: 2 cores and 2 GB RAM for a test node. Production guidance is 16 or more cores and 32 GB for YCQL workloads, and 16 or more cores and 64 GB for YSQL.

Storage rules:
- SSD only. Do not use RAID; present disks as JBOD and create a data directory on each disk and pass a comma-separated list to YB-Master and YB-TServer in `--fs_data_dirs`.
- Use XFS (recommended) and mount the data drives with `noatime`. ZFS and NFS are not currently supported. Local or remote attached storage both work.
- Plan for about 20 percent headroom on each node for temporary compaction space, metadata and other overheads; typical space amplification is 10-20 percent.
- Third-party disk encryption software must be running before YugabyteDB starts, or restarting an encrypted node can corrupt data.

Platform: AlmaLinux 8 and RHEL 8 are the recommended production operating systems; x86 and ARM (aarch64) are supported. The CPU must support SSE2 and SSE4.2. Set system limits with ulimit and use chrony for time sync.

Cluster shape: the number of YB-Master servers should match the RF and the number of YB-TServers should not be less than the RF, each on a separate machine. Default RF is 3.

Ephemeral (local) disks are early access and supported only for manual deployments and YugabyteDB Anywhere with an on-premises provider:
- Never stop all nodes at once; total data loss.
- Use RF of at least 3 (RF 5 or more is recommended), spread across zones.
- Unless automatic master failover is enabled, run masters on dedicated VMs with persistent disks.
- Before rebooting a node, blacklist it and let it drain, or (recommended) remove it and add it back; work on one node at a time.
- Take frequent backups.

A node that loses its ephemeral disk needs a full re-replication of its data rather than an incremental catch-up, which takes minutes to hours and widens the double-fault window.

## Checked

2026-11-04. Confirmed against the Plan your deployment checklist: minimum 2 cores and 2GB RAM, production 16+ cores with 32GB+ (YCQL) or 64GB+ (YSQL), SSD required, no RAID/JBOD with comma-separated `--fs_data_dirs`, XFS and noatime, ZFS and NFS unsupported, about 20% headroom, AlmaLinux 8 and RHEL 8, x86 and ARM, SSE2 and SSE4.2, master count matching RF and tservers not below RF, and the ephemeral-disk guidance. Removed: the claim that `--fs_data_dirs` cannot be changed after creation, and the remote-bootstrap and snapshot reasons for headroom (not stated). The encryption-at-rest page supplies the disk-encryption warning.

Method: documentation only; no commands were run.
