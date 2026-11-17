---
id: computing-software.cloud-infrastructure-engineering.talos-linux.rook-ceph-on-talos
name: rook-ceph-on-talos
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [rook, ceph, csi, helm, osd, storage, talos-upgrade, disk-wipe]
level: advanced
status: docs-checked
description: "Deploy Ceph with Rook on Talos: spare-disk prerequisites, the three Helm installs, privileged namespace label, mon quorum workaround, safe upgrades and disk wipe cleanup."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/kubernetes-guides/csi/ceph-with-rook.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Ceph does its storage work in OSDs, one per disk, so every spare disk becomes an OSD. Talos reserves a whole disk for the OS, so each storage node needs an additional unused disk with no partitions or filesystems. Rook runs 3 mons by default, one per node, and control plane nodes are tainted against them, so plan at least 3 workers. Helm v3 is required.

Install in three parts:

```bash
helm repo add rook-release https://charts.rook.io/release
helm install --create-namespace --namespace rook-ceph rook-ceph rook-release/rook-ceph
kubectl label namespace rook-ceph pod-security.kubernetes.io/enforce=privileged
helm repo add ceph-csi-operator https://ceph.github.io/ceph-csi-operator/
helm install --create-namespace --namespace rook-ceph ceph-csi-drivers ceph-csi-operator/ceph-csi-drivers
helm install --create-namespace --namespace rook-ceph rook-ceph-cluster --set operatorNamespace=rook-ceph rook-release/rook-ceph-cluster
```

With fewer than 3 non-control-plane nodes, creation stalls on `cannot start 3 mons on 2 node(s) when allowMultiplePerNode is false`. `helm upgrade --set` fails with a field-ownership conflict, so patch the resource (Helm values will drift):

```bash
kubectl -n rook-ceph patch cephcluster rook-ceph --type merge -p '{"spec":{"mon":{"allowMultiplePerNode":true}}}'
```

Verify with `kubectl --namespace rook-ceph get cephcluster rook-ceph --watch`. Status can lag, so also read `kubectl -n rook-ceph logs deploy/rook-ceph-operator --tail=30` and look for real OSD pods: `kubectl -n rook-ceph get pods -l app=rook-ceph-osd`. The storage classes (`ceph-block`, `ceph-bucket`, `ceph-filesystem`) exist from install time and do not prove health.

Talos upgrades: upgrade one node at a time with `talosctl upgrade --nodes <node-ip> --image ghcr.io/siderolabs/installer:<talos-version>`, proceeding only when `HEALTH_OK`, and wait between nodes:

```bash
kubectl --namespace rook-ceph wait --timeout=1800s --for=jsonpath='{.status.ceph.health}=HEALTH_OK' cephclusters.ceph.rook.io rook-ceph
```

Cleanup: patch `cleanupPolicy.confirmation` to `yes-really-destroy-data`, delete storage classes and Ceph objects, delete the cephcluster, uninstall the charts, then clear leftovers on each node's `dataDirHostPath` (default `/var/lib/rook`) with a privileged busybox pod and wipe disks with `talosctl wipe disk <device> -n <node-ip>`.

## Checked

2026-11-04. Prerequisites, install commands, mon workaround, upgrade gating and cleanup steps confirmed on the Ceph with Rook page.

Method: documentation only; no commands were run.
