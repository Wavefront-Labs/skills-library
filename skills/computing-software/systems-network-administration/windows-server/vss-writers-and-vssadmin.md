---
id: computing-software.systems-network-administration.windows-server.vss-writers-and-vssadmin
name: vss-writers-and-vssadmin
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-server-backup, vss-writers, vssadmin, volume-shadow-copy, backup-troubleshooting, diskshadow, shadow-storage]
level: advanced
status: docs-checked
description: "Troubleshoot VSS-based backups: vssadmin list writers states, restarting writer services, shadow storage limits, diskshadow tests and common VSS errors."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/vssadmin
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/diskshadow
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/volume-shadow-copy-service
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/backup-and-storage/backup-fails-vss-writer
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/backup-and-storage/system-writer-not-found-in-backup
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/backup-and-storage/event-12289-vss-backup-restore
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/backup-and-storage/event-id-32-shadow-copies-are-unexpectedly-deleted
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VSS writers and vssadmin troubleshooting

Most Windows backup products (WSB, MARS, Veeam, DPM) depend on Volume Shadow Copy
Service. Writer failures = failed or inconsistent backups.

## Check writers
```powershell
vssadmin list writers          # each writer: State and Last error
vssadmin list providers        # registered providers
vssadmin list shadows
vssadmin list shadowstorage
vssadmin list volumes          # volumes eligible for shadow copies
```
Microsoft's examples show a healthy writer as `State: [1] Stable` with `Last error: No error`. Any writer that is
not stable, or shows an error, needs action: if any writer fails during the snapshot, the whole backup job fails.

## Writer notes
- **System Writer** is hosted by Cryptographic Services: `net stop cryptsvc` then `net start cryptsvc`, and re-run
  `vssadmin list writers`.
- **SQL Server writer** failures show up as SQLWRITER and SQLVDI errors in the Application log. Identify the failing
  instance from the first SQLVDI error, then stop that instance and re-run the backup to confirm; if no SQL instance is
  running, the SQL VSS writer is not used.
- Other writers belong to the service or application they represent: restart that service rather than the server, then
  re-run `vssadmin list writers` and retry the backup.

## Shadow storage
```powershell
vssadmin resize shadowstorage /for=E: /on=E: /maxsize=15%
vssadmin delete shadows /for=E: /oldest
```
`/maxsize` must be at least 1 MB and takes KB to EB units or a percentage; with no value there is no limit. When the
diff area runs out of space, shadow copies for the volume are deleted starting with the oldest. The diff area can be on
any local volume but must be NTFS with enough space. `vssadmin delete shadows` removes only client-accessible shadow
copies and deletion is permanent; use diskshadow for other types.
Event `volsnap` 32 (shadow copies aborted because the shadow copy storage volume was not present) can follow a restart
when phantom entries under `HKLM\SYSTEM\CurrentControlSet\Enum\STORAGE\VolumeSnapshot` slow enumeration; Microsoft's
workaround is the devnodeclean tool.

## Isolate with diskshadow
```
diskshadow
set context persistent
add volume E:
create
list shadows all
delete shadows all
```
If diskshadow succeeds, VSS is fine and the backup product is the problem.

## Common errors
- Event VSS 12289 about an older writer session state being removed (hr 0x80042409): stale writer session cleanup,
  logged for sessions older than two days; intermittent occurrences can be ignored, repeated ones point to a backup
  application not cleaning up sessions.
- Event VSS 8193 with access denied on `HKLM\SYSTEM\CurrentControlSet\Services\VSS\Diag` after installing the DHCP role
  does not stop VSS working; Microsoft documents a PowerShell ACL reset to avoid it.
- System Writer missing from `vssadmin list writers` or the backup: incorrect permissions on `%windir%\winsxs\filemaps`
  or `%windir%\winsxs\temp\PendingRenames` (Microsoft lists the takeown and icacls grants for SYSTEM, TrustedInstaller
  and Users, then a Cryptographic Services restart). Event VSS 8213 means the writer host runs under an account without
  access; check `HKLM\SYSTEM\CurrentControlSet\Services\VSS\VssAccessControl`.

## Verify
- [ ] All writers show Stable and No error after the fix; backup succeeds twice in a row.

## Checked

2026-10-27. Documentation release: windowsserverdocs vssadmin and diskshadow references, Volume Shadow Copy Service overview, and Support Articles on VSS writer failures, event 12289, event 32, event 8193 and System Writer not found (pages dated up to 2026-02-12). Confirmed: the vssadmin commands used, resize and delete behaviour, diff area rules, out-of-space deletion order, diskshadow create/list/delete commands, stable writer output, SQL and System Writer procedures, events 12289, 8193, 8213 and volsnap 32. Removed the writer-to-service table, the [8] Failed state, VolSnap 25/33 and error codes 0x8004230F and 0x80042306 as unconfirmed.

Method: documentation only; no commands were run.
