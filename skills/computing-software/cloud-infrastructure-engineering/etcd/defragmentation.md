---
id: computing-software.cloud-infrastructure-engineering.etcd.defragmentation
name: defragmentation
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [defrag, defragmentation, disk-space, db-size, fragmentation, etcdctl-defrag, maintenance]
level: practitioner
status: docs-checked
description: "Reclaim disk space after compaction with etcdctl defrag; it blocks the member while running and is not replicated, so cover every member."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/maintenance/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

After compaction etcd frees old revisions inside the backend database, but that space is only free for etcd to reuse; the host filesystem does not get it back. Deleting application data does not reclaim disk space either. Defragmentation releases the space back to the filesystem.

```bash
etcdctl defrag
# Finished defragmenting etcd member[127.0.0.1:2379]
etcdctl defrag --cluster
etcdctl defrag --data-dir <path-to-etcd-data-dir>     # only while etcd is not running
```

Facts from the maintenance guide:

- Defragmentation is issued per member, so cluster-wide latency spikes can be avoided.
- Defragmenting a live member blocks the system from reading and writing data while it rebuilds its state.
- The request is not replicated across the cluster; it applies only to the local node. To cover the cluster, list every member in `--endpoints`, or use `--cluster` to find all members automatically.
- To defragment a data directory directly, run `defrag --data-dir` while etcd is not running.
- After a NOSPACE alarm the recovery order is: compact, defragment, then `etcdctl alarm disarm`.
- `etcd_mvcc_db_total_size_in_use_in_bytes` shows actual usage after compaction; `etcd_mvcc_db_total_size_in_bytes` includes free space waiting for defragmentation (named `etcd_debugging_mvcc_db_total_size_in_bytes` before v3.4).

## Checked

2026-11-08. Read the v3.5 maintenance guide in full. Confirmed: per-member defrag, blocking of reads and writes, not replicated, --cluster and --endpoints, offline --data-dir form, compact-defrag-disarm order, the two size metrics and the v3.4 rename. Removed: etcdutl defrag, leader-last ordering, free-disk-space requirement, bootstrap defrag threshold flag and dbSizeInUse JSON fields, none of which the page states.

Method: documentation only; no commands were run.
