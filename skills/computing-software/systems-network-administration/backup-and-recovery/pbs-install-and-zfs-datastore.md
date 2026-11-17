---
id: computing-software.systems-network-administration.backup-and-recovery.pbs-install-and-zfs-datastore
name: pbs-install-and-zfs-datastore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pbs-install, proxmox-backup-server, pbs-datastore, zfs, proxmox, pbs]
level: practitioner
status: docs-checked
description: "Install Proxmox Backup Server from ISO or on Debian, build a ZFS pool with a special device for the datastore, create the datastore, and attach it to Proxmox VE."
sources:
  - https://pbs.proxmox.com/docs/installation.html
  - https://pbs.proxmox.com/docs/storage.html
  - https://pbs.proxmox.com/docs/sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox Backup Server install and ZFS datastore

**Goal:** a PBS host with a resilient, fast datastore that Proxmox VE can back up to.

## Install
- **ISO** (bare metal, recommended): installer offers ext4/xfs/ZFS for the OS disks; keep OS disks separate from datastore disks.
- **On Debian** (shown for Debian 12; the installation page also gives the Debian 13 `trixie` form):
```sh
echo "deb http://download.proxmox.com/debian/pbs bookworm pbs-no-subscription" > /etc/apt/sources.list.d/pbs.list
wget https://enterprise.proxmox.com/debian/proxmox-release-bookworm.gpg -O /etc/apt/trusted.gpg.d/proxmox-release-bookworm.gpg
apt update && apt install proxmox-backup-server
```
Web UI: `https://<host>:8007` (login `root@pam`).

## Datastore on ZFS
PBS stores backup data as many small chunk files; the PBS docs recommend a fast metadata cache, for example a ZFS special device mirror.
```sh
zpool create -o ashift=12 backup raidz2 /dev/disk/by-id/ata-HDD1 ... /dev/disk/by-id/ata-HDD6 \
  special mirror /dev/disk/by-id/nvme-A /dev/disk/by-id/nvme-B
zfs set compression=lz4 atime=on relatime=on backup
proxmox-backup-manager datastore create store1 /backup/store1
```
Or GUI: Administration -> Storage/Disks -> ZFS -> Create (tick *Add as Datastore*).
- Keep atime working (relatime is fine); garbage collection relies on chunk access times.

## Attach to Proxmox VE
```sh
proxmox-backup-manager cert info | grep Fingerprint
pvesm add pbs pbs1 --server 10.0.0.5 --datastore store1 --username backup@pbs \
  --password 'xxx' --fingerprint 'aa:bb:...'
```
Use a dedicated user/token with DatastoreBackup, not root.

## Verify
`proxmox-backup-manager datastore list`, a test vzdump to `pbs1` succeeds, and scheduled verify/prune/GC jobs exist on the datastore.

## Checked

2026-10-28

Confirmed: PBS installation and sysadmin docs: no-subscription repository, package name, port 8007, special device recommendation, datastore create, cert info, pvesm add pbs.

Removed or corrected: chunk size figure, co-install claim, ZFS dedup advice, special vdev and RAIDZ comparison claims.

Method: documentation only; no commands were run.
