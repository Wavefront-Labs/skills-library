---
id: computing-software.systems-network-administration.backup-and-recovery.windows-server-backup-and-system-state
name: windows-server-backup-and-system-state
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [wbadmin, system-state, windows-server-backup, bare-metal-recovery, domain-controller, authoritative-restore, dsrm]
level: practitioner
status: gated
description: "Use Windows Server Backup and wbadmin for system state and bare-metal backups, restore DC system state (non-authoritative and authoritative), and know its limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-perform-nonauthoritative-restore
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Windows Server Backup and system state

**Goal:** a built-in, scriptable way to back up and restore Windows server configuration and domain controllers.

## Install and back up
```powershell
Install-WindowsFeature Windows-Server-Backup   # (gated: unconfirmed, source is paywalled or blocked)
```
```cmd
wbadmin start systemstatebackup -backupTarget:E: -quiet
wbadmin start backup -backupTarget:\\bkp01\wsb$\dc01 -allCritical -systemState -vssFull -quiet
wbadmin get versions -backupTarget:E:
```
- `-allCritical` includes all critical volumes (those holding operating-system state) for bare-metal recovery; it requires `-backupTarget`, and the target cannot be one of the volumes being backed up.
- A backup to a remote share overwrites the previous backup of the same computer in the same folder, and a failed run can leave you with no usable backup; use sub-folders (which need twice the space).
- `-vssFull` performs a full VSS backup, updates file history and may truncate logs of previous backups; do not use it if another product backs up applications on those volumes. `-vssCopy` is the default and leaves that history alone.
- `wbadmin start systemstatebackup` takes a volume or UNC target; WSB does not back up or restore registry user hives (HKCU).
- Schedule a daily backup with `wbadmin enable backup` (`-addtarget`, `-schedule:HH:MM`, `-systemState`, `-allCritical`); a disk given as target is formatted and its data erased.

## Restore system state (domain controller)
1. Boot into Directory Services Restore Mode (`bcdedit /set safeboot dsrepair`, reboot; DSRM password needed) (gated: unconfirmed, source is paywalled or blocked). This command line is not on the Microsoft pages that could be read for this check.
2. ```cmd
   wbadmin start systemstaterecovery -version:10/15/2026-02:00 -quiet
   ```
   `-version` is MM/DD/YYYY-HH:MM from `wbadmin get versions`; add `-backupTarget` with `-machine` for another location, `-recoveryTarget` for an alternate directory and `-autoReboot` only if no further steps are needed. This is a **nonauthoritative** restore of AD DS. Add `-authsysvol` to also restore SYSVOL authoritatively, only on the first DC restored in the forest root domain; the backup must explicitly include system state.
3. For **authoritative** restore of deleted objects use `ntdsutil` before leaving DSRM (gated: unconfirmed, source is paywalled or blocked); follow Microsoft's AD DS recovery documentation for the exact subtree commands and back-link handling.
4. Clear the safe-boot flag with `bcdedit /deletevalue safeboot` and reboot (gated: unconfirmed, source is paywalled or blocked).

## Bare-metal recovery
Boot into the Windows Recovery Environment and run `wbadmin start sysrecovery`, which is available only there (see the WinRE system image recovery skill).

## Limits
It is a built-in tool without central management; use it for small sites, DC system state, or as an extra layer.

## Verify
`wbadmin get versions` lists recent versions, and a system state restore of a lab DC in an isolated network succeeds.

## Checked

Checked 2026-10-27 against the wbadmin reference pages in MicrosoftDocs/windowsserverdocs (wbadmin, start backup, start systemstatebackup, start systemstaterecovery, start sysrecovery, enable backup) and the AD DS forest recovery guide pages for system state backup and nonauthoritative restore. Confirmed: `-allCritical` rules, remote-share overwrite behaviour, `-vssFull` versus the default `-vssCopy`, the HKCU hive exclusion, `enable backup` options and disk formatting, `systemstaterecovery` options including `-authsysvol`, `-version` format, and that `sysrecovery` runs only in WinRE. Gated: the `Install-WindowsFeature` name, the `bcdedit` safe-boot commands for DSRM and the `ntdsutil` authoritative restore step are not documented on the pages readable for this check.

Method: documentation only; no commands were run.
