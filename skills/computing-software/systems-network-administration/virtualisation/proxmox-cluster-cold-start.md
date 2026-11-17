---
id: computing-software.systems-network-administration.virtualisation.proxmox-cluster-cold-start
name: proxmox-cluster-cold-start
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [cluster-cold-start, proxmox-cluster, pve-ha, ceph-noout, startup-order, power-outage, proxmox]
level: advanced
status: docs-checked
description: "Shut down and cold start a whole Proxmox VE cluster with HA and Ceph safely: order, Ceph flags, HA behaviour on full shutdown, guest startup order and checks."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html#_cluster_cold_start
  - https://pve.proxmox.com/pve-docs/chapter-pveceph.html
  - https://pve.proxmox.com/pve-docs/chapter-ha-manager.html
  - https://pve.proxmox.com/pve-docs/chapter-qm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Full cluster shutdown and cold start

Planned power work or a DC move. Goal: no fencing, no Ceph rebalancing storm, guests come
back in dependency order.

## Prepare
- Guest startup order: Options → Start at boot (`onboot`), Start/Shutdown order, Startup delay and Shutdown timeout (default 180 s). A lower order starts first and is shut down last; equal orders sort by VMID. Infra first (DNS/DHCP, AD, DB), apps after. HA-managed guests do not follow these settings; their state follows HA.
- HA: powering down an HA guest through the Proxmox VE tooling sets its state to `stopped`, and it returns to `started` when it is powered on again. The node shutdown policy is `ha: shutdown_policy=` in `datacenter.cfg`.
- Pause backup and replication jobs so nothing starts mid-shutdown.

## Shutdown order
1. Stop all Ceph clients first: VMs and containers, and anything using CephFS or RADOS GW.
2. Ceph: verify health, then prevent recovery during the shutdown and power-on phases:
   ```sh
   ceph -s
   ceph osd set noout
   ```
3. Power down the nodes without a monitor (MON) first, then the nodes with monitors.

## Cold start
1. Power on network and storage first, then the PVE nodes, starting those with Ceph monitors. Some nodes boot faster than others; the `pve-guests` service waits for quorum and then starts all guests with the `onboot` flag, so guest startup is delayed until the cluster is quorate.
2. `pvecm status` quorate; confirm all Ceph services are up.
3. The only Ceph warning left should be that `noout` is set; clear it:
   ```sh
   ceph osd unset noout
   ```
4. Start the guests; HA guests change their state to `started` when they power on (set HA resources back to `started` yourself if you stopped them).
5. Re-enable backup and replication jobs.

## Gotchas
- A UPS avoids the all-nodes-down state after a power failure, especially with HA.
- Do not start guests before the Ceph flag is cleared and Ceph is healthy.
- A node that never comes back leaves HA services assigned to it in the `fence` state until fencing completes, after which they are recovered elsewhere.

## Verify
All HA resources `started`, `ceph -s` healthy, application smoke tests pass, jobs enabled.

## Checked

Checked 2026-10-25 against pve-docs master (pvecm.adoc, pveceph.adoc, qm.adoc, ha-manager.adoc; last pushed 2026-10-17). Confirmed: cold-start behaviour of `pve-guests` and `onboot`; the documented Ceph HCI shutdown and power-on procedure (`ceph -s`, `noout`, monitor node order); start/shutdown order, startup delay and 180 s shutdown timeout semantics and the HA exemption; HA guest state changes on power down and up. Removed: the extra Ceph flags (`norebalance`, `norecover`, `nobackfill`, `nodown`, `pause`) and the claim that guests hang on I/O with `pause` (the Proxmox VE procedure sets only `noout`), and the claim that nodes must boot within a few minutes of each other.

Method: documentation only; no commands were run.
