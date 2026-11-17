---
id: computing-software.systems-network-administration.virtualisation.proxmox-replication-failover-after-node-loss
name: proxmox-replication-failover-after-node-loss
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [replication-failover, pvesr, storage-replication, pve-ha, zfs, proxmox]
level: advanced
status: docs-checked
description: "Recover guests on a surviving Proxmox node from ZFS storage replication after a node failure: HA or manual config move, data-loss window, and rebuilding replication after."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvesr.html
  - https://pve.proxmox.com/pve-docs/chapter-ha-manager.html
  - https://github.com/proxmox/pve-docs/blob/master/pvesr.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Failover with pvesr storage replication

pvesr replicates local ZFS volumes to other nodes on a schedule (default every 15 minutes).
After a node dies, the replica is as old as the last successful sync: **data written
since then is lost** (RPO = schedule interval plus sync time).

## With HA configured
For guests managed by the HA stack, see the HA chapter of the admin guide (`ha-manager`); the replication chapter does not describe how HA picks a replica node, so check that behaviour in your release before relying on it. Keep replication targets and HA node choices consistent.

## Manual recovery (no HA)
Cluster still quorate, node `pve01` dead, replica on `pve02`:
1. Confirm `pve01` is really down (powered off via IPMI): two nodes running the same VM
   on diverging disks is worse than downtime.
2. Move the config (pmxcfs allows this while the owner is offline):
   ```sh
   pvecm status            # confirm quorum first
   mv /etc/pve/nodes/pve01/qemu-server/101.conf /etc/pve/nodes/pve02/qemu-server/101.conf
   ```
   For a container move `/etc/pve/nodes/pve01/lxc/<CTID>.conf` the same way.
3. Start on `pve02`: `qm start 101` (containers: `pct start <CTID>`). The replicated volumes already exist there.
4. Use the replication log or `pvesr status` to state the time of the last successful sync, which is your data loss window.

If there is no quorum, fix that first. Only if that is not possible, `pvecm expected 1` forces quorum on the current node; avoid cluster-affecting changes (adding or removing nodes, storages or guests) while expected votes are overridden.

## After the failed node returns
- The guest configuration was moved, so the returning node will not start the old copy, but its local ZFS still holds stale volumes of that guest.
- Replication jobs run from the node that now owns the guest; the direction switches automatically when a guest is migrated to a node it replicates to.
- Failed jobs enter an error state and are retried every 30 minutes; check the replication log for the cause (network, no space on the target, storage ID missing on the target node). Do not delete volumes on either side until you have verified which copy is current.

## Gotchas
- Replication needs the **same storage ID** (ZFS) on both nodes.
- Only ZFS volumes replicate; the replication chapter lists `zfspool` as the supported plugin.
- A shorter schedule reduces the loss window but adds I/O load.

## Verify
`pvesr status` shows OK and recent last-sync for all jobs; quarterly test: shut down a
node and recover one test VM using the steps above, record achieved RPO/RTO.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09).

Confirmed in the replication chapter ("Migrating a guest in case of Error"): check quorum with `pvecm status`, `pvecm expected 1` only as a last resort with the warning about cluster-affecting changes, move the guest config files between `/etc/pve/nodes/<node>/qemu-server` and `/lxc`, then `qm start` or `pct start`; default 15-minute interval; error state with 30-minute retries and the common causes; automatic direction switch on migration; supported plugin zfspool. Removed as unconfirmed: the HA recovery description (the HA chapter does not mention replication), the `__replicate_` snapshot grep, the "conflicting snapshot" cleanup with `zfs destroy`, and the claim that failed jobs are silent without notifications.

Method: documentation only; no commands were run.
