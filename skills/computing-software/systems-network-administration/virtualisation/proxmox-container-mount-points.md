---
id: computing-software.systems-network-administration.virtualisation.proxmox-container-mount-points
name: proxmox-container-mount-points
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [lxc-mount-point, mp0, bind-mount, storage-backed-mount, pct-set, lxc, pct, backup-flag, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Add storage to Proxmox containers: storage-backed mount points vs host bind mounts (mp0), backup/replicate flags, read-only mounts, and the migration and snapshot limits."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#pct_mount_points
  - https://github.com/proxmox/pve-docs/blob/master/pct.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container mount points (mpN)

**Goal:** give containers extra storage or access to host data, knowing what that does to
backups, snapshots and migration.

## Storage-backed mount point
A new volume on a PVE storage, managed like the rootfs:
```sh
pct set 200 --mp0 local-lvm:50,mp=/srv/data,backup=1
```
Included in snapshots; included in vzdump backups only with `backup=1`; replicated by default (`replicate=1`) and moved with the container.

## Bind mount (host directory)
```sh
pct set 200 --mp1 /tank/media,mp=/mnt/media,ro=1
```
- Host path must exist and must not contain symlinks; ownership must suit the unprivileged UID shift (see idmap skill). The docs advise bind mounting only from a dedicated directory such as one under `/mnt/bindmounts`, never system directories.
- **Not** included in vzdump backups or container snapshots; back up the host path
  separately.
- Bind mounts are not managed by the storage subsystem: no snapshots and no quotas from inside the container. Migration needs the same path on the target node; mark `shared=1` only if it truly is shared, e.g. an NFS mount on every node.

## Options
| Option | Meaning |
|---|---|
| `backup=0/1` | Include volume in vzdump (additional mount points are off by default; add `backup=1`) |
| `ro=1` | Read-only |
| `replicate=0` | Exclude from storage replication (default 1) |
| `acl=1`, `quota=1` | ACLs and user quotas inside (quota is not supported with ZFS subvolumes) |
| `size=` | Volume size for storage-backed volumes |
| `shared=1` | Mark a bind-mount path as available on all nodes |

## Device mounts
Block devices of the host can be mounted as a device mount point (not backed up by vzdump, but `quota` and `acl` are honoured); the docs say to use them only in special circumstances. Device nodes to pass through use `devN:` entries (`dev0: /dev/dri/renderD128,gid=104`; options path, uid, gid, mode, deny-write).

## Gotchas
- Bind-mounting a path that is itself an NFS mount on the host: if the NFS server hangs,
  the container hangs.
- Removing an `mp` entry detaches the volume as an `unusedN` entry; remove that entry to delete the volume.

## Verify
`pct config 200` shows the mpN entries; inside `df -h /srv/data` shows the volume; a test
vzdump log lists which mount points were included or excluded.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: pct.adoc Mount Points, Backup and Restore sections; generated pct-mountpoint-opts.adoc) and confirmed bind-mount behaviour (no snapshots, quotas or vzdump backup, no symlinks in the source path), the backup, replicate, quota, acl, shared and size options, and that additional mount points need backup=1. Removed the unconfirmed PVE 8.1 gate and the pct set --delete detail.

Method: documentation only; no commands were run.
