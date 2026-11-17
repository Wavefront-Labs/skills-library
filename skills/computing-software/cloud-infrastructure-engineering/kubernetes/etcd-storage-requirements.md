---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-storage-requirements
name: etcd-storage-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, fsync, wal, defrag, db-size-limit, raft, control-plane, disk-latency, nvme, control-plane-storage, etcdctl]
level: sme
status: docs-checked
description: "etcd's storage requirements for the cluster's own control plane: fsync latency budget, disk type, the 8GB db-size default, and defrag/compaction."
sources: ["https://etcd.io/docs/v3.6/op-guide/hardware/", "https://etcd.io/docs/v3.6/faq/", "https://etcd.io/docs/v3.6/dev-guide/limit/", "https://etcd.io/docs/v3.6/op-guide/maintenance/", "https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd storage requirements — the cluster's own most demanding stateful workload

**Goal:** know why etcd is uniquely sensitive to disk latency (not throughput), and
the maintenance operations that keep its database from hitting a hard size wall.

## 1. Latency, not throughput, not capacity
etcd's Raft consensus does a disk `fsync` on every write to its write-ahead log
before acknowledging a write — this makes **fsync latency**, not IOPS or MB/s
throughput, the binding constraint. The etcd FAQ says the p99 of `etcd_disk_wal_fsync_duration_seconds` should be under 10 ms and the p99 of
`etcd_disk_backend_commit_duration_seconds` under 25 ms; a slow disk is the most common cause of missed
heartbeats and spurious leader elections. The hardware page asks for about 50 sequential IOPS at minimum and
500 for heavily loaded clusters, and advises SSD. A network-attached disk with
occasional 50-100ms latency spikes (common on burst-limited cloud block storage, or
noisy shared NFS/SAN) is worse for etcd than a smaller but consistently-fast local
NVMe.
```bash
etcdctl check perf              # built-in latency check, run from an etcd node/peer
# or watch directly:
etcdctl --endpoints=<ep> endpoint status --write-out=table
# metrics: etcd_disk_wal_fsync_duration_seconds, etcd_disk_backend_commit_duration_seconds
```

## 2. What to actually provision
- Local SSD/NVMe on dedicated control-plane nodes where possible — this is the
  default recommendation precisely because network storage adds a hop of latency
  variance etcd is least tolerant of in the whole cluster.
- If network-attached storage is unavoidable (some managed/cloud control planes have
  no choice), pick the lowest-latency tier available and dedicate it — don't share
  the disk/IOPS budget with anything else on that node.
- Never put etcd data on the same disk as heavy log-writing or other noisy-neighbor
  workloads, even on otherwise-fast storage — contention shows up as fsync latency
  spikes, not capacity errors.

## 3. Quota and the suggested ceiling
etcd's backend has a space quota (`--quota-backend-bytes`) of 2 GiB by default; 8 GiB is the suggested maximum
for normal environments and etcd warns at startup if the configured value exceeds it. The etcd FAQ asks for at
least as much RAM as the quota, to avoid swapping or running out of memory. If a member's database exceeds the
quota, etcd raises a cluster-wide NOSPACE alarm and the cluster accepts only key reads and deletes (so no new
pods or scaling) until space is freed, the backend is defragmented and the alarm is cleared. Requests are also
capped at 1.5 MiB by default.

## 4. The two maintenance operations, and why both are needed
- **Compaction**: removes old key revisions beyond a retention window — reduces the
  *logical* keyspace etcd tracks, but doesn't shrink the on-disk file.
- **Defragmentation** (`etcdctl defrag`): reclaims the disk space freed by compaction. It applies only to the
  member it is sent to and blocks that member from reading and writing while it runs, so do one member at a time.
Kubernetes docs call defragmentation expensive, recommend running it as infrequently as possible while staying
under quota, and suggest the etcd-defrag tool (also runnable as a CronJob).

## Gotchas
- Kubernetes docs say taking a snapshot with `etcdctl snapshot save` does not affect member performance; it is
  a different thing from a Kubernetes `VolumeSnapshot` (kubeadm keeps etcd data in a hostPath directory on the
  control-plane node, not on a PV).
- `endpoint status` reporting `dbSize` close to quota with no recent compaction job
  is a predictable future outage, not a current one — alert on it before it's read-only.
- A control-plane node's root volume filling up (unrelated logs, images) can starve
  etcd's own disk I/O even if etcd's partition itself has room, if they share the
  same underlying device — isolate etcd's disk physically/logically where possible.

## Verify
- [ ] Checked `etcd_disk_wal_fsync_duration_seconds` (or `etcdctl check perf`) against
      the ~10ms guidance, not just assumed the disk is "fast enough."
- [ ] Confirmed compaction + defrag run on a schedule (automatic on managed control
      planes; explicit job on self-managed) and checked `dbSize` trend over time.
- [ ] Knows what happens (cluster-wide read-only) if quota is exceeded, and has a
      recovery plan rehearsed, not just a monitoring alert.
- [ ] Verified etcd's disk doesn't share I/O budget with noisy neighbors on the same
      control-plane node.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm source (kubernetes/kubernetes master).

Fixed: the FAQ guidance is WAL fsync p99 under 10 ms and backend commit p99 under 25 ms (the skill attributed 25 ms to fsync); the quota default is 2 GiB with 8 GiB a suggested maximum (etcd warns at startup above it) and the stated reason is that the machine should have at least as much RAM as the quota, not defrag or snapshot-transfer cost; a NOSPACE alarm puts the cluster into a maintenance mode that accepts only key reads and deletes (not fully read-only); Kubernetes docs say a snapshot does not affect member performance. Confirmed: hardware page (about 50 sequential IOPS minimum, 500 recommended for heavily loaded clusters, SSD advised, dedicated machines); `etcdctl check perf` exists; compaction does not shrink the file and defragmentation reclaims it; defragmentation is per member and blocks that member; Kubernetes docs recommend the etcd-defrag tool and a CronJob; kubeadm stores etcd data in a hostPath. Removed as unconfirmed: leader-last defrag ordering, claims about managed control planes handling maintenance, and "single most common incident".

Method: documentation only; no commands were run.
