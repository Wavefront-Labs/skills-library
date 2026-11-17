---
id: computing-software.cloud-infrastructure-engineering.kubespray.inventory-groups-and-membership
name: inventory-groups-and-membership
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [inventory, groups, kube-control-plane, kube-node, etcd, k8s-cluster]
level: intro
status: docs-checked
description: "Define a Kubespray inventory from the kube_control_plane, kube_node and etcd groups, decide which hosts are schedulable, and know what k8s_cluster, calico_rr and bastion mean."
sources:
  - https://kubespray.io/docs/ansible/inventory.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The inventory has three groups: `kube_node` (hosts where pods run), `kube_control_plane` (apiserver, scheduler, controller) and `etcd` (the etcd servers; at least 3 for failover).

Membership decides scheduling:
- A host in both `kube_control_plane` and `kube_node` acts as control plane and worker.
- A host only in `kube_control_plane` is a standalone, unschedulable control plane.
- When `kube_node` contains the `etcd` hosts, the etcd cluster is schedulable for workloads. For a standalone etcd, make sure the groups do not intersect.

Two special groups exist: `calico_rr` (route reflectors for advanced Calico networking) and `bastion`. `k8s_cluster` is not written by hand: it is dynamically the union of `kube_node`, `kube_control_plane` and `calico_rr`, and is what whole-cluster variables under `<inventory>/group_vars/k8s_cluster/*.yml` attach to.

The page's complete example sets `ansible_host` for the SSH address and `ip` to bind Kubernetes services on a different address than the default interface:

```ini
node1 ansible_host=95.54.0.12 ip=10.3.0.1
node2 ansible_host=95.54.0.13 ip=10.3.0.2

[kube_control_plane]
node1
node2

[etcd]
node1
node2
node3

[kube_node]
node2
node3
```

For customisation, see the Customize Ansible vars section of the Ansible page.

## Checked

2026-11-04. Both the group definitions and the example were confirmed on the Inventory page of the Kubespray docs; the abbreviated example here keeps its first two nodes and trims the rest.

Method: documentation only; no commands were run.
