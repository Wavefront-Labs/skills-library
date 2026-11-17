---
id: computing-software.cloud-infrastructure-engineering.talos-linux.control-plane-quorum-and-bootstrap
name: control-plane-quorum-and-bootstrap
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [control-plane, etcd, quorum, bootstrap, scaling, high-availability, talosctl-bootstrap]
level: practitioner
status: docs-checked
description: "Control plane sizing and lifecycle on Talos: etcd quorum maths (3 or 5 nodes), one-time bootstrap, scale down via reset, and why an upgrade equals scale-down then scale-up."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/learn-more/control-plane.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nodes with `.machine.type` of `controlplane` run etcd, kube-apiserver, kube-controller-manager and kube-scheduler. Check membership with `talosctl get member`. They are tainted by default so workloads are not scheduled on them.

**Quorum.** etcd needs a majority for any read or write. Two control plane nodes are worse than one (either failing locks the database); four are worse than three (quorum needs 3 of 4 versus 2 of 3). Run three or five. Five tolerates two simultaneous failures but costs hardware, and write throughput drops about 5% versus three. If etcd is slow, scale the nodes vertically, not horizontally.

**Replacing nodes.** Failed node: remove it first, then add the replacement (the dead node must not vote). Healthy node: add the new one, then remove the old.

**Bootstrap.** Done once per cluster against one control plane node with `talosctl bootstrap`. It only tells etcd to form a cluster; it does not start Kubernetes. If the bootstrap call returned successfully but Kubernetes fails for other reasons (bad config, unreachable registry), do not bootstrap again; fix the config. Flow: etcd starts, kubelet starts, control plane static pods are rendered and started, bootstrap manifests (join token, kubelet CSR auto-approval, CNI) are injected under an etcd mutex, then other etcd members discover each other through the Kubernetes `Endpoints` resource. After this the bootstrap node has no special role.

**Scale down:** `talosctl -n IP.of.node.to.remove reset`, then `kubectl delete node`. Reset makes the node leave etcd and erases its disks.

**Upgrade:** the node leaves etcd, wipes the system disk, installs the new version and rejoins, which equals scale-down followed by scale-up.

## Checked

2026-11-04. Control Plane page confirms quorum reasoning, recommendations, bootstrap steps and the reset and upgrade behaviour for control plane nodes.

Method: documentation only; no commands were run.
