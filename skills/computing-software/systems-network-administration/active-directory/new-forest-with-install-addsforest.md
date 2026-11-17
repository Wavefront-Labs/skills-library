---
id: computing-software.systems-network-administration.active-directory.new-forest-with-install-addsforest
name: new-forest-with-install-addsforest
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-ds, install-addsforest, new-forest, domain-controller-deployment, dcpromo, forest-root, functional-level, dsrm, dns-delegation, addsdeployment, windows-server]
level: practitioner
status: docs-checked
description: "Stand up a new AD forest root with Install-ADDSForest: naming, functional levels, integrated DNS, DSRM password, test first, and post-promotion checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-
  - https://learn.microsoft.com/en-us/powershell/module/addsdeployment/install-addsforest
  - https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/adac/active-directory-recycle-bin
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# New forest root with Install-ADDSForest

**Goal:** a first domain controller for a new forest that you will not regret in ten years.

## Decide before you type
- **Name:** use a subdomain of a public domain you own (`ad.example.com`), never `.local`
  or a name you do not control. Treat the DNS name as fixed for the life of the forest.
- **NetBIOS name:** 15 characters maximum; users see it in `DOMAIN\user`.
- **Functional level:** the highest that every future DC OS supports. Windows Server 2025 requires a new
  forest to be at Windows Server 2016 functional level or later; `WinThreshold` is the 2016 value in the cmdlet.
  The install page's example uses `-ForestMode Win2025` for the 2025 level (the cmdlet reference page lists values
  only up to `WinThreshold`). Windows Server 2019 and 2022 have no newer level than 2016.
- **Server:** static IP, correct hostname set *before* promotion, time source sane, patched.

## Install and test
```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Import-Module ADDSDeployment
$p = @{
  DomainName                    = 'ad.example.com'
  DomainNetbiosName             = 'EXAMPLE'
  ForestMode                    = 'WinThreshold'
  DomainMode                    = 'WinThreshold'
  InstallDns                    = $true
  DatabasePath                  = '<DATA_DRIVE>:\NTDS'
  LogPath                       = '<DATA_DRIVE>:\NTDS'
  SysvolPath                    = '<DATA_DRIVE>:\SYSVOL'
  SafeModeAdministratorPassword = (Read-Host -AsSecureString 'DSRM password')
  NoRebootOnCompletion          = $false
}
Test-ADDSForestInstallation @p      # prerequisite check, changes nothing
Install-ADDSForest @p -Force
```
- To install a new forest you log on as the local Administrator of the server.
- On Azure VMs put NTDS/SYSVOL on a data disk with host caching **None**.
- If the parent zone is not on Windows DNS, create the DNS delegation yourself when clients outside the forest need
  to resolve the new namespace.
- Record the DSRM password in your vault; you need it for restores. For an in-line password, do not store clear
  text in scripts: a DSRM password lets someone impersonate the DC.

## After the reboot
```powershell
Get-ADDomainController -Discover
dcdiag /v /c /e /q              # only errors printed
Get-Service NTDS,DNS,Netlogon,KDC,DFSR | ft Name,Status
Resolve-DnsName _ldap._tcp.dc._msdcs.ad.example.com -Type SRV
```
With Active Directory-integrated DNS, the first DC's preferred DNS server is set to loopback (`127.0.0.1`)
automatically. Then consider enabling the AD Recycle Bin (irreversible once enabled):
```powershell
Enable-ADOptionalFeature -Identity 'CN=Recycle Bin Feature,CN=Optional Features,CN=Directory Service,CN=Windows NT,CN=Services,CN=Configuration,DC=ad,DC=example,DC=com' -Scope ForestOrConfigurationSet -Target 'ad.example.com'
```
Create sites and subnets, and add a second DC promptly: one DC is a single point of failure.

## Verify
- [ ] `dcdiag` passes with no failures.
- [ ] SRV records exist in `_msdcs`.
- [ ] Recycle Bin decision recorded, second DC planned or built.

## Checked

Date: 2026-10-27. Documentation: Install-ADDSForest (Windows Server 2025 module page), the AD DS install overview
(updated for 2025), What's new in Windows Server 2025, Active Directory Recycle Bin page (MicrosoftDocs repositories,
main branch).
Confirmed: parameter names, `WinThreshold`/`Win2025` usage as above, local-Administrator requirement, Test- cmdlet
behaviour, first-DC loopback DNS setting with AD-integrated DNS, Recycle Bin command shape and irreversibility,
2016 functional-level floor for 2025 DCs.
Removed unconfirmed claims: the domain-rename and "cannot lower level" statements, the NetBIOS "no dots" rule, the
PDC/NTP advice, the sysprep/duplicate-SID warning, event 4013 behaviour and the local-Administrator-password rule.

Method: documentation only; no commands were run.
