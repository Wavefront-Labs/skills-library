---
id: computing-software.systems-network-administration.virtualisation.proxmox-nfs-and-cifs-storage
name: proxmox-nfs-and-cifs-storage
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-nfs, pve-cifs, nfs, smb, pve-storage, storage-cfg, qcow2, shared-storage, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Add NFS and SMB/CIFS shares as Proxmox VE storage: content types, mount options and NFS version, qcow2 for snapshots, stale-mount behaviour and backup targets."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#storage_nfs
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#storage_cifs
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-nfs.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-cifs.adoc
  - https://github.com/proxmox/pve-docs/blob/master/pvesm.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NFS and CIFS storage on Proxmox VE

**Goal:** shared file storage for VM disks, ISOs or backups that all nodes mount
consistently.

## NFS
```sh
pvesm scan nfs <server>
pvesm add nfs nas-vm --server <server> --export /export/pve --content images,iso,backup \
  --options vers=4.2 --path /mnt/pve/nas-vm
```
- NFS has no storage-level snapshots; use the **qcow2** format for VM snapshots and clones. Creating and deleting internal qcow2 snapshots blocks a running VM and can be very slow on network storage for large disks; do it while the VM is shut down if that is a problem.
- The `shared` flag is always set for NFS and CIFS. Prefer an IP address for `server` to avoid DNS lookup delays.
- Mount options go in `options` (see `man nfs`); `path` defaults to `/mnt/pve/<STORAGE_ID>/`.

## CIFS/SMB
```sh
pvesm add cifs nas-backup --server <server> --share pvebackup --username <svc> \
  --password '<from-vault>' --content backup --smbversion 3
```
The password is stored in `/etc/pve/priv/storage/<id>.pw`, readable only by root. `smbversion` unset or `default` negotiates the highest SMB2+ version both sides support; SMB1 is not supported. `username` defaults to `guest`. PVE always sets the mount option `soft`; `username`, `credentials`, `guest`, `domain` and `vers` are set automatically, so do not repeat them in `options`. Optional properties include `domain` and `subdir`. `pvesm scan cifs <server>` lists shares.

## Behaviour
- PVE mounts under `/mnt/pve/<storage-id>` and checks availability (`pvesm status`).
- After an NFS request times out, requests are retried indefinitely by default, which can hang the client. For read-only content consider the NFS `soft` option, which limits retries to three.
- For a manually mounted path used as directory storage, set `is_mountpoint` so the storage is treated as offline when the mount is missing.

## Content types
`images` (VM disks), `rootdir` (container volumes), `iso`, `vztmpl`, `backup`, `snippets`
(for example hook scripts). Restrict to what is intended so backups do not land on
VM storage.

## Verify
`pvesm status` shows the storage active on every node; create a qcow2 test disk, snapshot
it, and run a test backup to the backup-type share.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09).

Confirmed: `pvesm scan nfs`, `server`, `export`, `options`, `path` default; the NFS indefinite-retry tip and the `soft` option (three retries); CIFS properties (`server`, `share`, `username` default guest, `smbversion` semantics, SMB1 unsupported, `subdir`, `domain`, password file location, mount options set automatically, `soft` always set); `shared` always set; qcow2-based snapshots and clones with the performance caution; content type list. Removed as unconfirmed: `no_root_squash` and sync export advice, jumbo-frame advice, the pvestatd and lazy-unmount recovery steps, and "SMB disks are slower".

Method: documentation only; no commands were run.
