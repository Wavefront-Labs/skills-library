---
id: computing-software.systems-network-administration.virtualisation.proxmox-ceph-public-and-cluster-network-design
name: proxmox-ceph-public-and-cluster-network-design
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ceph-cluster-network, ceph-public-network, ceph, proxmox, network-design]
level: advanced
status: docs-checked
description: "Design Proxmox VE Ceph networks: public vs cluster network, bandwidth and MTU, separation from corosync, full-mesh options and changing networks later."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pve_ceph_install_wizard
  - https://docs.ceph.com/en/latest/rados/configuration/network-config-ref/
  - https://github.com/proxmox/pve-docs/blob/master/pveceph.adoc
  - https://github.com/ceph/ceph/blob/main/doc/rados/configuration/network-config-ref.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ceph public and cluster network design on Proxmox VE

**Goal:** Ceph traffic that does not starve guests or corosync, and survives a link failure.

## Two networks
- **public_network**: monitors, managers, clients (VM RBD/QEMU, CephFS mounts) talk to OSDs here.
- **cluster_network** (optional): OSD replication and heartbeat traffic. A physically separate network relieves the public and guest networks and brings significant performance improvement, per the guide.
```bash
pveceph init --network 10.10.10.0/24 --cluster-network 10.10.20.0/24
```
Written to `/etc/pve/ceph.conf` (`public_network`, `cluster_network`).

## Sizing
- The guide recommends at least 10 Gbps used exclusively for Ceph, or more; a few HDD OSDs per node can already saturate 10 Gbps, and a single NVMe SSD can too. Take recovery time into account, especially on small clusters.
- Prefer redundant links; see the Proxmox network chapter for bonding modes (`bond-mode`, `bond-xmit-hash-policy`) and verify your switch supports the mode.
- Use jumbo frames only if every NIC, bond, bridge and switch port agrees on the MTU.

## Corosync is separate
The guide recommends separating Ceph traffic from the PVE cluster (corosync) network, because Ceph's high-bandwidth I/O can interfere with low-latency services such as corosync. Give corosync its own link, plus a redundant link.

## Small clusters: full mesh
A meshed network is an option for three to five node clusters if there are no 10+ Gbps switch ports; see the Proxmox wiki page *Full Mesh Network for Ceph Server*.

## Changing networks later
The guide says the Ceph cluster network can be moved to another physically separated network later. For the public network, follow the Ceph documentation for changing monitor addresses before attempting it; plan addresses up front.

## Verify
`/etc/pve/ceph.conf` shows the intended `public_network` and `cluster_network`; `ceph config dump` and `ceph -s` look healthy after a recovery test.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09). Ceph documentation sources (ceph/ceph, doc/ directory, master).

Confirmed: public network (client and inter-service traffic, required) and cluster network (OSD replication and heartbeat, optional), the cluster-network recommendation and that it can be moved later, `pveceph init --network ... --cluster-network ...`, `/etc/pve/ceph.conf` and `public_network`/`cluster_network` option names, the 10 Gbps recommendation and saturation remarks, separation from corosync, full-mesh option for three to five nodes. Removed as unconfirmed: the 'doubles usable client bandwidth' claim, 25 GbE sizing, LACP/MLAG advice and `ping -M do -s 8972` MTU test, the routed-mesh implementation details, the monitor re-creation procedure for changing the public network and the rolling OSD restart claim, and the `ss`/`iperf3` verification commands.

Method: documentation only; no commands were run.
