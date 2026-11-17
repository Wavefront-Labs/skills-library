---
id: computing-software.systems-network-administration.backup-and-recovery.proxmox-backup-server-file-restore
name: proxmox-backup-server-file-restore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pbs-file-restore, proxmox-backup-client, proxmox-backup-server, file-restore, pxar, single-file-restore, proxmox-backup]
level: practitioner
status: docs-checked
description: "Restore single files from Proxmox Backup Server: GUI file restore from VM and CT backups, proxmox-backup-client catalog shell, mount and map, and host-level pxar backups."
sources:
  - https://pbs.proxmox.com/docs/backup-client.html
  - https://pve.proxmox.com/pve-docs/chapter-vzdump.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single-file restore from PBS

**Goal:** get one file or folder back from a VM, container or host backup without restoring the whole guest.

## From the Proxmox VE GUI
Storage (PBS) > Backups > select snapshot > **File Restore**. For VMs, PVE starts a temporary helper VM that reads the disk image's partitions and filesystems; browse and download files or folders (as zip). Container backups (pxar) are browsed directly.

## proxmox-backup-client
```bash
export PBS_REPOSITORY='restore@pbs@pbs1.example:store1'
export PBS_FINGERPRINT='<sha256 fingerprint>'
proxmox-backup-client snapshot list
proxmox-backup-client catalog shell host/web01/2026-10-15T01:00:00Z root.pxar
#   pxar:/ > find /etc/nginx/*.conf --select
#   pxar:/ > restore-selected /tmp/restore
proxmox-backup-client restore host/web01/2026-10-15T01:00:00Z root.pxar /tmp/restore --pattern 'etc/nginx/**'
```

## Mount and map
```bash
proxmox-backup-client mount host/web01/2026-10-15T01:00:00Z root.pxar /mnt/pbs     # FUSE
proxmox-backup-client map vm/101/2026-10-15T01:00:00Z drive-scsi0.img             # loop device for a VM disk
mount -o ro /dev/loop0p1 /mnt/vmdisk
proxmox-backup-client unmap /dev/loop0
```

## Host backups (physical or non-PVE machines)
```bash
proxmox-backup-client backup root.pxar:/ etc.pxar:/etc --exclude /var/cache --keyfile /root/pbs-enc.key
```
Client-side encryption keys must be available at restore time; escrow them (paperkey).

## Gotchas
- Encrypted backups cannot be browsed server-side without the key.

## Verify
Restore a known file monthly from an older snapshot and compare its hash with a reference copy.

## Checked

2026-10-28

Confirmed: PVE admin guide (file restore with on-the-fly zip download of directories, temporary VM) and PBS backup client docs: catalog shell, restore-selected, --pattern, mount, map and unmap.

Removed or corrected: supported-filesystem list, helper VM binary name, free-memory gotcha.

Method: documentation only; no commands were run.
