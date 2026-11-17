---
id: computing-software.data-engineering.apache-hadoop.hdfs-name-and-space-quotas
name: hdfs-name-and-space-quotas
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, quota, dfsadmin, setquota, capacity]
level: practitioner
status: docs-checked
description: "HDFS name quotas and space quotas: setQuota/setSpaceQuota semantics, replication counting, edge cases, clearing, and checking usage with count -q."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsQuotaAdminGuide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Name and space quotas

Name quota: a hard limit on the number of file and directory names in the tree rooted at a directory. A directory counts against its own quota, so a quota of 1 keeps it empty. Creating over quota fails; a rename that would violate a quota fails. Setting a quota still succeeds if the directory would already be in violation. New directories have no quota; the largest value is Long.Max_Value.

Space quota: a hard limit on bytes used by files in the tree. Block allocation fails if the quota cannot take a full block. Each replica counts, so 1 GB at replication 3 uses 3 GB; quotas are charged at the intended replication factor, and changing a file's replication credits or debits the quota. A quota of zero still permits creating files but no blocks can be added. Directories and host-filesystem metadata space do not count.

Quotas stick with renamed directories and persist in the fsimage. At startup, a warning is printed for each quota the fsimage already violates. Setting or removing a quota creates a journal entry.

Admin-only commands:

```
hdfs dfsadmin -setQuota <N> <dir>...
hdfs dfsadmin -clrQuota <dir>...
hdfs dfsadmin -setSpaceQuota <N> <dir>...     # N accepts binary prefixes, e.g. 50g, 2t
hdfs dfsadmin -clrSpaceQuota <dir>...
```

Each is best effort per directory, with faults reported for a missing directory or a file; set also faults on an invalid N or if the directory would immediately exceed the new quota. Clearing a quota that is not set is not a fault.

Report: `hadoop fs -count -q [-h] [-v] [-t [types]] <dir>` shows the quota set and remaining for names and space. Where no quota is set the values are `none` and `inf`. -h gives human-readable sizes, -v adds a header.

## Checked

Method: 2026-11-08 docs-only read of the page's source file (HdfsQuotaAdminGuide.md in the apache/hadoop repo). Added the edge cases the page states; removed an example "Verify" step the page does not state.
