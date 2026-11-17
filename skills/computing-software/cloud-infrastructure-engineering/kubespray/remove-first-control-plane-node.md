---
id: computing-software.cloud-infrastructure-engineering.kubespray.remove-first-control-plane-node
name: remove-first-control-plane-node
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [control-plane, etcd, reorder, cluster-info, remove-node]
level: sme
status: docs-checked
description: "Remove the first kube_control_plane and etcd node: reorder the inventory, run an upgrade, remove it, edit the cluster-info configmap, then add a replacement."
sources:
  - https://kubespray.io/docs/operations/nodes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The first node in `kube_control_plane` and the etcd master list cannot be removed directly. The documented sequence:

1. Reorder the inventory so the first entry moves to any other position in all three groups (`kube_control_plane`, `kube_node`, `etcd`). To remove `node-1`, list `node-2`, `node-3`, `node-1` in each.
2. Run `upgrade-cluster.yml` or `cluster.yml`.
3. With the node still in the inventory, run `remove-node.yml -e node=node-1`. If it is offline, add `-e '{"reset_nodes": false, "allow_ungraceful_removal": true}'`.
4. Edit the `cluster-info` configmap in the `kube-public` namespace:

```
kubectl edit cm -n kube-public cluster-info
```

   Change the `server` field from the old control plane IP to a live control plane IP. Update `certificate-authority-data` too if you changed certs.
5. Update the inventory if needed, add the new control plane node and run `cluster.yml` with `--limit=kube_control_plane`.

## Checked

2026-11-04. The five steps and commands were confirmed on the page section Adding/Removal of first kube_control_plane and etcd-master. Unsupported explanations were removed.

Method: documentation only; no commands were run.
