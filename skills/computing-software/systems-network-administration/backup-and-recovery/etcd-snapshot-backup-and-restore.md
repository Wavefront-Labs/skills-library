---
id: computing-software.systems-network-administration.backup-and-recovery.etcd-snapshot-backup-and-restore
name: etcd-snapshot-backup-and-restore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [etcd-snapshot, etcd, kubernetes, etcdctl, etcdutl, database-backup]
level: advanced
status: docs-checked
description: "Back up and restore Kubernetes etcd: etcdctl snapshot save with TLS, etcdutl status and restore to a new data dir, kubeadm static pod changes, k3s/RKE2 commands, and keys to keep."
sources:
  - https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/
  - https://etcd.io/docs/v3.5/op-guide/recovery/
  - https://docs.k3s.io/cli/etcd-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd snapshot backup and restore

**Goal:** a restorable etcd snapshot so a broken control plane can be rebuilt with all cluster state.

## Save (kubeadm cluster, on a control-plane node)
```sh
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /backup/etcd-$(date +%F-%H%M).db
etcdutl snapshot status /backup/etcd-2026-10-17-0200.db -w table   # hash, revision, keys, size
```
Copy off the node. Also back up `/etc/kubernetes/pki` and keep a secure backup of the API server's encryption-at-rest key if you use one; the Kubernetes documentation warns that if you lose all copies of the key you must delete the resources that were encrypted under it.

## Restore (kubeadm)
1. Stop the API server and etcd: move manifests out of `/etc/kubernetes/manifests/` on every control-plane node.
2. Restore the **same snapshot** on each member into a new data dir:
```sh
etcdutl snapshot restore /backup/etcd.db --data-dir /var/lib/etcd-restore \
  --name cp1 --initial-cluster cp1=https://10.0.0.11:2380,cp2=https://10.0.0.12:2380,cp3=https://10.0.0.13:2380 \
  --initial-advertise-peer-urls https://10.0.0.11:2380
```
3. Point `etcd.yaml` hostPath `etcd-data` at `/var/lib/etcd-restore` (or replace `/var/lib/etcd`), move manifests back.
4. Restart kubelet; check `kubectl get nodes` and `etcdctl endpoint health --cluster`.

## k3s / RKE2
```sh
k3s etcd-snapshot save --name manual          # on-demand; scheduled snapshots are on by default (every 12 h, 5 kept per server node) and tuned with --etcd-snapshot-schedule-cron and --etcd-snapshot-retention
k3s server --cluster-reset --cluster-reset-restore-path=/var/lib/rancher/k3s/server/db/snapshots/<file>
```
RKE2 uses `rke2 etcd-snapshot save` and the same reset flags.

## Gotchas
- `etcdctl snapshot status` and `etcdctl snapshot restore` have been deprecated since etcd 3.5.x (the Kubernetes docs say they were slated for removal in 3.6); use `etcdutl`. A snapshot taken with `etcdctl snapshot save` carries an integrity hash checked at restore; a copy of the data directory has none and needs `--skip-hash-check`.
- A restore rolls the whole cluster back; workloads created after the snapshot vanish, and controllers reconcile to old state. Velero/GitOps covers app-level restore better.
- Snapshot from one member only; never mix snapshots across members.

## Verify
Restore the snapshot into a throwaway single-node etcd and list keys (`etcdctl get / --prefix --keys-only | head`) monthly.

## Checked

Checked 2026-10-27 against the Kubernetes website sources (kubernetes/website: configure-upgrade-etcd and encrypt-data), the etcd v3.6 recovery guide (etcd-io/website), the K3s etcd-snapshot documentation (k3s-io/docs) and the RKE2 backup and restore page (rancher/rke2-docs). Confirmed: `etcdctl snapshot save` with the kubeadm certificate flags, `etcdutl snapshot status` and `etcdutl snapshot restore` with `--data-dir`, `--name`, `--initial-cluster` and `--initial-advertise-peer-urls`, restoring the same snapshot on every member, the deprecation of the etcdctl status and restore subcommands, the integrity-hash and `--skip-hash-check` behaviour, `k3s etcd-snapshot save --name`, default scheduled snapshots and retention, `--cluster-reset` with `--cluster-reset-restore-path`, and `rke2 etcd-snapshot save` with the same reset flags. The kubeadm manifest and `etcd-data` hostPath steps follow the Kubernetes restore text.

Method: documentation only; no commands were run.
