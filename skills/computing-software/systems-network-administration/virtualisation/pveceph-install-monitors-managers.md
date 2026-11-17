---
id: computing-software.systems-network-administration.virtualisation.pveceph-install-monitors-managers
name: pveceph-install-monitors-managers
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pveceph, pveceph-install, ceph, ceph-mon, ceph-mgr, public-network, cluster-network, hyper-converged, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Deploy hyper-converged Ceph on Proxmox VE: hardware and network sizing, pveceph install/init, public vs cluster network, three monitors and managers, and dashboards."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#chapter_pveceph
  - https://github.com/proxmox/pve-docs/blob/master/pveceph.adoc
  - https://github.com/proxmox/pve-manager/blob/master/PVE/CLI/pveceph.pm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing Ceph on Proxmox VE: monitors and managers

**Goal:** a Ceph cluster inside the PVE cluster with enough monitors for quorum and
networks sized so recovery traffic does not starve VMs.

## Plan
- **3+ nodes** are the usual minimum for a hyper-converged Ceph cluster; leave headroom for recovery.
- Network: a Ceph **public** network (VM RBD and CephFS clients, and communication between Ceph services) is required; a separate **cluster** network for OSD replication and heartbeat traffic is optional. The guide recommends at least 10 Gbps used exclusively for Ceph, and separating Ceph traffic from the PVE cluster (corosync) network. A routed or broadcast full mesh is an option for three to five nodes without 10+ Gbps switch ports.
- Disks: the guide recommends SSDs or NVMe with power-loss protection for OSDs.
- RAM: OSD daemons need 4 GiB by default; the guide recommends at least 8 GiB per OSD for good performance (set with `ceph config set osd osd_memory_target 8G`).

## Install
```sh
pveceph install --repository no-subscription     # on every node (GUI: node -> Ceph)
pveceph init --network 10.60.0.0/24 --cluster-network 10.61.0.0/24   # once per cluster
pveceph mon create          # on each node that should run a monitor
pveceph mgr create          # on the monitor nodes; one manager is active, others standby
ceph -s
```
`pveceph install` sets up an apt repository (`/etc/apt/sources.list.d/ceph.sources`); `--repository` accepts `enterprise` (default), `no-subscription`, `test` or `manual`. `pveceph init` writes `/etc/pve/ceph.conf` and links it at `/etc/ceph/ceph.conf`; it is only needed once because pmxcfs distributes it.

## Monitors and managers
- Monitors keep the master copy of the cluster map; for high availability you need at least 3. A small or medium cluster does not need more than 3; only very large clusters need more.
- Multiple managers can exist but only one is active at a time; the guide recommends running managers on the monitor nodes. The manager handles features such as PG autoscaling and device health monitoring.

## Gotchas
- Most Ceph configuration lives in the central config database; read it with `ceph config dump` and change it with `ceph config set <who> <name> <value>`. A value in a local config file takes precedence.
- Use device classes and CRUSH rules to keep pools on the intended disk type.

## Verify
`ceph -s` shows `HEALTH_OK`, `mon: 3 daemons, quorum ...`, `mgr: active + standbys`;
`ceph mon stat` lists monitors on separate nodes.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09). pve-manager CLI source (PVE/CLI/pveceph.pm).

Confirmed: install flow (`pveceph install`, repository file, `--repository` enum), `pveceph init --network`, `/etc/pve/ceph.conf` with symlink, public versus cluster network descriptions, 10 Gbps recommendation, full-mesh note for three to five nodes, OSD memory (4 GiB default, 8 GiB recommended, `ceph config set osd osd_memory_target 8G`), monitor count (at least 3, no more than 3 for small to medium), manager behaviour, config database commands. `--cluster-network` is an option of `pveceph init` in the API source. Removed as unconfirmed: the 5-node and 25 GbE figures, the odd-number and 'more than 5 adds latency' statements, dashboard and Prometheus module commands, and the 'public network is painful to change' claim (the guide says only the cluster network can be moved later).

Method: documentation only; no commands were run.
