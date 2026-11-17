---
id: computing-software.systems-network-administration.backup-and-recovery.windows-system-image-recovery-winre
name: windows-system-image-recovery-winre
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [winre, system-image-recovery, bare-metal-recovery, wbadmin, windows-server-backup, windows]
level: practitioner
status: gated
description: "Restore a Windows system image from WinRE: create a recoverable backup, boot recovery media, load storage drivers, use a network share, and wbadmin sysrecovery switches."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-start-sysrecovery
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-recovery-environment--windows-re--technical-reference
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-start-backup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows system image recovery via WinRE

**Goal:** restore a whole Windows machine from a system image when it will not boot or the disk died.

## Create a recoverable image
```cmd
wbadmin start backup -backupTarget:E: -allCritical -systemState -vssFull -quiet
wbadmin start backup -backupTarget:\\backup01\images\srv01 -allCritical -quiet
```
`-allCritical` includes all critical volumes (those holding operating-system state), requires `-backupTarget`, and the target cannot be one of the included volumes. A backup to a remote share overwrites the previous backup of the same computer in that folder; use sub-folders (which need twice the space).

## Boot into WinRE
`wbadmin start sysrecovery` must be run from the Windows Recovery Environment and is not listed in wbadmin's default usage text. Microsoft's WinRE technical reference describes how to boot into it.

## Command line in WinRE
```cmd
wpeinit                                      :: start networking (gated: unconfirmed, source is paywalled or blocked)
drvload <driver-media>\storage\iaStorVD.inf      :: load RAID/NVMe driver if disks are not visible (gated: unconfirmed, source is paywalled or blocked)
net use Z: \\backup01\images /user:CORP\restore  :: (gated: unconfirmed, source is paywalled or blocked)
wbadmin get versions -backupTarget:Z: -machine:srv01
wbadmin start sysrecovery -version:10/17/2026-02:00 -backupTarget:Z: -machine:srv01 -restoreAllVolumes -recreateDisks -quiet
```
- `-version` is MM/DD/YYYY-HH:MM from `wbadmin get versions`; `-machine` is required with `-backupTarget`.
- Without `-restoreAllVolumes` only critical volumes are recovered.
- `-recreateDisks` restores the disk configuration and deletes all data on volumes hosting operating-system components, and possibly on data volumes; protect data disks with `-excludeDisks` (valid only with `-recreateDisks`, takes identifiers from `wbadmin get disks`).
- `-skipBadClusterCheck` is not recommended when recovering to other hardware; run `chkdsk /b` afterwards instead.

## Gotchas
- Domain controllers: the AD DS forest recovery guide covers restoring AD DS with `wbadmin start systemstaterecovery`; follow it for DC recovery.

## Verify
Restore the image into a VM or spare machine quarterly; it boots, logs in, and services start.

## Checked

Checked 2026-10-27 against the wbadmin reference pages in MicrosoftDocs/windowsserverdocs (start sysrecovery, start backup, get versions, start systemstaterecovery). Confirmed: `sysrecovery` runs only in WinRE, its parameters (`-version`, `-backupTarget`, `-machine`, `-restoreAllVolumes`, `-recreateDisks`, `-excludeDisks`, `-skipBadClusterCheck`, `-quiet`) and their warnings, `-allCritical` rules, and the remote-share overwrite behaviour. Gated: the `wpeinit`, `drvload` and `net use` helper commands are not documented on the pages readable for this check. Removed the unconfirmed menu paths, firmware-mode, disk-size, BitLocker and VM-GenerationID remarks.

Method: documentation only; no commands were run.
