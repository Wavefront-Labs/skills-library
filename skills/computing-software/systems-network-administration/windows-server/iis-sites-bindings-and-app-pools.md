---
id: computing-software.systems-network-administration.windows-server.iis-sites-bindings-and-app-pools
name: iis-sites-bindings-and-app-pools
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, iis, iis-administration, iis-bindings, application-pools, iisadministration-module, new-iissite, app-pool-identity, recycling]
level: practitioner
status: docs-checked
description: "Manage IIS sites, bindings and application pools with the IISAdministration module: create sites, host headers, app pool identities, recycling and safe config changes."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/iisadministration/
  - https://learn.microsoft.com/en-us/powershell/module/iisadministration/new-iissite
  - https://learn.microsoft.com/en-us/powershell/module/iisadministration/new-iissitebinding
  - https://learn.microsoft.com/en-us/iis/manage/configuring-security/application-pool-identities
  - https://learn.microsoft.com/en-us/powershell/module/webadministration/backup-webconfiguration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IIS sites, bindings and app pools with IISAdministration

## Install
Install the Web Server (IIS) role and the management tools, then:
```powershell
Import-Module IISAdministration     # newer module; WebAdministration is the older one
```
The module provides `Get-IISServerManager`, `Get-IISSite`, `Get-IISAppPool`, `New-IISSite`, `New-IISSiteBinding`,
`Get-IISSiteBinding`, `Remove-IISSiteBinding`, `Start-IISCommitDelay`/`Stop-IISCommitDelay` and
`Reset-IISServerManager`.

## Create a site and pool
```powershell
New-Item '<vol>:\Sites\shop' -ItemType Directory
$sm = Get-IISServerManager
$pool = $sm.ApplicationPools.Add('shop')
$pool.ManagedRuntimeVersion = ''           # No Managed Code (ASP.NET Core)
$pool.ProcessModel.IdentityType = 'ApplicationPoolIdentity'
$pool.Recycling.PeriodicRestart.Time = [TimeSpan]::Zero     # disable the 29-hour recycle
$pool.Recycling.PeriodicRestart.Schedule.Add([TimeSpan]'03:00:00') | Out-Null
$sm.CommitChanges()
New-IISSite -Name shop -PhysicalPath '<vol>:\Sites\shop' -BindingInformation '*:80:shop.example.com'
$sm = Get-IISServerManager; $sm.Sites['shop'].Applications['/'].ApplicationPoolName = 'shop'; $sm.CommitChanges()
```
- `New-IISSite` takes `-Name`, `-PhysicalPath`, `-BindingInformation` and optionally `-Protocol`,
  `-CertificateThumbPrint`, `-SslFlag`, `-CertStoreLocation` and `-Passthru`.
- Re-get the server manager after `CommitChanges()`; `Start-IISCommitDelay` and `Stop-IISCommitDelay` batch cmdlet
  changes into one commit.

## Bindings
Format `IP:port:hostheader`. HTTPS with SNI:
```powershell
New-IISSiteBinding -Name shop -BindingInformation '*:443:shop.example.com' -Protocol https `
  -CertificateThumbPrint <thumb> -CertStoreLocation 'Cert:\LocalMachine\My' -SslFlag Sni
Get-IISSiteBinding -Name shop
```
`-SslFlag` accepts None, Sni, CentralCertStore, DisableHTTP2, DisableOCSPStp, DisableQUIC, DisableTLS13 and
DisableLegacyTLS (combine with commas, for example `"Sni, CentralCertStore"`).

## Identities and permissions
- ApplicationPoolIdentity is the default for new pools (IIS 7.5 and later): WAS creates a virtual account named after
  the pool, `IIS AppPool\shop`. Add that identity to the ACL of content it needs:
  `icacls '<vol>:\Sites\shop' /grant 'IIS AppPool\shop:(OI)(CI)RX'`.
- For resources on other machines use a domain account (a gMSA is the usual choice) as the pool identity.

## Operations
```powershell
Get-IISAppPool
Get-IISSite
Backup-WebConfiguration -Name pre-change
```
Config lives in `%windir%\System32\inetsrv\config\applicationHost.config`.

## Verify
- [ ] A request to the site over its host name (hosts-file entry) returns 200 locally before the DNS change.

## Checked
Date 2026-10-27. Documentation: IISAdministration module index and New-IISSite, New-IISSiteBinding,
Get-IISSiteBinding pages, application pool identities page, Backup-WebConfiguration page. Confirmed: cmdlet names and
parameters, SslFlags values, default identity behaviour. ProcessModel and Recycling property names follow the IIS
configuration reference.
Method: documentation only; no commands were run.
