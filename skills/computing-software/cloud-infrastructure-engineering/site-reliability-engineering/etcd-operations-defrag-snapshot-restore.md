---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.etcd-operations-defrag-snapshot-restore
name: etcd-operations-defrag-snapshot-restore
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, distributed-consensus, etcd-defrag, etcd-snapshot-restore, etcd, kubernetes]
level: advanced
status: docs-checked
description: "Operate etcd clusters: health checks, compaction and defragmentation, space quota alarms, snapshot backups and restore, and member replacement without losing quorum."
sources: ["https://etcd.io/docs/v3.5/op-guide/maintenance/", "https://etcd.io/docs/v3.5/op-guide/recovery/", "https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://etcd.io/docs/v3.5/op-guide/runtime-configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd operations

**Goal:** keep etcd (for example the Kubernetes datastore) healthy, small and recoverable.

## Health
```bash
export ETCDCTL_API=3 EP=https://10.0.0.1:2379,https://10.0.0.2:2379,https://10.0.0.3:2379
C="--cacert=ca.crt --cert=client.crt --key=client.key"
etcdctl --endpoints=$EP $C endpoint health
etcdctl --endpoints=$EP $C endpoint status -w table     # leader, DB size, raft index
etcdctl --endpoints=$EP $C alarm list
```
Also watch the etcd metrics for leader presence and changes, WAL fsync and backend commit latency, and database size against the quota.

## Compaction and defrag
- History grows with every revision; **compaction** discards superseded revisions (`etcdctl compact <revision>`, or automatically with `--auto-compaction-mode` and `--auto-compaction-retention`; modes are periodic (default) and revision).
- Compaction leaves free pages; **defragmentation** returns space to the filesystem:
```bash
etcdctl --endpoints=https://10.0.0.1:2379 $C defrag      # applies to that member only; blocks reads and writes on it
```
Defrag is per member and not replicated; `etcdctl defrag --cluster` finds all members. A live member cannot read or write while it rebuilds, so defrag them one at a time.
- **Space quota** (`--quota-backend-bytes`, in bytes; the default is conservative, see the maintenance guide): when a member's database exceeds it, etcd raises a cluster-wide `NOSPACE` alarm and accepts only reads and deletes. Fix: free space (compact), defrag, then `etcdctl alarm disarm`.

## Snapshots
```bash
etcdctl --endpoints=https://10.0.0.1:2379 $C snapshot save /backup/etcd-$(date +%F-%H%M).db
etcdutl snapshot status /backup/etcd-2026-10-18-0200.db -w table
```
Schedule (for example hourly), copy off-host, encrypt (contains Secrets).

## Restore (disaster: quorum lost or data corrupted)
1. Stop traffic to etcd (API servers) and stop the etcd members.
2. On each member: `etcdutl snapshot restore snap.db --name m1 --initial-cluster m1=https://10.0.0.1:2380,m2=...,m3=... --initial-cluster-token etcd-restore-1 --initial-advertise-peer-urls https://10.0.0.1:2380 --data-dir /var/lib/etcd-restored`.
3. Point etcd at the new data dir, start members, then API servers.
Restore builds a new cluster from the snapshot; everything after the snapshot is lost.

## Member replacement (one failed member, quorum intact)
`etcdctl member remove <id>`, then `etcdctl member add m3 --peer-urls=https://10.0.0.3:2380`, and start the new member with `--initial-cluster-state existing`. Never remove members such that quorum is lost.

## Verify
- [ ] Restore drill into a test cluster from last night's snapshot succeeds; DB size well under quota; fsync latency within your target.

## Checked
2026-11-01. Confirmed against the etcd v3.5 maintenance, recovery and runtime-configuration guides and the Kubernetes etcd task page: compaction modes, defrag behaviour and `--cluster`, quota alarm behaviour, snapshot save and status, restore flags, member remove/add and `--initial-cluster-state existing`. Removed: metric names and thresholds, default and maximum quota sizes, the Kubernetes compaction interval and the defrag order.
Method: documentation only; no commands were run.
