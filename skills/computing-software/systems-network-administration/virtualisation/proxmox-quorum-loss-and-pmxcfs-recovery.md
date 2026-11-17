---
id: computing-software.systems-network-administration.virtualisation.proxmox-quorum-loss-and-pmxcfs-recovery
name: proxmox-quorum-loss-and-pmxcfs-recovery
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pmxcfs, pvecm-expected, quorum, etc-pve, read-only, config-db, proxmox-cluster, disaster-recovery, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Recover a Proxmox cluster that lost quorum: why /etc/pve goes read-only, pvecm expected, pmxcfs local mode, restoring config.db, and recovering guest configs."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pmxcfs.html
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
  - https://github.com/proxmox/pve-docs/blob/master/pmxcfs.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lost quorum and pmxcfs recovery

**Goal:** regain control of guests when too many nodes are down, without creating a split
brain.

## What happens without quorum
`/etc/pve` (pmxcfs, a FUSE filesystem backed by an SQLite database in `/var/lib/pve-cluster/config.db` and replicated via corosync) turns **read-only**: the cluster switches to read-only mode when it loses quorum, and guest startup (`pve-guests`) waits for quorum. With HA, a node that loses quorum while its LRM has active services is reset by its watchdog after 60 seconds.

## Temporary quorum on the survivors
Only if you are **certain** the missing nodes are down (powered off, not just partitioned):
```sh
pvecm status
pvecm expected 1        # sets the expected vote count to 1 and makes the cluster quorate
```
The documentation presents this for fixing `/etc/pve/corosync.conf` on a node without quorum, "if you understand what you are doing". If corosync cannot start at all, edit the local `/etc/corosync/corosync.conf` instead, and make sure all nodes end up with the same content to avoid split-brain.

## Local mode for a single node (no cluster comms)
```sh
systemctl stop pve-cluster
systemctl stop corosync
pmxcfs -l               # start the cluster file system in local mode
# ... fix configs ...
killall pmxcfs
systemctl start pve-cluster
```
This is the documented step for putting a node back to local mode (see the node-removal skill); use it for repairs only.

## Recover guest configs
The node directory that holds a guest config (`/etc/pve/nodes/<node>/qemu-server/<vmid>.conf`, `lxc/<vmid>.conf`) defines its owner, and a regular migration is impossible while the owning node is offline. HA-managed guests are recovered by the HA stack. A non-HA guest that has only shared disks (no local resources on the failed node) can be recovered by moving its config to an online node, as root on any member node:
```sh
mv /etc/pve/nodes/node1/qemu-server/100.conf /etc/pve/nodes/node2/qemu-server/
```
First make absolutely sure the failed node is really powered off or fenced, otherwise Proxmox VE's locking principles are violated. Guests with local disks cannot be recovered this way: wait for the node or restore from backup.

## Back up the cluster config
`/var/lib/pve-cluster/config.db` is the pmxcfs database. To move a lost host's configuration to a new Proxmox VE host (with nothing running): stop `pve-cluster`, replace `config.db` (permissions `0600`), adapt `/etc/hostname` and `/etc/hosts` to the lost host, reboot and check; guest data must be restored separately.

## Gotchas
- Making both sides of a network partition quorate (`pvecm expected 1` on each) risks split-brain, with two copies of a guest writing to shared storage; confirm power state first.
- Do not use these recovery methods to merge a node holding an old database into a running cluster; the documented recommendation for a node leaving a cluster is a reinstall.

## Verify
`pvecm status` shows the cluster quorate after recovery and each guest config exists under exactly one node directory.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, pvecm.adoc, last pushed 2026-10-17) and pmxcfs.adoc. Confirmed: read-only when quorum is lost; SQLite database `config.db` and FUSE basis; `pvecm expected 1` wording and the local-corosync.conf caveat; `pmxcfs -l` local mode and its stop/start sequence; the recovery and moving-guests procedure including both warnings; the config.db move procedure (0600, hostname and hosts); 60 s watchdog. Removed: the claim that running guests keep running, the sqlite3 backup command and daily-backup advice, the touch test, and the claim about restoring an old database onto a running cluster (not documented).

Method: documentation only; no commands were run.
