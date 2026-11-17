---
id: computing-software.systems-network-administration.active-directory.dc-post-promotion-verification
name: dc-post-promotion-verification
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, dc-deployment, dc-post-promotion-checks, sysvol, netlogon, dcdiag]
level: practitioner
status: docs-checked
description: "After promoting a DC, confirm SYSVOL and NETLOGON shares, SRV registration, replication, GC status and DNS settings before trusting it."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dcdiag
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/troubleshoot-missing-sysvol-and-netlogon-shares
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/verify-srv-dns-records-have-been-created
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/move-addirectoryserver
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Post-promotion verification of a new DC

A DC that answers LDAP but has no SYSVOL share will hand out empty Group Policy. Check before you point clients at it.

## 1. Shares and SYSVOL initial sync
```cmd
net share | findstr /i "SYSVOL NETLOGON"
dcdiag /s:<NEWDC> /test:sysvolcheck /test:netlogons
```
`SysVolCheck` reads the Netlogon `SysvolReady` registry value (must be 1; works for FRS or DFSR) and `NetLogons` checks
the shares can be read. Missing shares mean DFSR initial sync has not finished. Check:
```powershell
Get-WinEvent -LogName 'DFS Replication' -MaxEvents 20 | Format-Table TimeCreated,Id,Message -Wrap
```
Event **4614** = waiting for initial synchronization, **4604** = SYSVOL initialised. A DC that logs 4614 without 4604
is waiting on its source partner: check the partner's DFSR (for example event 2213, dirty shutdown pause) and fix that,
rather than editing the registry by hand.

## 2. DNS registration
```cmd
dcdiag /test:dns /DnsRecordRegistration /s:<NEWDC>
nltest /dsgetdc:corp.example.com /force
```
`%SystemRoot%\System32\config\netlogon.dns` lists the SRV and other records the DC should register; every record
there should exist in DNS. Registered locator records are under `_msdcs` in the domain zone.

## 3. Replication
```cmd
repadmin /showrepl <NEWDC>
repadmin /replsummary
```
All partitions the DC holds should show successful inbound replication.

## 4. Roles and placement
- Global catalog if planned: `Get-ADDomainController <NEWDC> | Format-List *` and check the global catalog and site
  properties.
- Correct site; move with `Move-ADDirectoryServer -Identity <NEWDC> -Site <SITE>` if placement chose wrong.
- DNS client settings on the new DC match your DNS design and point at working DNS servers.

## 5. Health and backup
```cmd
dcdiag /s:<NEWDC> /q
```
Add to monitoring and system-state backup the same day.

## Verify
- [ ] SYSVOL and NETLOGON shared; `dcdiag` SysVolCheck and NetLogons pass.
- [ ] dcdiag quiet, repadmin clean.
- [ ] Site, GC and DNS client settings match the design.

## Checked

Date: 2026-10-27. Documentation: dcdiag command reference, Microsoft Support "missing SYSVOL and NETLOGON shares"
and "verify SRV records" articles, repadmin and nltest references (Windows Server 2012 R2 / 2008 R2 archive pages),
Move-ADDirectoryServer (Windows Server 2025 module page).
Confirmed: `SysVolCheck` and `NetLogons` tests and the SysvolReady value, DFSR events 4614/4604/2213, netlogon.dns
location, `dcdiag /test:dns /DnsRecordRegistration`, `repadmin /showrepl` and `/replsummary`, `nltest /dsgetdc /force`,
`Move-ADDirectoryServer`.
Removed unconfirmed claims: the `net stop netlogon`/`ipconfig /registerdns` sequence, the partition list and the
"flip SysvolReady by hand" wording.

Method: documentation only; no commands were run.
