---
id: computing-software.systems-network-administration.active-directory.force-ad-replication
name: force-ad-replication
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-replication, force-replication, repadmin, repadmin-syncall]
level: practitioner
status: docs-checked
description: "Push or pull AD replication on demand with repadmin /syncall, /replicate and Sync-ADObject, and read the results without making things worse."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc835086(v=ws.11)
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc742152(v=ws.11)
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc742123(v=ws.11)
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/sync-adobject
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/replication-error-8456-8457
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forcing AD replication

Use after an urgent change (disabled account, group membership for an incident) or to test a fixed link.

## Whole DC, all partitions, push to everyone
```cmd
repadmin /syncall <DC> /AdeP
```
- `A` all naming contexts held on the home server, `d` identify servers by distinguished name, `e` all sites in the
  enterprise (by default other sites are not synchronized), `P` push changes outward from the specified DC. Omit `P`
  to pull.
- `/q` suppresses call-back messages; keep output visible when troubleshooting.

## One partition between two DCs
```cmd
repadmin /replicate <DestDC> <SourceDC> "DC=corp,DC=example,DC=com"
```
`/force` overrides connections an administrator disabled with `repadmin /options` and allows replication with corrupt and
divergent partners; do not use it if you suspect a USN rollback. `/full` makes the source resend all changes (it resets
the up-to-dateness vector and high watermark, and does not remove lingering objects); use it only when a procedure
tells you to, and never with a suspected USN rollback.

## One object (fastest for incidents)
```powershell
Sync-ADObject -Object "CN=jdoe,OU=Users,DC=corp,DC=example,DC=com" -Source <DC-where-changed> -Destination <BranchDC>
```
Or `repadmin /replsingleobj <Dest> <Source> <ObjectDN>`.

## Reading results
- Error 1722 RPC unavailable, 1256, 8524 DNS lookup failure: connectivity or DNS, fix before retrying.
- Error 8456/8457: replication is disabled on the source or destination, by an administrator or automatically by the
  OS (USN rollback, full disk, corrupt UTD vector; see the `DSA not writable` registry value). Find out why before
  re-enabling.

## Don't
- Don't loop `/syncall` in scripts every few minutes; it masks topology problems and floods WAN links.
- Don't force replication from a DC suspected of USN rollback or lingering objects.

## Verify
```cmd
repadmin /showrepl <DestDC> /errorsonly
repadmin /showobjmeta <DestDC> "<ObjectDN>"
```
- [ ] Destination shows the new attribute version from the source.

## Checked
2026-10-27, against the repadmin /syncall, /replicate, /replsingleobj, /showrepl and /showobjmeta reference pages (Learn previous-versions, Windows Server 2012 R2) and the Sync-ADObject cmdlet page. Confirmed: /syncall switches A, d, e, P, q and the default of not crossing sites; /replicate /force and /full semantics and the USN-rollback warning; /replsingleobj syntax; /showrepl /errorsonly; Sync-ADObject -Object -Source -Destination; error 8456/8457 causes (SupportArticles-docs). Removed as unconfirmed: the "SyncAll terminated with no errors" string and the repadmin /options flag name. Corrected: /force overrides administrator-disabled connections, not an inter-site schedule.

Method: documentation only; no commands were run.
