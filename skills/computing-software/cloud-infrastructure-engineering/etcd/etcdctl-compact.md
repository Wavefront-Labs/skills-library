---
id: computing-software.cloud-infrastructure-engineering.etcd.etcdctl-compact
name: etcdctl-compact
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [compact, compaction, revision, etcdctl, history, auto-compaction]
level: practitioner
status: docs-checked
description: "Compact the etcd key history with etcdctl compact REVISION, use auto-compaction modes, and know what it does and does not free."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/maintenance/"
  - "https://etcd.io/docs/v3.5/dev-guide/interacting_v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcd keeps an exact history of the keyspace, so the history must be compacted periodically to avoid performance degradation and eventual storage exhaustion. Compaction drops all information about keys superseded before a given revision; the space they used becomes available for further writes.

```bash
etcdctl compact 5
# compacted revision 5
etcdctl get --rev=4 foo
# Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

Finding the current revision: a `get` on any key, even a nonexistent one, in JSON shows it in the header.

```bash
etcdctl get mykey -w=json
# {"header":{"cluster_id":...,"member_id":...,"revision":15,"raft_term":4}}
```

What it frees: logical history. After compaction the backend database is internally fragmented: the gaps are usable by etcd but not by the host filesystem, so the file does not shrink until you defragment (see the defragmentation skill).

Auto-compaction is set with `--auto-compaction-mode` and `--auto-compaction-retention`. There are two modes, `periodic` (default) and `revision`.

- Periodic: `--auto-compaction-retention=1h` keeps one hour of history. With a retention above 1 hour etcd compacts every hour while keeping the full window (with `10h` it waits 10 hours for the first compaction, then compacts hourly); with 1 hour or less it compacts at the retention interval. The guide suggests short periods such as `1h` or `30m` for frequently updated keys and longer ones such as `24h` to `72h` for infrequent updates.
- Revision: `--auto-compaction-mode=revision --auto-compaction-retention=1000` keeps a fixed number of revisions. etcd checks every 5 minutes and compacts on "latest revision" minus 1000 (latest 30000 compacts to 29000).

Manual `etcdctl` compaction gives fine-grained control; automatic compaction fits applications that only need history for some time.

## Checked

2026-11-08. Read the v3.5 maintenance guide and the interacting-with-etcd guide in full. Confirmed: compact command and compacted-revision error, finding the revision with get -w=json, periodic (default) and revision auto-compaction modes with the 1 hour rule and 5 minute check, fragmentation after compaction. Removed: --physical, retention 0 disables, jq command, Kubernetes remark and the any-endpoint claim, which the pages do not state.

Method: documentation only; no commands were run.
