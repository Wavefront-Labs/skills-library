---
id: computing-software.cloud-infrastructure-engineering.kubespray.add-or-remove-etcd-node
name: add-or-remove-etcd-node
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [etcd, scale, odd-quorum, kube-apiserver, etcd-retries]
level: sme
status: docs-checked
description: "Add or remove an etcd member while keeping an odd count: cluster.yml and upgrade-cluster.yml with ignore_assert_errors, etcd_retries, and --etcd-servers in kube-apiserver.yaml."
sources:
  - https://kubespray.io/docs/operations/nodes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Keep an odd number of etcd nodes at all times, so every change is a replacement or scale-up: add two nodes or remove one.

**Adding**
1. Update the inventory and run `cluster.yml` with `--limit=etcd,kube_control_plane -e '{"ignore_assert_errors": true}'`. A node that is already a worker or control plane node must first be removed with `remove-node.yml`.
2. Run `upgrade-cluster.yml` with the same limit and flag, so that all etcd configuration in the cluster is updated.
3. If you add several etcd nodes in one run, append `-e etcd_retries=10`; otherwise later joins may fail while the first is still processing. That value might work for 3 new nodes.
4. On every control plane node, edit `/etc/kubernetes/manifests/kube-apiserver.yaml` and make sure the new nodes appear in `--etcd-servers=...`.

**Removing**
1. Run `remove-node.yml -e node=NODE_NAME` (with the offline flags `reset_nodes` false and `allow_ungraceful_removal` true if it is down).
2. Remove the node from the inventory.
3. Run `cluster.yml` to regenerate configuration on remaining nodes.
4. Edit `kube-apiserver.yaml` on each control plane node so only active members remain in `--etcd-servers=...`.
5. Shut down the old instance.

Mid-procedure the member count is even; the page says apps should stay available unless a leader election happens then.

## Checked

2026-11-04. Both procedures were confirmed on the Adding an etcd node and Removing an etcd node sections of the Adding/replacing a node page.

Method: documentation only; no commands were run.
