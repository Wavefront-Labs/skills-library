---
id: computing-software.systems-network-administration.proxmox-ve.qdevice-external-vote
name: qdevice-external-vote
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [qdevice, qnetd, corosync-qdevice, two-node-cluster, tie-breaker]
level: advanced
status: docs-checked
description: "Add an external QDevice vote to a two-node Proxmox VE cluster with corosync-qnetd and pvecm qdevice setup."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A QDevice is a daemon on each cluster node that casts votes according to an external arbitrator, so even-sized clusters survive more failures. Only QDevice Net (`corosync-qnetd`) is supported. It connects over TCP/IP, so it may sit outside the cluster LAN and does not need corosync's low latency. One qnetd host can serve several clusters and needs no config file.

Supported for clusters with an even number of nodes, and recommended for two-node clusters. For odd node counts it is discouraged: the QDevice then provides N-1 votes, so if qnetd fails no single node may fail, and a mass HA recovery could overload the last node.

Setup:

```
external# apt install corosync-qnetd
pve# apt install corosync-qdevice
pve# pvecm qdevice setup <QDEVICE-IP>
pve# pvecm status
```

Install `corosync-qdevice` on all nodes and keep them online. The setup copies the cluster SSH key to the QDevice host, so allow root key access (or temporary root password login). If you see `Host key verification failed.` run `pvecm updatecerts`. Status shows `Flags: Quorate Qdevice`, and per node columns A/NA (qnetd alive), V/NV (vote cast) and MW/NMW (master wins, default NMW). If NA, check TCP port 5403 on the external host.

Ties between equal partitions go to the one with the lowest node id; tune with `tie_breaker` (see `man corosync-qdevice`) and restart `corosync-qdevice.service` on all nodes. Before adding or deleting a cluster node, remove the QDevice with `pvecm qdevice remove`, then set it up again once the node count is even.

## Checked

2026-11-09. Compared with the External Vote Support (QDevice) section of https://pve.proxmox.com/pve-docs/chapter-pvecm.html; vote behaviour, port 5403, tie-break and node add or remove advice match.

Method: documentation only; no commands were run.

