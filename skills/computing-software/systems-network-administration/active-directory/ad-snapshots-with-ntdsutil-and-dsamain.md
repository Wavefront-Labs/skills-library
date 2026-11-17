---
id: computing-software.systems-network-administration.active-directory.ad-snapshots-with-ntdsutil-and-dsamain
name: ad-snapshots-with-ntdsutil-and-dsamain
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-recovery, ad-backup, ad-snapshot, dsamain, ntdsutil-snapshot, attribute-recovery, ldap-mount]
level: advanced
status: docs-checked
description: "Create AD DS snapshots with ntdsutil, mount them with dsamain as a read-only LDAP instance, compare and recover lost attribute values."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc753609(v=ws.10)
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc731620(v=ws.10)
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# AD snapshots with ntdsutil and dsamain

Snapshots let you look at AD as it was (for example before someone modified or deleted data) without restoring a DC. The
mounting tool lets you compare data from snapshots taken at different times so you can decide what to restore, without
restoring several backups and without restarting in DSRM.

## Take snapshots
```cmd
ntdsutil "activate instance ntds" snapshot create quit quit
ntdsutil snapshot "list all" quit quit
```
You need Enterprise Admins, Domain Admins or delegated permission. You can schedule a task that runs ntdsutil
regularly. Snapshots are VSS snapshots of the volume holding the AD database; any consistent VSS backup of the database
(including non-Microsoft ones) also works with dsamain, and so does a restored `ntds.dit`.

## Mount and expose
```cmd
ntdsutil snapshot "list all" "mount {GUID}" quit quit
dsamain /dbpath <MOUNT_PATH>\Windows\NTDS\ntds.dit /ldapport 50000
```
The mounted snapshot appears under a path of the form `$SNAP_<timestamp>_VOLUME<letter>$`. Leave dsamain running; it
exposes the data read-only over LDAP. By default the file is opened read-only, ASCII paths only, no network share paths.
Only the LDAP port is required; the LDAP-SSL, GC and GC-SSL ports default to LDAP port plus 1, 2 and 3. Use different
ports to browse several snapshots side by side. By default only Domain Admins and Enterprise Admins can view the
data (the `/allowNonAdminAccess` switch is for snapshots of a deleted domain or forest).

## Query and compare
```powershell
Get-ADGroupMember -Identity 'Finance-RW' -Server dc01:50000
Get-ADUser jsmith -Server dc01:50000 -Properties * | Select title,department,manager
```
You can also browse with Ldp.exe or Active Directory Users and Computers connected to the snapshot port. Data is
read-only: add, modify and delete fail. Re-apply old values to production with `Set-ADUser` or `Add-ADGroupMember`.
Deleted objects can be re-created from snapshot data, but stripped attributes and back links must be re-created by hand.

## Clean up
Press Ctrl+C in the dsamain window (or set the `stopservice` attribute on the rootDSE if running it remotely), then
`ntdsutil snapshot "unmount {GUID}" "delete {GUID}" quit quit`.

## Gotchas
- Snapshots contain sensitive AD data; protect them like DC backups (encryption, restricted access), because
  permissions in the data are enforced but copies can be examined from another forest.
- Dsamain permissions: all permissions that apply to the data in the snapshot are enforced on read.

## Verify
- [ ] Mount the latest snapshot and query a known object from the snapshot port.

## Checked

Date: 2026-10-27. Documentation: "Active Directory Domain Services Database Mounting Tool (Snapshot Viewer or Snapshot
Browser) Step-by-Step Guide" and the ntdsutil `snapshot` reference (Windows Server 2008 / 2008 R2 archive pages; no
current-release page was readable).
Confirmed: `activate instance ntds snapshot create`, `list all`, `mount`, `unmount`, `delete`, `dsamain /dbpath
/ldapport` syntax, port defaults, read-only behaviour, permissions, `/allowNonAdminAccess`, stopping dsamain, security
guidance, and `-Server` accepting a snapshot instance as `host:port` (AD module reference).
Removed unconfirmed claims: the "$SNAP" example date and `-dbpath` dash syntax, the firewall note, the daily-schedule
advice and the shared-shadow-storage sentence.

Method: documentation only; no commands were run.
