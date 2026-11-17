---
id: computing-software.systems-network-administration.virtualisation.proxmox-cluster-node-removal
name: proxmox-cluster-node-removal
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pvecm-delnode, node-removal, pvecm, proxmox-cluster, separate-node, reinstall-node, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Remove a node from a Proxmox VE cluster safely with pvecm delnode, clean leftover config and SSH keys, separate a node without reinstalling, and rejoin a rebuilt node."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
  - https://github.com/proxmox/pve-docs/blob/master/pvecm.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Removing or re-adding a Proxmox cluster node

**Goal:** take a node out of the cluster permanently (or rebuild it) without disturbing
quorum or leaving ghosts in the configuration.

## Standard removal (node will be wiped or reinstalled)
1. Move all VMs and containers off the node. If a QDevice is configured, remove it first (`pvecm qdevice remove`). If the node is part of Ceph: destroy its OSDs one after another, wait for `HEALTH_OK`, destroy any metadata server (`pveceph mds destroy <node>`), monitor and manager, then remove the empty host bucket (`ceph osd crush remove <node>`).
2. **Power off the node** and make sure it does not power on again in this network with its current configuration; otherwise the cluster could end up broken and hard to restore.
3. On a remaining node:
```sh
pvecm nodes
pvecm delnode <nodename>
pvecm status
```
The error `could not kill node (error = cs_err_not_exist)` only means corosync failed to kill an offline node and can be ignored.
4. Clean leftovers: the directory `/etc/pve/nodes/<nodename>` (recover any configuration you need first), the node from any HA rules that still reference it, and its public key in `/etc/pve/priv/authorized_keys`. Its SSH fingerprint stays in `known_hosts` on the other nodes: if you get an SSH error after rejoining a node with the same IP or hostname, run `pvecm updatecerts` once on the re-added node.
5. Reinstalling is the recommended way to reuse the machine; to rejoin the same server, reinstall Proxmox VE and join it as described in the create-and-join skill.

## Separate a node without reinstalling (advanced, from the admin guide)
Not the recommended method. A cluster cannot share the exact same storage with another cluster (storage locking does not work across clusters) and it risks VMID conflicts, so first give the node its own new storage (for example a new NFS export or Ceph pool) and move its data and VMs there. Then, on the node to separate:
```sh
systemctl stop pve-cluster
systemctl stop corosync
pmxcfs -l
rm /etc/pve/corosync.conf
rm -r /etc/corosync/*
killall pmxcfs
systemctl start pve-cluster
```
Then run `pvecm delnode <oldnode>` on a remaining node, and on the separated node remove `/var/lib/corosync/*`. The removed node's keys stay in `/etc/pve/priv/authorized_keys` until you delete them.

## Two-node edge case
If `pvecm delnode` fails on the remaining node because quorum is lost, the documented workaround is `pvecm expected 1` followed by repeating `pvecm delnode`.

## Gotchas
- Booting the removed node with its old configuration can break the cluster; reinstall or isolate it.
- A QDevice must be removed before adding or removing nodes.
- Destroy the node's Ceph services and remove it from the CRUSH hierarchy before power-off.

## Verify
`pvecm nodes` lists only the remaining members, `/etc/pve/nodes/<old>` is gone, and `ceph -s` shows the expected monitors and OSDs.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, pvecm.adoc, last pushed 2026-10-17). Confirmed: removal prerequisites, Ceph removal order and commands, power-off warning, `pvecm delnode`, the `cs_err_not_exist` note, cleanup items (node directory, HA rules, `authorized_keys`, `known_hosts` and `pvecm updatecerts`), the separate-without-reinstall procedure and storage warning, the `pvecm expected 1` delnode workaround, QDevice removal first, reinstall to rejoin. Removed: `pvesr list`, the `/etc/pve/priv/known_hosts` path, the two-node expected-votes claim as a general rule, and the backup-job and Ceph-monitor-quorum remarks (not documented).

Method: documentation only; no commands were run.
