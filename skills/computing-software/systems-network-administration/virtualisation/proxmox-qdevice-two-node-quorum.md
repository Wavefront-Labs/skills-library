---
id: computing-software.systems-network-administration.virtualisation.proxmox-qdevice-two-node-quorum
name: proxmox-qdevice-two-node-quorum
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [qdevice, corosync-qnetd, corosync-qdevice, two-node-cluster, quorum, pvecm, proxmox-cluster, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Add an external QDevice (corosync-qnetd) to a two-node or even-node Proxmox cluster so one node failure keeps quorum; setup, placement and when not to use it."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
  - https://github.com/proxmox/pve-docs/blob/master/pvecm.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# QDevice for two-node Proxmox clusters

**Goal:** a two-node cluster (or any even count) that survives one node failure without
losing quorum and without manual `pvecm expected 1`.

## What it is
An external **corosync-qnetd** daemon on a third machine provides votes through the `corosync-qdevice` daemon on each cluster node, so a cluster can sustain more node failures than standard quorum rules allow. The documentation supports QDevices for clusters with an even number of nodes and recommends it for 2 node clusters that should have higher availability. Only QDevice Net is supported. The external host only needs network access to the cluster and a `corosync-qnetd` package (Debian-based hosts have one).

## Setup
```sh
# On the external machine (Debian-based):
apt install corosync-qnetd
# On ALL cluster nodes:
apt install corosync-qdevice
# Make sure all cluster nodes are online, then on one cluster node:
pvecm qdevice setup <qnetd-ip>
pvecm status          # shows the Qdevice with its vote
```
The cluster's SSH key is copied to the QDevice host automatically: set up key-based access for root on that host, or temporarily allow root login with a password during setup. If setup fails with 'Host key verification failed', run `pvecm updatecerts`. Remove with `pvecm qdevice remove`.

## Placement
- Run it on an independent external server, as an unprivileged user (the Proxmox and Debian package is already configured that way). Traffic between the daemon and the cluster is encrypted.
- The QDevice connects over TCP/IP, so it may sit outside the cluster LAN and is not bound by corosync's low-latency requirement. Ensure TCP port 5403 (the qnetd default) is reachable from the nodes.
- It must be able to see all nodes so it can choose one set of nodes to give its vote to.

## When not to use
- **Odd-numbered clusters:** Proxmox currently discourages QDevices there. The QDevice then provides N-1 votes (N = node count), so all but one node may fail, but if the QNet daemon itself fails no single node may fail without losing quorum, and a mass recovery of HA services can overload the last node; a Ceph server also stops providing services if only (N-1)/2 nodes or fewer remain.
- Clusters with HA where you would rather have a real third node.

## Gotchas
- To add or remove a cluster node you must remove the QDevice first, then set it up again once the node count is even.
- In a 2 node cluster with a QDevice (3 votes), a failed QDevice plus a failed node leaves one vote and no quorum; monitor the QDevice.
- `pvecm status` shows flags per node: `A`/`NA` (qnetd reachable or not), `V`/`NV` (will cast a vote), `MW`/`NMW` (master wins, default NMW), `NR` (not registered).
- On a tie between equal partitions that both see the QDevice, it gives its vote to the partition with the lowest node ID (tunable with `tie_breaker`, restart `corosync-qdevice.service` on all nodes).

## Verify
`pvecm status` lists the `Qdevice` with a vote and the flags `Quorate Qdevice`.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, pvecm.adoc, last pushed 2026-10-17). Confirmed: QDevice Net only, package names, setup and remove commands, key-copy requirement and `pvecm updatecerts` hint, TCP port 5403, TCP/IP transport and latency note, supported even-count and discouraged odd-count setups and their drawbacks, remove-before-add/remove-node rule, status flags, tie-breaking behaviour. Removed: the ffsplit/lms algorithm names, the certificate claim about moving the qnetd host, and the shutdown test (not documented).

Method: documentation only; no commands were run.
