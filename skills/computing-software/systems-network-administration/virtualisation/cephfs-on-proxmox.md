---
id: computing-software.systems-network-administration.virtualisation.cephfs-on-proxmox
name: cephfs-on-proxmox
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [cephfs, ceph-mds, pveceph, ceph, shared-filesystem, iso-storage, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Set up CephFS on Proxmox VE for ISOs, templates, snippets and backups: metadata servers, pveceph fs create, storage entry, standby MDS and limits for VM disks."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pveceph_fs
  - https://github.com/proxmox/pve-docs/blob/master/pveceph.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-cephfs.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CephFS on Proxmox VE

**Goal:** a shared POSIX filesystem across the cluster for ISOs, container templates,
snippets and vzdump files, without an external NAS.

## Create
```sh
pveceph mds create              # at least one MDS is required; create more for standbys
pveceph fs create --pg_num 128 --add-storage
ceph fs status
```
This creates a CephFS named `cephfs` with a data pool `cephfs_data` (128 PGs here) and a metadata pool `cephfs_metadata` with a quarter of the data pool's PGs (32), plus a PVE storage entry; the mount point defaults to `/mnt/pve/<STORAGE_ID>/`. CephFS storage supports the content types vztmpl, iso, backup and snippets (no VM disk images). Prerequisites: working OSDs and at least one MDS.

## Use well
- Good: ISOs and templates available on every node; cloud-init snippets; small backup
  targets.
- **VM disks:** use RBD, not CephFS. RBD is the block path with better performance and
  snapshots integrated with PVE.
- Backups on CephFS live in the same Ceph cluster as the VMs: one cluster failure loses
  both. Use PBS or external storage for real backups.

## Metadata servers
- With the default settings only one MDS is active at a time; if it or its node fails, a `standby` MDS is promoted. Speed up the handover with the `hotstandby` option when creating the MDS, or by setting `mds standby replay = true` for an existing one.
- Multiple active MDS daemons are possible but normally only useful with a high number of parallel clients.

## Gotchas
- CephFS snapshots are not yet guaranteed to be stable (the storage page's note: they lack sufficient testing); `clones` are not supported.
- If you need the FUSE client instead of the kernel client, the storage has a `fuse` option (default 0).

## Verify
`ceph fs status` shows one active and at least one standby MDS; `pvesm status` shows the
cephfs storage active on all nodes; an ISO uploaded on one node appears on all.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09).

Confirmed in the CephFS chapter: at least one MDS needed, `pveceph mds create`, one active MDS by default with standby promotion, `hotstandby` and `mds standby replay = true`, multiple active MDS caveat, `pveceph fs create --pg_num 128 --add-storage` creating `cephfs` with `cephfs_data` (128 PGs) and `cephfs_metadata` (32 PGs); storage features (content types, snapshots not yet guaranteed stable, no clones), `fuse` option, default mount path. Removed as unconfirmed: the `--name` flag in the example, the 4 GiB MDS cache default, the SSD metadata-pool advice, the stale-mount remount tip, the multiple-filesystem remark, and the default content list.

Method: documentation only; no commands were run.
