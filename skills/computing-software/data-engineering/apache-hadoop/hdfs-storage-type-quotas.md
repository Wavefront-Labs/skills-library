---
id: computing-software.data-engineering.apache-hadoop.hdfs-storage-type-quotas
name: hdfs-storage-type-quotas
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, quota, storage-types, ssd, archive]
level: advanced
status: docs-checked
description: "HDFS storage type quotas (SSD, DISK, ARCHIVE, PROVIDED, NVDIMM): commands, the storage policy prerequisite, and recommended practice alongside space quotas."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsQuotaAdminGuide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage type quotas

A storage type quota is a hard limit on usage of one storage type by files under a directory. Available types in the commands are DISK, SSD, ARCHIVE, PROVIDED and NVDIMM. It works like a space quota but gives finer control, and combines with name and space quotas. Usage reflects intended placement per the storage policy: 1 GB at replication 3 with ALL_SSD consumes 3 GB of SSD quota.

Commands (admin only):

```
hdfs dfsadmin -setSpaceQuota <N> -storageType <type> <dir>...
hdfs dfsadmin -clrSpaceQuota -storageType <type> <dir>...
```

N accepts binary prefixes (50g, 2t). Set is best effort per directory and faults on an invalid N, a missing directory or file, or an immediate violation. Clearing a quota that is not set is not a fault.

Reporting: `hadoop fs -count -q -t [types] <dir>` shows per-storage-type quota and remaining; with listed types only those are shown, otherwise all types supporting quotas.

Guidance from the guide:
- Storage policies must be configured on the directory so files can land on different types (see the Archival Storage page).
- With a policy: set type quotas on constrained types such as SSD and leave other type quotas and the overall space quota less restrictive or unlimited. HDFS deducts from both the target type and the overall space quota.
- Without a policy: do not set type quotas. They can be set even if the type is unavailable or not configured, but use an overall space quota since type information is unavailable or inaccurate.
- A DISK quota is of limited use except when DISK is not the dominant medium, for example a cluster that is mostly ARCHIVE.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (HdfsQuotaAdminGuide.md in the apache/hadoop repo). Corrected an inverted DISK-quota claim, added NVDIMM, removed an unsupported "Verify" step.
