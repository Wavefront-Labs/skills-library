---
id: computing-software.systems-network-administration.windows-server.hyper-v-vm-backup-with-windows-server-backup
name: hyper-v-vm-backup-with-windows-server-backup
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, server-backup, hyper-v-vm-backup, wbadmin, vss, hyper-v]
level: practitioner
status: docs-checked
description: "Back up and restore Hyper-V VMs with Windows Server Backup and wbadmin: host-level VSS backups, production checkpoints, restore to original or alternate location."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-start-backup
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-start-recovery
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V VM backup with Windows Server Backup

Windows Server Backup (WSB) is the in-box backup tool; `wbadmin` is its command line. Confirm in the Hyper-V and WSB
documentation how VM-level (VSS writer) backup behaves for your host version, and test a restore before relying on it.

## Back up the volumes that hold the VMs
```cmd
wbadmin start backup -backupTarget:\\backup01\hv01 -include:<VM_VOLUME>: -quiet
wbadmin start backup -backupTarget:<BACKUP_VOLUME>: -include:<VM_VOLUME>: -vssFull -quiet
```
- `wbadmin` has no `-hyperv` switch; `-include` takes files, folders or volumes, and needs `-backupTarget`.
- Without `-vssFull` or `-vssCopy`, parameters given means a copy backup (`-vssCopy`, the default) that does not update
  file history. Do not use `-vssFull` if another product also backs up apps on those volumes: it can break that
  product's incremental or differential chain.
- A remote share keeps one backup per computer: a second backup to the same share overwrites the first, and a failed run
  can leave you without a usable backup. Use subfolders per backup (needs about twice the space).
- Console: Windows Server Backup > Backup Once / Backup Schedule > Custom.

## Restore
```cmd
wbadmin get versions -backupTarget:\\backup01\hv01 -machine:HV01
wbadmin get items -version:<MM/DD/YYYY-HH:MM> -backupTarget:\\backup01\hv01 -machine:HV01
wbadmin start recovery -version:<MM/DD/YYYY-HH:MM> -itemType:File -items:<VM_FOLDER> -recursive -recoveryTarget:<RESTORE_PATH> -backupTarget:\\backup01\hv01 -machine:HV01
```
- `-itemType` is Volume, App or File only. Files must share one volume and parent folder.
- `-recoveryTarget` restores to a different location; restore a copy first, then register or compare it.
- The `Start-WBHyperVRecovery` cmdlet exists for Hyper-V recovery (see its reference page for parameters).

## Gotchas
- Run elevated as a Backup Operators or Administrators member.
- Large VMs over a slow share run long; schedule outside business hours.

## Verify
- [ ] `wbadmin get versions` shows the backup; a test restore to an alternate location boots.

## Checked
2026-10-28. Confirmed against the Microsoft Learn pages `wbadmin start backup` and `wbadmin start recovery`: `-include`,
`-backupTarget`, `-vssFull`/`-vssCopy` behaviour, share overwrite and subfolder advice, `-itemType` values, `-recoveryTarget`,
`-machine`, existence of `Start-WBHyperVRecovery`. Removed as wrong: `-hyperv` on start backup, `-itemType:hyperv`,
`-alternateLocation`. Removed as unconfirmed: guest VSS and saved-state behaviour, CSV and cluster limits, shared VHDX
claim, DPM/MABS advice, "keeps versions on a dedicated disk".
Method: documentation only; no commands were run.
