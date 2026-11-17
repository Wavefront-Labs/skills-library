---
id: computing-software.cloud-infrastructure-engineering.etcd.etcdctl-endpoint-health-status
name: etcdctl-endpoint-health-status
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [endpoint, endpoint-health, endpoint-status, hashkv, cluster, leader, db-size]
level: practitioner
status: docs-checked
description: "Check member state with etcdctl endpoint status: table columns, JSON revision, and use in quota and version checks."
sources:
  - "https://etcd.io/docs/v3.5/dev-guide/interacting_v3/"
  - "https://etcd.io/docs/v3.5/op-guide/maintenance/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The cited pages document `endpoint status` only; they do not document `endpoint health` or `endpoint hashkv`, so look those up in `etcdctl endpoint --help` on your version.

```bash
etcdctl --write-out=table endpoint status
etcdctl --endpoints=:2379 endpoint status --write-out="json"
```

- The table output shows, per endpoint: `ENDPOINT`, `ID`, `VERSION`, `DB SIZE`, `IS LEADER`, `RAFT TERM` and `RAFT INDEX` (the maintenance page's example; newer versions may add columns).
- The version column is the server version, which is how the Versioning page says to check a running cluster.
- In JSON output the current store revision is the `revision` in the header. The interacting page also shows the current revision from `etcdctl get mykey -w=json` on any key, existent or not: `{"header":{"cluster_id":...,"member_id":...,"revision":15,"raft_term":4}}`.
- `DB SIZE` helps confirm the space quota has been exceeded: after `mvcc: database space exceeded` appears, `endpoint status` shows the member's size and `etcdctl alarm list` shows `alarm:NOSPACE`.
- The `--cluster` flag is documented on the maintenance page for `etcdctl defrag --cluster`, which finds all members; the page does not show it for `endpoint status`.

Metrics related to size: `etcd_mvcc_db_total_size_in_use_in_bytes` is actual database usage after a history compaction, and `etcd_debugging_mvcc_db_total_size_in_bytes` (renamed `etcd_mvcc_db_total_size_in_bytes` from v3.4) includes free space waiting for defragmentation. When both are close to the quota, compaction is required.

## Checked

2026-11-08. Read in full: etcd v3.5 Interacting with etcd page and Maintenance page. Confirmed the table columns shown, the JSON revision field, the quota and alarm flow and the size metrics. Removed: endpoint health and endpoint hashkv descriptions, the --cluster behaviour for these subcommands, IS LEARNER and raft applied index columns, dbSizeInUse and the use-case advice (none appear on the pages read).
Method: documentation only; no commands were run.
