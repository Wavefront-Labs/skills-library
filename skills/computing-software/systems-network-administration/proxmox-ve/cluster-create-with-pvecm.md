---
id: computing-software.systems-network-administration.proxmox-ve.cluster-create-with-pvecm
name: cluster-create-with-pvecm
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [cluster, pvecm-create, cluster-name, link0, corosync-links]
level: practitioner
status: docs-checked
description: "Create a Proxmox VE cluster with pvecm create, choosing a name and network links before any node joins."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: nodes reach each other on UDP ports 5405-5412 (corosync) and TCP 22 (SSH), clocks are synchronized, all nodes run the same version, and the root password is available when adding nodes. Use at least three nodes for reliable quorum, or two plus a QDevice. Install each node with its final hostname and IP: they cannot be changed after cluster creation. The cluster name cannot be changed either and follows the node name rules. Clusters in the same network need unique names.

Create the cluster on the first node (console or Datacenter, Cluster, Create Cluster):

```
pvecm create CLUSTERNAME
pvecm status
```

By default link 0 uses the address the node hostname resolves to. Use a dedicated NIC for corosync: it needs low latency, not bandwidth, so a dedicated 1 Gbit NIC is enough. Do not choose a network used for storage or live migration. Up to 8 links are supported; add redundancy at creation:

```
pvecm create CLUSTERNAME --link0 10.10.10.1,priority=15 --link1 10.20.20.1,priority=20
```

The link with the higher `priority` value carries the traffic; equal or unset priorities fall back to the lowest link number. Only the top-priority link sees corosync traffic while it works.

Cluster state is stored in pmxcfs under `/etc/pve`, replicated through corosync. The cluster's latency requirement is under 5 ms between nodes, and the Proxmox firewall adds the corosync ACCEPT rules automatically.

## Checked

2026-11-03. Commands, option names, defaults, limits and behaviour claims were compared with the official Proxmox VE documentation pages: https://pve.proxmox.com/pve-docs/chapter-pvecm.html (plus the chapter-qm, qm.1, pct, pvecm, pvesm, vzdump, pvesr and sysadmin pages). Items shown as placeholder or example values (file names, VM IDs, device names) are illustrative. Figures that the pages did not state were removed or reworded.

Method: documentation only; no commands were run.
