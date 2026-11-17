---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-snapshot-verification-and-restore-drills
name: etcd-snapshot-verification-and-restore-drills
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, etcdutl, snapshot-status, restore-drill, etcd-restore, disaster-recovery, game-day, backup-verification, rto, kind]
level: advanced
status: docs-checked
description: "Prove an etcd snapshot is restorable: etcdutl snapshot status, a scripted restore into a throwaway single-node etcd, and a quarterly full-cluster restore drill with a measured RTO."
sources: ["https://etcd.io/docs/v3.6/op-guide/recovery/", "https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/", "https://etcd.io/docs/v3.6/tasks/operator/how-to-save-database/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd snapshot verification and restore drills

**Goal:** a backup you have never restored is a hope, not a backup. Three levels of proof,
cheapest first, and a drill cadence that keeps the runbook honest.

## Level 1 — integrity check on every snapshot (seconds, automate it)
```bash
etcdutl snapshot status etcd-20261016T000000Z.db -w table
# +----------+----------+------------+------------+
# |   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
# | 7c1a9e3f | 18273645 |      41203 |     312 MB |
```
Checks: revision increases between consecutive snapshots (a flat revision means etcd is read-only
or you are snapshotting the wrong thing); TOTAL KEYS in the expected range (a cluster with 400
pods does not have 200 keys); size roughly stable. Fail the backup job if `snapshot status` errors.
(`etcdctl snapshot status` is deprecated; use `etcdutl`.)

## Level 2 — restore into a scratch etcd and read it (minutes, weekly in CI)
```bash
etcdutl snapshot restore etcd.db --data-dir /tmp/etcd-verify \
  --name verify --initial-cluster verify=http://127.0.0.1:12380 \
  --initial-advertise-peer-urls http://127.0.0.1:12380 --skip-hash-check=false
etcd --data-dir /tmp/etcd-verify --name verify \
  --listen-client-urls http://127.0.0.1:12379 --advertise-client-urls http://127.0.0.1:12379 \
  --listen-peer-urls http://127.0.0.1:12380 --initial-advertise-peer-urls http://127.0.0.1:12380 \
  --initial-cluster verify=http://127.0.0.1:12380 &
sleep 3
etcdctl --endpoints=http://127.0.0.1:12379 get /registry --prefix --keys-only | head
kill %1; rm -rf /tmp/etcd-verify
```
Seeing real keys proves the file is a usable etcd DB, not a truncated upload. `--keys-only` is enough
(stored values are ciphertext for resources covered by encryption at rest).

## Level 3 — full cluster restore drill (hours, quarterly, with a timer running)
1. Build a throwaway cluster with the **same** Kubernetes and etcd versions (kind or 1 VM with kubeadm).
2. Stop the API server (move `/etc/kubernetes/manifests/kube-apiserver.yaml` out), restore the
   snapshot with `etcdutl snapshot restore --data-dir /var/lib/etcd-restore`, point the etcd
   manifest's hostPath at it, put the apiserver manifest back.
3. Delete stale Node objects for nodes that don't exist, re-apply CNI if needed, then verify
   workloads: `kubectl get deploy -A`, Secrets decrypt (if KMS is used the drill cluster needs
   the same KMS key access), CRDs present, RBAC intact.
4. Record: time from "decision to restore" to "kubectl works" and to "app serves traffic".
   That is your real RTO; put it in the DR doc.

## What drills usually find
- Encryption-at-rest key not available on the restore target → every Secret unreadable.
- Restore target on a different etcd major.minor than the snapshot: Kubernetes docs only describe restores from
  snapshots taken by the same major.minor (a different patch release is fine).
- Restored cluster still lists Node objects and endpoints for machines that no longer exist.
- The person running the drill lacks bucket read permission in the DR account.

## Gotchas
- `--skip-hash-check` defaults to false for a snapshot taken by `etcdctl snapshot save`; set it to
  true only for a DB file copied straight out of `/var/lib/etcd/member/snap/db` (no trailing hash).
- Restore overwrites the member ID and cluster ID, so restored members form a new cluster and cannot rejoin the
  old one (etcd docs).
- Drill in a network-isolated environment: a restored cluster running old controllers can start
  reconciling real cloud resources (LBs, disks) via cloud-controller-manager.

## Verify
- [ ] Backup pipeline fails loudly when `etcdutl snapshot status` fails or revision is unchanged from the previous run.
- [ ] Weekly scratch restore job is green and logs the key count.
- [ ] Last full drill date, measured RTO and the list of findings are in the DR runbook, and each finding has an owner.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm source (kubernetes/kubernetes master).

Confirmed: `etcdutl snapshot status -w table` output columns HASH, REVISION, TOTAL KEYS and TOTAL SIZE and that `etcdctl snapshot status` is deprecated; `etcdutl snapshot restore` options and `--skip-hash-check` (an integrity hash exists only on snapshots from `snapshot save`); restore overwrites member and cluster IDs so a new cluster results; Kubernetes docs say restores are supported from snapshots of the same major.minor etcd version (a different patch version also works); losing the encryption key makes encrypted resources unrecoverable. Fixed: the claim that restoring a snapshot into a newer minor works is not in the docs and was replaced by the documented same-major.minor rule. Removed as unconfirmed: key-path examples under `/registry`, the CNI and kube-vip findings, and exit-code behaviour of `snapshot status`.

Method: documentation only; no commands were run.
