---
id: computing-software.systems-network-administration.active-directory.add-domain-controller-to-domain
name: add-domain-controller-to-domain
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-ds, install-addsdomaincontroller, additional-domain-controller, domain-controller-deployment, replica-dc, global-catalog, sitename, replicationsourcedc, addsdeployment, windows-server]
level: practitioner
status: docs-checked
description: "Add a replica DC to an existing domain with Install-ADDSDomainController: site, GC, DNS, replication source, prechecks and post-promotion replication checks."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/addsdeployment/install-addsdomaincontroller
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-a-replica-windows-server-2012-domain-controller-in-an-existing-domain--level-200-
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/upgrade-domain-controllers
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/move-addirectoryserver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Add a domain controller to an existing domain

**Goal:** a new writable DC that lands in the right site, replicates cleanly and serves DNS/GC.

## Preconditions
- Server with a static IP and its DNS client pointing at an existing healthy DC (the ADDSDeployment cmdlets
  expect a preferred DNS server to be configured first).
- Forest replication healthy *before* you start: `repadmin /replsummary` shows zero fails.
  Promoting into a broken forest copies the breakage.
- The subnet of the new DC's IP is mapped to the intended AD site, or pass `-SiteName`.
- Credentials: Domain Admins to add a DC to an existing domain. For the first DC running a newer Windows Server
  version, promotion runs adprep automatically and needs Enterprise Admins, Schema Admins and Domain Admins (of the
  domain that hosts the schema master); `-AdprepCredential` can supply them separately.

## Promote
```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
$p = @{
  DomainName                    = 'ad.example.com'
  SiteName                      = 'LON'
  InstallDns                    = $true
  NoGlobalCatalog               = $false
  ReplicationSourceDC           = 'dc01.ad.example.com'   # pick a near, healthy partner
  DatabasePath = '<DATA_DRIVE>:\NTDS'; LogPath = '<DATA_DRIVE>:\NTDS'; SysvolPath = '<DATA_DRIVE>:\SYSVOL'
  Credential                    = (Get-Credential AD\admin)
  SafeModeAdministratorPassword = (Read-Host -AsSecureString 'DSRM')
}
Test-ADDSDomainControllerInstallation @p
Install-ADDSDomainController @p -Force
```
Microsoft's guidance is to make a new DC a global catalog in most cases; the exceptions are limited WAN bandwidth
(use universal group membership caching instead) and the infrastructure master (do not co-locate it with a GC unless
every DC in the domain is a GC or the forest has a single domain).

For large databases or thin WAN links use install-from-media (`-InstallationMediaPath`) so
the initial copy comes from local disk.

## After promotion
```powershell
repadmin /showrepl <NEWDC>
repadmin /replsummary
dcdiag /s:<NEWDC> /q
Get-SmbShare -CimSession <NEWDC> | ? Name -in 'SYSVOL','NETLOGON'
```
SYSVOL must be shared (DFSR initial sync done: event 4604 in the DFS Replication log, preceded by 4614 while it
waits) before the DC advertises. If `SYSVOL`/`NETLOGON` stay missing, check DFSR events on the new DC and on its source
partner, in particular 2213 (dirty shutdown pause) on the partner.

## Gotchas
- Wrong site: the KCC builds topology around it; move it with
  `Move-ADDirectoryServer -Identity NEWDC -Site LON`.
- Expect long promotions on big directories; do not reboot mid-promotion.

## Verify
- [ ] `repadmin /replsummary` shows the new DC with zero failures both directions.
- [ ] SYSVOL and NETLOGON shared; `nltest /dsgetdc:ad.example.com /server:NEWDC` succeeds.
- [ ] DC is in the correct site and registered its SRV records.

## Checked

Date: 2026-10-27. Documentation: Install-ADDSDomainController and Move-ADDirectoryServer (Windows Server 2025 module
pages), the replica DC install page, Upgrade domain controllers, Planning global catalog placement, and the Microsoft
Support articles on missing SYSVOL/NETLOGON shares (all from MicrosoftDocs repositories, main branch).
Confirmed: all parameter names used above (`-AdprepCredential` on the replica install page), credential requirements for adding a DC and for adprep, automatic adprep
on promotion, GC placement exceptions, repadmin `/showrepl` and `/replsummary`, DFSR events 4614/4604/2213,
`Move-ADDirectoryServer -Identity -Site`.
Removed unconfirmed claims: DFSR event 4612, the "wait an hour" timing, the cloned/template-DC warning and the DNS
client ordering rule.

Method: documentation only; no commands were run.
