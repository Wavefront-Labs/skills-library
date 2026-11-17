---
id: computing-software.systems-network-administration.active-directory.virtual-dc-backup
name: virtual-dc-backup
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, virtualized-domain-controller, virtual-dc-backup, system-state-backup, vss]
level: practitioner
status: docs-checked
description: "Back up virtualized domain controllers correctly: VSS-aware system state or host-level backups that are AD-aware, never relying on hypervisor snapshots."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/virtual-dc/restore-virtualized-domain-controller
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/virtualized-domain-controllers-hyper-v
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-start-systemstatebackup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backing up virtual domain controllers

A hypervisor snapshot is not an AD backup. Microsoft's virtual DC guidance says not to take or use snapshots of
virtual DCs and to use an Active Directory-compatible backup method instead.

## What to back up
- **System state** of DCs on a regular schedule. Microsoft's restore guide says to back up regularly and at
  least every tombstone-lifetime interval; the system state includes AD data and log files, the registry,
  SYSVOL and parts of the OS. With Windows Server Backup:
```cmd
wbadmin start systemstatebackup -backupTarget:E: -quiet
```
  `-backupTarget` takes a drive letter, a GUID-based volume, or a share (`\\server\share\`).
- Or a third-party/host-level product that Microsoft's guide would count as an Active Directory-compatible backup
  utility; check the vendor's statement that it backs up the AD system state.

## Rules
- The default tombstone lifetime is 180 days; restore a DC only from a backup within the tombstone lifetime
  of the forest (check the actual value in your forest).
- Restore with the same Active Directory-compatible utility that created the backup.
- Do not use snapshots, VHD copies or Export of a DC as a backup or as a rollback plan for changes.
- Keep at least one backup copy outside the virtualization estate, so one compromise cannot delete both.
- Test restores in an isolated network.

## Verify
- [ ] Each domain has recent system-state backups from more than one DC.
- [ ] A restore test of system state is documented with its date.

## Checked

Documentation: Microsoft Learn "Restore a virtual domain controller" (updated 2025), virtualized-DC-on-Hyper-V guidance
and the wbadmin start systemstatebackup reference, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: wbadmin start systemstatebackup syntax with `-backupTarget` and `-quiet`, system state contents, default
tombstone lifetime 180 days, restore with the same compatible utility, no-snapshot/no-Export guidance.
Removed unconfirmed claims: `repadmin /showbackup`, event 2089 and its latency default, VSS integration-service and
dSASignature details, production checkpoints advice and the quarterly test schedule.

Method: documentation only; no commands were run.
