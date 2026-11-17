---
id: computing-software.systems-network-administration.active-directory.non-authoritative-dc-restore
name: non-authoritative-dc-restore
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-recovery, non-authoritative-restore, dsrm, system-state-backup]
level: advanced
status: gated
description: "Restore a domain controller non-authoritatively from system state backup in DSRM, let partners replicate newer changes, and know when to rebuild instead."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wbadmin-start-systemstaterecovery
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-perform-nonauthoritative-restore
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/virtual-dc/restore-virtualized-domain-controller
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/virtualized-domain-controller-architecture
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/detect-and-recover-from-usn-rollback
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Non-authoritative DC restore

Use when a DC's database is corrupt or the server was rebuilt, and you want it back with the same name and role
holder data. Newer changes replicate in from partners after the restore.

## Restore or rebuild?
Rebuilding (demote/metadata cleanup, then promote a fresh DC) is often simpler and safer. Restore when the DC holds
something hard to recreate (FSMO in a single-DC site with slow links, AD-integrated apps tied to the name).

Restore a system state backup only within the **tombstone lifetime** (see dc-backup-strategy-and-tombstone-lifetime for
the defaults of 180 and 60 days).

## Steps
1. Boot into Directory Services Restore Mode (DSRM): `bcdedit /set safeboot dsrepair` then restart, and log on as
   `.\Administrator` with the DSRM password (gated: unconfirmed, source is paywalled or blocked). The current bcdedit
   reference does not list `dsrepair`; confirm the boot method on a test server.
2. Find versions and restore system state. The backup must contain system state explicitly; a full-server backup used
   for full server recovery does not work for this procedure.
```cmd
wbadmin get versions -backupTarget:E: -machine:<DC_NAME>
wbadmin start systemstaterecovery -version:10/17/2026-21:00 -backupTarget:E: -machine:<DC_NAME> -quiet
```
   `-version` is in MM/DD/YYYY-HH:MM format. `-machine` should be given whenever `-backupTarget` is. Add `-authsysvol`
   only when this DC must be the authoritative source for SYSVOL.
3. Clear safe boot and restart: `bcdedit /deletevalue safeboot` (gated: unconfirmed, source is paywalled or blocked).
4. After the restart the DC replicates newer changes in from its partners.

## Virtual DCs
On a hypervisor that exposes VM-GenerationID, restoring a snapshot or VM backup compares the current GenerationID with
the value in the database; if different, the invocation ID is reset and the RID pool is discarded, which prevents USN
reuse. Without that safeguard, rolling a DC back outside its awareness causes USN rollback (event 2095 is logged when it
is detected).

## After
```cmd
repadmin /showrepl
dcdiag /q
```
Check event **1109** (the InvocationID was updated after a restore) and the DFSR events 4614 and 4604 for SYSVOL.

## Verify
- [ ] Inbound replication succeeds on all partitions; SYSVOL shared; no USN rollback event 2095.

## Checked

Date: 2026-10-27. Documentation: wbadmin start systemstaterecovery and get versions references, AD Forest Recovery
non-authoritative restore page, Restore a virtual domain controller, Virtualized domain controller architecture, USN
rollback article, USN and InvocationID overview (MicrosoftDocs repositories, main branch).Confirmed: wbadmin syntax and `-authsysvol`, `-machine` guidance, the version format, system-state-only requirement,
GenerationID behaviour (invocation ID reset, RID pool discard), events 1109 and 2095, DFSR events 4614/4604.
Gated: the `bcdedit` safeboot values for entering and leaving DSRM.
Removed unconfirmed claims: "the only DC is authoritative by nature", the 2012+ hypervisor wording, and the statement
that SYSVOL is restored non-authoritatively by default.

Method: documentation only; no commands were run.
