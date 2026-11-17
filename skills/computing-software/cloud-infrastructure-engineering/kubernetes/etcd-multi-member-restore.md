---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-multi-member-restore
name: etcd-multi-member-restore
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd-restore, multi-member-restore, initial-cluster-token, etcdutl, snapshot-restore]
level: practitioner
status: docs-checked
description: "Restore a three-member etcd cluster from a single snapshot: per-member etcdutl restore with matching initial-cluster flags, new token, swap data dirs."
sources: ["https://etcd.io/docs/v3.6/op-guide/recovery/", "https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restoring a multi-member etcd cluster

All members must be restored from the SAME snapshot file; restoring one member and letting
the others sync from it does not work because restore creates a new cluster identity.

## 1. Stop the API servers and etcd on every control plane
```bash
sudo mv /etc/kubernetes/manifests/kube-apiserver.yaml /etc/kubernetes/manifests/etcd.yaml /root/
```

## 2. Restore on each member with its own name and peer URL
```bash
# on cp1 (repeat on cp2 and cp3 changing --name and --initial-advertise-peer-urls)
sudo etcdutl snapshot restore /backup/snap.db \
  --name cp1 \
  --initial-cluster cp1=https://10.0.0.11:2380,cp2=https://10.0.0.12:2380,cp3=https://10.0.0.13:2380 \
  --initial-cluster-token etcd-restore-20261018 \
  --initial-advertise-peer-urls https://10.0.0.11:2380 \
  --data-dir /var/lib/etcd-restored
```
`etcdctl snapshot restore` is deprecated in favour of `etcdutl` (etcd 3.6 restores only with `etcdutl`). A new
`--initial-cluster-token` prevents restored members accidentally talking to old ones.
For Kubernetes, etcd docs recommend adding `--bump-revision <n> --mark-compacted` so that revisions never go
backwards and watch caches are invalidated (choose `n` larger than the revisions written since the snapshot).
Names must match the `--name` in each node's etcd manifest.

## 3. Point each manifest at the new data dir
Edit `etcd.yaml`: change the `etcd-data` hostPath to `/var/lib/etcd-restored` (or swap the
directories: `mv /var/lib/etcd /var/lib/etcd.old && mv /var/lib/etcd-restored /var/lib/etcd`,
which avoids editing the manifest). Put `etcd.yaml` back on all three nodes, then
`kube-apiserver.yaml`.

## 4. Check
```bash
etcdctl ... member list -w table          # three members, all started
etcdctl ... endpoint status --cluster -w table   # same revision, one leader
kubectl get nodes; kubectl get pods -A
```

## Gotchas
- If you only restore a snapshot file copied from a member's data dir (`member/snap/db`),
  add `--skip-hash-check`.
- Do not start etcd on one node with the old data while others are restored; you get two
  clusters with diverging data.
- Objects created after the snapshot are gone. Kubernetes docs recommend restarting kube-scheduler,
  kube-controller-manager and the kubelets afterwards (see the post-restore checks).

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master); etcd mixin (etcd-io/etcd main); kube-prometheus-stack chart values (prometheus-community/helm-charts main).

Confirmed: all members restore from the same snapshot with `etcdutl snapshot restore` and per-member `--name`, `--initial-cluster`, `--initial-cluster-token`, `--initial-advertise-peer-urls` and `--data-dir`; restore overwrites member and cluster IDs so a new logical cluster results; `etcdctl snapshot restore` is deprecated in favour of `etcdutl`; `--skip-hash-check` is needed for a copy of `member/snap/db`; stop all API servers before restoring; move static pod manifests out of `/etc/kubernetes/manifests` to stop and restart them; the etcd data directory is changed through the `etcd-data` hostPath. Added: etcd's recommended `--bump-revision` and `--mark-compacted` options for Kubernetes restores and the recommendation to restart control-plane components and kubelets afterwards.

Method: documentation only; no commands were run.
