---
id: computing-software.systems-network-administration.windows-server.wbadmin-file-and-volume-restore
name: wbadmin-file-and-volume-restore
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-server-backup, wbadmin, wbadmin-restore, file-recovery, volume-recovery, get-wbbackupset]
level: practitioner
status: docs-checked
description: "Restore files, folders, volumes and registered apps from Windows Server Backup with wbadmin: list versions, alternate locations, overwrite and ACL options."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-start-recovery
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-get-items
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restore files and volumes with wbadmin

## Find the backup
```powershell
wbadmin get versions -backupTarget:\\nas01\wsb -machine:SRV01
wbadmin get items -version:10/15/2026-21:00 -backupTarget:\\nas01\wsb -machine:SRV01
Get-WBBackupSet
```

## Files and folders
```powershell
wbadmin start recovery -version:10/15/2026-21:00 -itemType:File -items:'<vol>:\Shares\Finance\Budget' `
  -recursive -recoveryTarget:'<vol>:\Restore' -overwrite:CreateCopy -backupTarget:\\nas01\wsb -machine:SRV01
```
- `-version` uses `MM/DD/YYYY-HH:MM`; `-machine` is required when `-backupTarget` is given.
- All items must be on one volume and under the same parent folder. `-recursive` includes subfolders (default: only
  files directly in the folder).
- `-overwrite` (files only): Overwrite, CreateCopy (keeps the existing file), Skip.
- Add `-notRestoreAcl` (files only) so restored files inherit ACLs from the target; default restores original ACLs.
- Restoring to the original location while users work can conflict: restore to an
  alternate folder and copy.

## Whole volume
```powershell
wbadmin start recovery -version:10/15/2026-21:00 -itemType:Volume -items:E: -recoveryTarget:F: -quiet
```
With `-itemType:Volume` you can give only a single volume (drive letter, mount point or GUID-based name). A volume
with no letter at backup time is listed by `get items` as a GUID-based name. `-skipBadClusterCheck` skips the bad
cluster check; after skipping, run `chkdsk /b` on the target (Microsoft advises not skipping it for different hardware).

## Applications (registered with Windows Server Backup)
```powershell
wbadmin get items -version:<v>      # lists what can be recovered, including apps
wbadmin start recovery -version:<v> -itemType:App -items:Registry -recoveryTarget:<vol>:\
```
Only a single app per command; `ADIFM` recovers an Active Directory install-from-media copy and needs `-recoveryTarget`.
For Hyper-V see the `Start-WBHyperVRecovery` cmdlet reference.

## Gotchas
- Run from an elevated prompt as a member of Backup Operators or Administrators.

## Verify
- [ ] Restored item opens; hashes match a known copy where available.

## Checked
2026-10-28. Confirmed against the Microsoft Learn pages `wbadmin start recovery` and `wbadmin get items`: version format,
`-backupTarget`/`-machine`, `-itemType` values and single-item rules, `-recursive`, `-overwrite` options, `-notRestoreAcl`,
`-recoveryTarget`, `-skipBadClusterCheck`, ADIFM, required group membership. Removed as unconfirmed or wrong: `-itemsList`
(not a parameter), `wbadmin restore catalog`, overwrite-whole-volume claim, deduplication and Shadow Copies for Shared
Folders gotchas, Get-WBBackupSet property list.
Method: documentation only; no commands were run.
