---
id: computing-software.cloud-infrastructure-engineering.etcd.auto-compaction
name: auto-compaction
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [auto-compaction, compaction-mode, periodic, revision, retention, compaction-batch-limit, history-retention]
level: practitioner
status: docs-checked
description: "Enable automatic history compaction with --auto-compaction-mode periodic or revision and --auto-compaction-retention."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/maintenance/"
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcd can compact automatically. Configure two flags:

- `--auto-compaction-mode`: `periodic` (the default) or `revision`.
- `--auto-compaction-retention`: the retention value; the default is 0, meaning auto compaction is disabled.

Periodic mode: retention is a duration (time-based window of history). Examples:

```bash
etcd --auto-compaction-retention=1h     # keep one hour of history
etcd --auto-compaction-mode=periodic --auto-compaction-retention=30m
```

With mode `periodic` the value defaults to hours if no time unit is provided; duration strings such as `30m` are accepted. A record is not compacted until about that duration after creation, so slow watchers can catch up. When the retention is greater than 1 hour etcd compacts every hour while keeping the full window (with `10h`, the first compaction happens after 10 hours, then hourly); when it is 1 hour or less, etcd compacts at the retention interval. The page suggests a short period such as 1h or 30m for frequently updated keys and 24h to 72h for infrequent updates.

Revision mode: retention is a number of revisions to keep:

```bash
etcd --auto-compaction-mode=revision --auto-compaction-retention=1000
```

etcd checks every 5 minutes and compacts on the latest revision minus 1000 (for example latest revision 30000 compacts at 29000).

Notes:

- Compaction leaves internal fragmentation in the backend database: deleting data does not reclaim space on disk until you defragment.
- Revisions prior to the compaction revision become inaccessible: `etcdctl get --rev=2 somekey` fails with `etcdserver: mvcc: required revision has been compacted`.
- `--experimental-compaction-batch-limit` (default 1000) sets the maximum revisions deleted in each compaction batch.
- Manual compaction is `etcdctl compact REVISION`.

## Checked

2026-11-03. Confirmed on the v3.5 maintenance guide: periodic as the default mode, retention semantics and the 1 hour rule with the 10h example, recommended values, revision mode with the 5-minute check and latest-minus-1000 example, fragmentation after compaction, the required-revision-has-been-compacted error, etcdctl compact. Confirmed on the configuration page: --auto-compaction-retention default 0 disables, the periodic/revision description with default hours, --experimental-compaction-batch-limit 1000 (maximum revisions per batch). Corrected: the one-tenth interval rule was wrong. Removed: the Kubernetes API server compaction statement.

Method: documentation only; no commands were run.
