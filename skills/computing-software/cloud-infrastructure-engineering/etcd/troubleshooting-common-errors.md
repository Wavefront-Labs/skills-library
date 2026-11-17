---
id: computing-software.cloud-infrastructure-engineering.etcd.troubleshooting-common-errors
name: troubleshooting-common-errors
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [troubleshooting, errors, request-size, took-too-long, compacted, database-space-exceeded, heartbeat]
level: practitioner
status: docs-checked
description: "Common etcd errors and warnings and their documented causes: request size, space exceeded, compacted revision, slow apply, heartbeats."
sources:
  - "https://etcd.io/docs/v3.5/dev-guide/limit/"
  - "https://etcd.io/docs/v3.5/op-guide/failures/"
  - "https://etcd.io/docs/v3.5/op-guide/maintenance/"
  - "https://etcd.io/docs/v3.5/faq/"
  - "https://etcd.io/docs/v3.5/dev-guide/interacting_v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Frequent errors and warnings, with the fix the etcd 3.5 docs give.

- Large requests: etcd is designed for small key-value pairs. Larger requests work but may increase the latency of other requests. The default maximum request size is 1.5 MiB, set with the `--max-request-bytes` server flag. The storage limit defaults to 2 GiB (`--quota-backend-bytes`); 8 GiB is the suggested maximum and etcd warns at startup above it.
- `etcdserver: mvcc: database space exceeded`: a member's backend database passed the space quota, so a cluster-wide NOSPACE alarm puts the cluster in maintenance mode that accepts only reads and deletes. Recover by compacting the history, defragmenting every endpoint, then disarming the alarm. The maintenance page example: `etcdctl compact REVISION`, `etcdctl defrag` (add `--cluster` to cover all members), `etcdctl alarm disarm`; `etcdctl alarm list` shows the alarm. Defragmenting a live member blocks reads and writes while it rebuilds, and a request only applies to the local node. Setting `--auto-compaction` avoids exhausting space.
- `etcdserver: mvcc: required revision has been compacted`: a read used a revision older than the compaction point; revisions before the compacted one are no longer accessible.
- Leader loss: when a leader fails, a new one is elected after about an election timeout. During the election the cluster cannot process writes; requests sent meanwhile are queued, and some writes not yet committed may time out, but committed writes are never lost. Frequent leader loss can come from disk latency spikes (disk latency is part of leader liveness); tune disk settings or etcd time parameters.
- Warning `apply entries took too long`: etcd warns when the average apply duration exceeds 100 ms (normally under 50 ms). Usual cause is a slow disk (check backend_commit_duration_seconds, p99 under 25 ms), then CPU starvation, then expensive requests touching too many keys.
- Warning `failed to send out heartbeat on time`: the leader skipped two heartbeat intervals. Usual cause is a slow disk (check wal_fsync_duration_seconds, p99 under 10 ms), then CPU starvation, then a slow network. For cross-data-center clusters, set `heartbeat-interval` near the round-trip time and `election-timeout` to at least 5 times it.
- Warning `request ignored (cluster ID mismatch)`: usually appears after tearing down an old cluster and reusing some peer addresses while an old etcd process is still running. Make peer addresses of distinct clusters disjoint.

Useful diagnostic command from the maintenance page: `etcdctl --write-out=table endpoint status`.

## Checked

Method: docs-checked 2026-11-09 against the etcd v3.5 limit, failures, maintenance, FAQ and interacting_v3 pages. Removed claims not found on those pages: the exact no leader, request timed out, too many requests, authentication and learner error strings, and the cluster-ID cause involving data directory or token.
