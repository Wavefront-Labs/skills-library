---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-corruption-check-and-hashkv
name: etcd-corruption-check-and-hashkv
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, etcd-corruption-check, hashkv, data-integrity, etcd-operations]
level: practitioner
status: docs-checked
description: "Turn on etcd initial and periodic corruption checks, compare members with endpoint hashkv at one revision, and replace a member that diverged."
sources: ["https://etcd.io/docs/v3.6/op-guide/data_corruption/", "https://etcd.io/docs/v3.6/feature-gates/", "https://etcd.io/docs/v3.6/upgrades/upgrade_3_6/", "https://etcd.io/docs/v3.6/tasks/operator/how-to-check-cluster-status/", "https://github.com/kubernetes/kubernetes/blob/master/cmd/kubeadm/app/phases/etcd/local.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd corruption detection

## Enable the checks
etcd 3.5 flags (add to the etcd static pod or unit):
```
--experimental-initial-corrupt-check=true          # compare with peers during bootstrap
--experimental-corrupt-check-time=4h               # periodic latest-revision hash check (leader)
--experimental-compact-hash-check-enabled=true     # compacted-revision hash check (leader, every 1m by default)
```
In etcd 3.6 the experimental flags are deprecated: use the `InitialCorruptCheck` and `CompactHashCheck`
feature gates (`--feature-gates=InitialCorruptCheck=true,CompactHashCheck=true`) and `--corrupt-check-time` /
`--compact-hash-check-time`. Current kubeadm already starts local etcd with `InitialCorruptCheck=true`.

The initial check runs while a member bootstraps and the member exits on a mismatch. The periodic checks
run on the leader, which compares its state with the other members and raises a CORRUPT alarm on a
mismatch. The compacted-revision check is cheap but needs regular compaction; the latest-revision check
scans the whole keyspace at a revision, so etcd recommends a period of a couple of hours.

## Manual comparison
```bash
etcdctl endpoint hashkv --cluster --rev=<revision> -w table
```
All members must report the same hash for the same revision. Without `--rev`, members at
different revisions will differ legitimately.

```bash
etcdctl alarm list
```

## Fixing a diverged member
Identify the odd one out from the hashkv table, then use one of the three documented ways to restore a
corrupted member:
1. **Purge persistent state**: stop etcd, back up the data directory, move the `snap` subdirectory out of it,
   and start etcd with `--initial-cluster-state=existing` and the members in `--initial-cluster`; the
   member downloads an up-to-date snapshot from the leader.
2. **Replace the member**: stop etcd, back up and remove the data directory, `etcdctl member remove`,
   `etcdctl member add`, then start with `--initial-cluster-state=existing`.
3. **Restore the whole cluster**: save a snapshot from the leader and restore it to all members
   (see `etcd-backup-and-restore`).
After the member is restored the CORRUPT alarm can be removed (`etcdctl alarm disarm`).

## Causes worth chasing
Check the node for disk or filesystem errors, and read the release notes of your etcd version for
data-consistency fixes.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master).

Confirmed: `--experimental-initial-corrupt-check`, `--experimental-corrupt-check-time` and `--experimental-compact-hash-check-enabled` in the data corruption guide; in etcd 3.6 the `--experimental-` forms of the check-time flags are deprecated in favour of `--corrupt-check-time` and `--compact-hash-check-time`, and the initial and compact-hash checks became the `InitialCorruptCheck` and `CompactHashCheck` feature gates (both alpha, default false); the initial check makes a member exit on mismatch, the periodic checks run on the leader and raise a CORRUPT alarm; `etcdctl endpoint hashkv --cluster --rev` options; the three documented ways to restore a corrupted member; current kubeadm starts local etcd with `--feature-gates=InitialCorruptCheck=true`. Removed as unconfirmed: the jq revision pipeline, the claim that the cluster refuses writes on an alarm, the example alarm output, and the list of suspected causes.

Method: documentation only; no commands were run.
