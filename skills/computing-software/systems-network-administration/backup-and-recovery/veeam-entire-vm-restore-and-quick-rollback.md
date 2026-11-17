---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-entire-vm-restore-and-quick-rollback
name: veeam-entire-vm-restore-and-quick-rollback
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, entire-vm-restore, quick-rollback, vm-restore, cbt, secure-restore]
level: practitioner
status: draft
description: "Restore a whole VM with Veeam to original or new location, use Quick Rollback to write back only changed blocks, and scan with Secure Restore before power-on."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/incremental_restore.html
  - https://helpcenter.veeam.com/docs/backup/vsphere/av_scan_about.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entire VM restore and Quick Rollback

Home > Backups > right-click VM > **Restore entire VM**.

## Decide location
- **Original location**: overwrites the existing VM (powers it off). Fastest path back for a corrupted guest.
- **New location / different settings**: new name, host, datastore, network; original VM untouched. Use when you must compare or when the original is evidence (ransomware).

## Quick Rollback
Option on original-location restore: **Quick rollback (restore changed blocks only)**. Veeam uses CBT to find blocks changed since the restore point and writes only those back.
- Use for guest-level problems (bad patch, deleted files, app corruption) where the VM's disks are intact.
- Do not use after storage failure, disk corruption or a host crash affecting the VMDK: CBT data may be wrong. Run a normal full restore.
- Takes minutes instead of hours for large VMs.

## Secure Restore
Tick **Scan the restored machine for malware** (uses the antivirus installed on the mount server) and choose the action on detection: abort, or restore with network disconnected. Use whenever restoring after a security incident.

## Steps
1. Pick restore point (check the Malware status column in v12.1+ if detection is enabled).
2. Choose mode, location, optionally rename and disconnect NICs.
3. Reason field: enter the ticket number for audit.
4. Do not power on automatically if IP conflicts are possible (restoring alongside the original).

## Gotchas
- Restore to original location of a VM that was renamed or moved: Veeam matches by MoRef ID; if the VM was deleted, choose new location.
- Thick/thin conversion: restore uses the selected disk type; check datastore space.

## Verify
VM powers on, app owner validates; restore session log shows "Restored N GB (changed blocks)" for Quick Rollback.
