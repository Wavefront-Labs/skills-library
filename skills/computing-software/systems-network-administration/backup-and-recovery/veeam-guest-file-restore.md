---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-guest-file-restore
name: veeam-guest-file-restore
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [guest-file-restore, veeam-restore, file-level-restore, mount-server, veeam, flr]
level: practitioner
status: draft
description: "Restore individual files from Veeam VM backups: Windows file-level restore via mount server, Linux restore via helper host, permissions and Copy To options."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/overview.html?ver=120
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Veeam guest OS file restore

## Windows guests (NTFS/ReFS)
Home → Backups → right-click VM → **Restore guest files → Microsoft Windows**:
1. Pick the restore point.
2. Veeam mounts the backup disks on the **mount server** associated with the repository (
   under `<SYSTEM_DRIVE>\VeeamFLR\<vm>\Volume N`).
3. Veeam Backup Browser opens: search, select files/folders, then:
   - **Restore → Overwrite / Keep** (writes back into the original VM via VIX/VMware Tools
     or network share, needs guest credentials),
   - **Copy To** (any path, option to preserve permissions/ownership),
   - Open in Explorer for manual copy.
4. Close the browser to unmount (sessions time out after inactivity).

With guest indexing enabled on the job, you can search the catalogue in Enterprise Manager
and restore without mounting first (and delegate self-service restores).

## Linux and other filesystems
Restore guest files → **Linux and other**: Veeam mounts disks to a Linux host you specify
(v12, any Linux server with the right tools) or a temporary **helper appliance** on a
host/cluster. Supports ext2/3/4, XFS, Btrfs, LVM, ZFS (with limits). Restore back to the
original VM over SSH or download.

## Requirements and gotchas
- Mount server must reach the repository and have enough temp space.
- Restoring to original location requires credentials with write rights in the guest and
  network/VIX access; when blocked, use Copy To + manual copy.
- Encrypted backups prompt for the password (or use password loss protection).
- Dedup-enabled Windows volumes: mount server needs the Data Deduplication feature to read
  them.
- BitLocker inside the guest: you need the recovery key to open the volume.
- Long paths and special permissions: use Copy To with "preserve permissions" and verify ACLs.

## Verify
Files restored match expected versions/size and open in the app; user confirms; restore
session logged (Home → History) for audit.
