---
id: computing-software.systems-network-administration.virtualisation.proxmox-directory-and-btrfs-storage
name: proxmox-directory-and-btrfs-storage
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-directory-storage, pve-btrfs, pvesm, proxmox, storage]
level: practitioner
status: docs-checked
description: "Add directory and BTRFS storage in Proxmox VE with pvesm, protect against missing mounts with is_mountpoint, and choose content types and shared flags correctly."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#storage_directory
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#storage_btrfs
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-dir.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-btrfs.adoc
  - https://github.com/proxmox/pve-storage/blob/master/src/PVE/Storage/DirPlugin.pm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Directory and BTRFS storage

**Goal:** file-based storage for ISOs, templates, backups or disk images, without filling the root filesystem by accident.

## Directory storage
```bash
mkfs.xfs /dev/sdb1 && mkdir -p /mnt/backup
echo 'UUID=<uuid> /mnt/backup xfs defaults,nofail 0 2' >> /etc/fstab && mount -a
pvesm add dir backup-local --path /mnt/backup --content backup,iso,vztmpl --is_mountpoint yes --prune-backups keep-daily=7,keep-weekly=4
```
- `is_mountpoint yes` makes PVE refuse to use the path when nothing is mounted, so backups do not silently land on the root disk.
- `shared 1` only if the path is the same network share on every node (for example a mounted cluster filesystem); PVE does not mount it for you.
- Disk images on directories are `qcow2` (snapshots, linked clones) or `raw`.

## BTRFS storage (technology preview)
```bash
mkfs.btrfs -m raid1 -d raid1 /dev/sdc /dev/sdd
mount /dev/sdc /mnt/btrfs
pvesm add btrfs btrfs1 --path /mnt/btrfs --content images,rootdir --is_mountpoint yes
```
`raw` guest disks are placed in a subvolume so snapshots work; a snapshot is a read-only subvolume named like the original path followed by `@` and the snapshot name. BTRFS honours `O_DIRECT`, so VMs must not use cache mode `none` (checksum errors). If the storage path is a subdirectory of the mount point, set `is_mountpoint` to the actual mount point, for example `is_mountpoint /mnt/data2`. Check the storage table for the current support level: BTRFS is a technology preview with best-effort support.

## Content types
`images` (VM disks), `rootdir` (container volumes), `iso`, `vztmpl`, `backup`, `snippets` (for example guest hook scripts), `import` (OVAs and disk images to import). Directory layout: `images/<VMID>/`, `template/iso/`, `template/cache/`, `dump/`, `snippets/`, `import/`; the optional `content-dirs` property changes it.

## Gotchas
- Mount extra disks through `/etc/fstab` and then define the directory storage on the mount point; `is_mountpoint` marks the storage offline when nothing is mounted.
- Some file systems do not support `O_DIRECT`; use cache mode `writeback` instead of `none` there.
- Directory storage has no storage-level snapshots; only `qcow2` images get snapshots and clones. Template base images are made read-only (mode 0444, `chattr +i` where supported).

## Verify
`pvesm status` lists the storage as active with expected size; unmount it and `pvesm status` shows it inactive rather than reporting the root filesystem size.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09).

Confirmed: `is_mountpoint` description ("consider the storage offline if it is not mounted", boolean shortcut uses the storage path) in the plugin source; BTRFS technology-preview status, subvolume layout, `O_DIRECT` cache warning, `@` snapshot naming and the `is_mountpoint` example in the BTRFS page; directory layout, `content-dirs`, content types and qcow2-only snapshots in the directory page; `shared` semantics in the pvesm page. Removed as unconfirmed: BTRFS RAID5/6 advice, the Node -> Disks GUI claim, nofail ordering advice and the manual-NFS health-check claim.

Method: documentation only; no commands were run.
