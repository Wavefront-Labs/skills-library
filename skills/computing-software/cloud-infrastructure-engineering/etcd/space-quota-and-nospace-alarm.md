---
id: computing-software.cloud-infrastructure-engineering.etcd.space-quota-and-nospace-alarm
name: space-quota-and-nospace-alarm
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [quota, nospace, alarm, quota-backend-bytes, database-space-exceeded, alarm-disarm, read-only]
level: practitioner
status: docs-checked
description: "What happens when etcd hits its backend quota: NOSPACE alarm, the database space exceeded error, and the compact-defrag-disarm recovery."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/maintenance/"
  - "https://etcd.io/docs/v3.5/dev-guide/limit/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The backend size quota is `--quota-backend-bytes` (default 2 GiB; 8 GiB is the suggested maximum). When any member's backend database exceeds it, etcd raises a cluster-wide alarm (NOSPACE) that puts the cluster into a maintenance mode accepting only key reads and deletes. Writes fail with `etcdserver: mvcc: database space exceeded`. The quota is checked at the API layer (early rejection) and the Apply layer (which raises the alarm), so a request can return a no-space error and still have succeeded in the backend.

Recovery:

```bash
# 1. find the current revision
rev=$(etcdctl endpoint status --write-out=json | egrep -o '"revision":[0-9]*' | egrep -o '[0-9].*')
# 2. compact
etcdctl compact $rev
# 3. defragment (--cluster covers all members; defrag is not replicated)
etcdctl defrag --cluster
# 4. clear the alarm
etcdctl alarm disarm
```

The page's order is: free space in the keyspace, defragment, clear the alarm; `etcdctl alarm list` shows `alarm:NOSPACE`. Note that defragmenting a live member blocks reads and writes while it rebuilds.

Prevention:

- Compact the keyspace history (manually or with auto-compaction).
- Watch `etcd_mvcc_db_total_size_in_use_in_bytes` (actual usage after compaction) and `etcd_mvcc_db_total_size_in_bytes` (including free space awaiting defragmentation, renamed from `etcd_debugging_mvcc_db_total_size_in_bytes` in v3.4); when both are close to the quota, compaction is required.
- Setting a quota also helps mitigate disk-exhaustion denial of service.
- Raising the quota above 8 GiB triggers a startup warning.

## Checked

2026-11-03. Confirmed on the v3.5 maintenance guide (Space quota) and System limits page: --quota-backend-bytes 2 GiB default and 8 GiB suggested maximum with startup warning, cluster-wide alarm and reads-and-deletes-only mode, the database space exceeded error, the revision/compact/defrag/alarm disarm sequence, defrag not replicated and blocking, API-layer and Apply-layer quota checks, the two size metrics and the v3.4 rename. Removed: the jq command (replaced by the page's), the CORRUPT alarm remark and the hot-key and defragment-on-schedule advice.

Method: documentation only; no commands were run.
