---
id: computing-software.systems-network-administration.backup-and-recovery.vss-writer-errors-in-vm-backups
name: vss-writer-errors-in-vm-backups
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [vss-writers, vssadmin, vss, guest-quiescing, application-consistent, windows]
level: advanced
status: gated
description: "Fix VSS errors that break application-consistent backups: read writer states with vssadmin, map writers to services, shadow storage, provider conflicts and event log IDs."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/vssadmin
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/volume-shadow-copy-service
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VSS writer errors in VM and agent backups

App-consistent backups (Veeam app-aware, VMware Tools quiescing, Hyper-V production
checkpoints, Windows Server Backup) depend on the guest's Volume Shadow Copy Service.

## Inspect
```cmd
vssadmin list writers          :: State and Last error per writer
vssadmin list providers        :: Microsoft Software Shadow Copy provider + any third-party
vssadmin list shadowstorage
vssadmin list shadows
```
Healthy: every writer `State: [1] Stable`, `Last error: No error`; anything else, or a writer missing from the list, needs investigation (gated: unconfirmed, source is paywalled or blocked); the state codes and error wording are not on the readable pages. Microsoft describes a writer as the component that makes data consistent for backup, and notes that a freeze may not last longer than 60 seconds and shadow copy creation no more than 10 seconds, or the shadow copy can be aborted.

## Writer → service to restart (gated: unconfirmed, source is paywalled or blocked)
| Writer | Service |
|---|---|
| SqlServerWriter | SQL Server VSS Writer (`SQLWriter`) |
| Microsoft Exchange Writer | Microsoft Exchange Information Store / Replication |
| NTDS | Active Directory Domain Services (restart only in a window) |
| Registry Writer, COM+ REGDB Writer, System Writer | Volume Shadow Copy (`VSS`), Cryptographic Services (`CryptSvc`) |
| WMI Writer | Windows Management Instrumentation (`Winmgmt`) |
| IIS Config / IIS Metabase Writer | Application Host Helper / IIS Admin |
| Hyper-V VSS writer (in guest: `vmicvss`) | Hyper-V Volume Shadow Copy Requestor |
Restart the owning service, re-run `vssadmin list writers`; writers reset to Stable.

## Common causes
- **Shadow storage too small or volume nearly full**: `vssadmin resize shadowstorage /for=C: /on=C: /maxsize=20GB`. `/maxsize` must be at least 1 MB with a unit (KB to EB); omitting it removes the limit, and resizing may make shadow copies disappear.
- Timeouts under heavy I/O: schedule backups off-peak; increase VSS timeouts in the backup product.
- **Third-party VSS providers** (hardware providers from storage vendors, old backup agents) can conflict with the built-in software provider: `vssadmin list providers` shows what is registered; remove leftovers you do not use.
- Too many shadow copies on a volume (gated: unconfirmed, source is paywalled or blocked); the per-volume limit is not on the readable pages.
- Corrupt WMI repository or registry permissions (System Writer missing): see event logs.

## Event logs
Check the Application log for sources `VSS`, `VolSnap`, `SQLWRITER` and `ESENT` (gated: unconfirmed, source is paywalled or blocked); specific event IDs are not on the readable pages. Correlate times with the backup job.

## Verify
`vssadmin list writers` all Stable with No error after a backup; backup job reports
application-aware processing succeeded; a manual `diskshadow` snapshot succeeds (the manual says only `add` and `create` are required, which makes a copy backup).

## Checked

Checked 2026-10-27 against Microsoft's Volume Shadow Copy Service overview, the vssadmin and diskshadow command pages (MicrosoftDocs/windowsserverdocs) and the VSS in-box writers page (MicrosoftDocs/win32). Confirmed: `vssadmin list writers` and `resize shadowstorage` syntax with its size units and warning, the 60 second writer freeze and 10 second shadow copy limits, hardware versus software providers, and that `diskshadow` needs only `add` and `create`. Gated: writer-state codes and error wording, the writer-to-service table, the per-volume shadow copy limit and the event IDs are not documented on pages readable for this check. Removed the percentage form of `/maxsize`, which the command page does not list.

Method: documentation only; no commands were run.
