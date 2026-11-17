---
id: computing-software.systems-network-administration.virtualisation.proxmox-zfs-over-iscsi-storage
name: proxmox-zfs-over-iscsi-storage
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [zfs-over-iscsi, zfs, iscsi, pvesm, proxmox, storage]
level: advanced
status: docs-checked
description: "Configure ZFS over iSCSI storage in Proxmox VE: SSH key setup to the storage box, iSCSI provider choice (LIO, istgt, comstar), storage.cfg options and limits."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#storage_zfs
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-zfs.adoc
  - https://github.com/proxmox/pve-storage/blob/master/src/PVE/Storage/ZFSPlugin.pm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ZFS over iSCSI storage

**Goal:** shared block storage with per-disk zvols and snapshots on a separate ZFS storage server.

## How it works
PVE logs into the storage server over SSH as root, creates a zvol per VM disk, and exports it as an iSCSI LUN; QEMU connects to the LUN directly. Snapshots are ZFS snapshots on the server.

## SSH key (key file lives in /etc/pve/priv/zfs, shared through pmxcfs)
```bash
mkdir -p /etc/pve/priv/zfs
ssh-keygen -f /etc/pve/priv/zfs/10.0.0.30_id_rsa -N ''
ssh-copy-id -i /etc/pve/priv/zfs/10.0.0.30_id_rsa.pub root@10.0.0.30
ssh -i /etc/pve/priv/zfs/10.0.0.30_id_rsa root@10.0.0.30 true   # accept host key on each node
```
The filename must be `<portal>_id_rsa`.

## storage.cfg
```
zfs: san-zfs
	portal 10.0.0.30
	target iqn.2003-01.org.linux-iscsi.san01:sn.pve
	pool tank/pve
	iscsiprovider LIO
	lio_tpg tpg1
	blocksize 16k
	sparse 1
	content images
```
Providers (`iscsiprovider`): `LIO` (Linux), `iet` (Linux), `istgt` (FreeBSD), `comstar` (Solaris). `lio_tpg` sets the target portal group for LIO; Comstar has `comstar_tg` and `comstar_hg`.

## Limits
- Content type is `images` only (raw VM disks); no containers (`rootdir`) on this storage type.
- Shared and snapshot-capable, but no clones; the ZFS appliance must not become a single point of failure.
- PVE runs the zvol and LUN commands on the storage server over SSH as root with a passwordless key, so that key is a high-value credential.

## Verify
Create a test VM disk: a new zvol appears in `zfs list tank/pve` and a LUN in `targetcli ls`; snapshots in PVE create ZFS snapshots on the server.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09).

Confirmed: PVE reaches the target over `ssh` and creates a zvol per guest disk exported as an iSCSI LUN; key path `/etc/pve/priv/zfs/<target_ip>_id_rsa` and the key-creation commands; providers LIO, IET, ISTGT, Comstar; properties `iscsiprovider`, `lio_tpg`, `comstar_tg`, `comstar_hg`, `blocksize`, `sparse`; content type `images` only (plugin source); features table (raw, shared, snapshots yes, clones no). Removed as unconfirmed: the "TrueNAS legacy" and "illumos/OmniOS" provider labels, the multipath statement, the TrueNAS SCALE paragraph and the host-key acceptance rationale beyond the guide's own ssh test.

Method: documentation only; no commands were run.
