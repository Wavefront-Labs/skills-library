---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-defragmentation-and-compaction
name: etcd-defragmentation-and-compaction
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, defrag, defragmentation, compaction, mvcc, db-size, quota-backend-bytes, no-space-alarm, etcdctl, dbstatus]
level: advanced
status: docs-checked
description: "Keep etcd's on-disk DB from hitting its space quota: MVCC compaction vs file-level defrag, alarm handling, and the rolling-defrag procedure that doesn't trip quorum."
sources: ["https://etcd.io/docs/v3.6/op-guide/maintenance/", "https://etcd.io/docs/v3.6/dev-guide/limit/", "https://etcd.io/docs/v3.6/op-guide/configuration/", "https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apiserver/pkg/storage/storagebackend/config.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd defragmentation and compaction

**Goal:** stop etcd from hitting `mvcc: database space exceeded` and going read-only,
without causing an outage while fixing it. This is routine maintenance, not disaster
recovery — pairs with
`computing-software.cloud-infrastructure-engineering.kubernetes.etcd-backup-and-restore`
for the actual DR path, and
`computing-software.cloud-infrastructure-engineering.kubernetes.etcd-cluster-membership-and-recovery`
for quorum-loss scenarios.

## 1. Why the DB grows even when the keyspace doesn't
- etcd is MVCC: every write creates a new revision, old revisions stay on disk until
  **compacted**. A cluster with high write churn (controllers re-writing status, lease
  renewals, HPA metrics-adjacent writes) can grow the DB file continuously even if the
  logical key count is flat.
- Compaction can be requested by kube-apiserver (`--etcd-compaction-interval`, default 5 minutes; 0 disables
  it) and by etcd itself (`--auto-compaction-mode` of `periodic` or `revision` plus
  `--auto-compaction-retention`, which defaults to 0 in the etcd 3.6 configuration reference). kubeadm does not set
  the etcd auto-compaction flags, so on a kubeadm cluster compaction normally comes from the API server;
  check which one is active instead of assuming.
- Compaction frees *logical* space (marks revisions deletable) but does **not** shrink
  the on-disk file — that's what defrag does. Skipping defrag after compaction is the
  most common reason DB size looks "stuck" despite compaction running.

## 2. Checking the numbers
```bash
etcdctl endpoint status --write-out=table --endpoints=https://127.0.0.1:2379 \
  --cacert=... --cert=... --key=...
```
Recent releases (the 3.6 downgrade guide's output) show `DB SIZE` (file size), `IN USE` (logical data),
`PERCENTAGE NOT IN USE` and `QUOTA`; older ones label the in-use column `DB SIZE IN USE`. A large gap between the two means compaction has freed space that defrag has not
reclaimed on disk yet.
- The default quota is 2 GiB (`--quota-backend-bytes`; 8 GiB is the suggested maximum and etcd warns at startup
  above it). kubeadm sets no quota flag, so the default applies. When a member's backend exceeds the quota,
  etcd raises a cluster-wide NOSPACE alarm and the cluster goes into a maintenance mode that accepts only key
  reads and deletes, until enough space is freed, the backend is defragmented and the alarm is cleared.

## 3. Defragment and clear a NOSPACE alarm
The etcd maintenance guide's recovery order is compact, defragment, then disarm:
```bash
etcdctl compact <current-revision>
etcdctl defrag --endpoints=https://<member-ip>:2379 --cacert=... --cert=... --key=...
etcdctl alarm list
etcdctl alarm disarm
```
- A defrag request is applied only to the member it is sent to and, on a live member, blocks reading and
  writing while the member rebuilds its state. The docs issue it per member to avoid cluster-wide latency
  spikes: defragment one member at a time and check `etcdctl endpoint health --cluster` between members.
  (`--cluster` finds all members automatically.)
- Kubernetes docs call defragmentation expensive: run it as infrequently as possible while keeping every member
  under quota, and suggest the third-party etcd-defrag tool, which can also run as a CronJob.
- Disarm only after space has been freed (compaction plus defrag); disarming without fixing the growth
  just delays the next alarm.

## 4. Preventing recurrence
- Confirm compaction is configured (API server interval or etcd flags, see section 1).
- Raise `--quota-backend-bytes` deliberately (and raise disk and IOPS alongside it, staying at or under the
  8 GiB suggestion) rather than as a reaction to an active alarm.
- Watch `etcd_mvcc_db_total_size_in_bytes` against `etcd_server_quota_backend_bytes`. The etcd mixin alerts
  `etcdDatabaseQuotaLowSpace` at 95 percent of quota (critical) and `etcdExcessiveDatabaseGrowth` on a four hour
  linear prediction; add an earlier warning of your own.
- A workload writing excessively (a controller re-patching status every second) is a more common root cause
  than genuine growth; look at the `etcd_mvcc_put_total` rate and at `etcd_request_duration_seconds` from the
  API server before assuming that more quota is the fix.

## Gotchas
- Defrag against a member serving heavy traffic is felt as stalled reads and writes on that member while it
  runs; schedule it in a quiet window.
- Compact before defrag: defragmentation can only return space that compaction has already released.

## Verify
- [ ] `etcdctl endpoint status` on every member shows `IN USE` tracking close
      to `DB SIZE`, not a persistent large gap.
- [ ] `etcdctl alarm list` is empty on all members.
- [ ] A Prometheus alert fires well before DB size reaches `quota-backend-bytes`.
- [ ] Defrag has been run as a rolling, one-member-at-a-time procedure, with
      `endpoint health` checked between members, not as a single all-member blast.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master); etcd mixin (etcd-io/etcd main); kube-prometheus-stack chart values (prometheus-community/helm-charts main).

Fixed: a NOSPACE alarm puts the cluster into a maintenance mode that still accepts key reads and deletes (the skill said every write including deletes fails); kube-apiserver, not etcd, performs the default 5 minute compaction (`--etcd-compaction-interval`, DefaultCompactInterval = 5 minutes in the apiserver source) and kubeadm does not set `--auto-compaction-*` or `--quota-backend-bytes` on local etcd (kubeadm source); etcd 3.6 `endpoint status` output in the downgrade guide shows the columns DB SIZE, IN USE, PERCENTAGE NOT IN USE and QUOTA (older releases label the in-use column DB SIZE IN USE). Confirmed: default quota 2 GiB with 8 GiB as the suggested maximum and a startup warning above it; defragmentation is per member, is not replicated, and blocks reads and writes on that member; the compact, defrag, alarm disarm sequence; `--auto-compaction-mode` periodic or revision; the metrics `etcd_mvcc_db_total_size_in_bytes` and `etcd_server_quota_backend_bytes`; Kubernetes docs recommend the third-party etcd-defrag tool. Removed as unconfirmed: leader-last defrag ordering, NOSPACE blocking defrag in some versions, and rates by key prefix.

Method: documentation only; no commands were run.
