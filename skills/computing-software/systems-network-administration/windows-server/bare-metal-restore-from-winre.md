---
id: computing-software.systems-network-administration.windows-server.bare-metal-restore-from-winre
name: bare-metal-restore-from-winre
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server-backup, bare-metal-restore, winre, system-state-backup, disaster-recovery]
level: advanced
status: docs-checked
description: "Perform a bare-metal recovery of Windows Server from a WSB image using WinRE: boot media, finding the backup, drivers, disk layout and post-restore checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-start-sysrecovery
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc755163(v=ws.11)
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bare-metal restore from WinRE

Restores a whole server (OS, apps, critical volumes) onto new or wiped hardware from a backup that included
**Bare metal recovery**.

## Prepare
- Windows Server installation media of the same version (or the server's own WinRE if the disk still boots).
- The backup target: attached WSB disk, or a network share path plus credentials.
- Storage/NIC drivers for the new hardware on a USB stick.

## Steps
Use the command line below from the recovery environment; `-recreateDisks` recreates the disk layout and `-excludeDisks` leaves chosen disks alone.


## After restore
- Reapply updates installed after the backup date; check applications and services.

## Verify
- [ ] Server boots, services and data current to backup time; restore time recorded for RTO.

## Checked
2026-10-28: Confirmed on Learn page wbadmin-start-sysrecovery: syntax with -version, -backupTarget, -machine, -restoreAllVolumes, -recreateDisks, -excludeDisks; wbadmin get versions -backupTarget -machine. Removed: System Image Recovery wizard steps, disk-size claim, domain controller non-authoritative and tombstone notes, secure-channel and password-cycle claims.
Method: documentation only; no commands were run.
