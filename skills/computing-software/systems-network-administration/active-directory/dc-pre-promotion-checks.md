---
id: computing-software.systems-network-administration.active-directory.dc-pre-promotion-checks
name: dc-pre-promotion-checks
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, dc-deployment, test-addsforestinstallation, dc-prerequisite-checks, test-addsdomaincontrollerinstallation]
level: practitioner
status: docs-checked
description: "Run Test-ADDSForestInstallation and Test-ADDSDomainControllerInstallation plus network, DNS and replication checks before promoting any domain controller."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/addsdeployment/test-addsdomaincontrollerinstallation
  - https://learn.microsoft.com/en-us/powershell/module/addsdeployment/test-addsforestinstallation
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/upgrade-domain-controllers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-promotion checks for domain controllers

**Goal:** promotion succeeds first time and the new DC is healthy, instead of a half-promoted box.

## Host checks (before installing the role)
- Static IPv4 address.
- DNS client points at an **existing healthy DC** for additional DCs (the ADDSDeployment cmdlets expect a preferred
  DNS server to be configured first).
- Hostname final; renaming after promotion is a separate procedure.
- Time in sync with the domain.
- Target server meets the system requirements and application compatibility has been reviewed; NTDS volume has
  space for database, logs and SYSVOL.
- Source DCs healthy: `dcdiag /e /q` and `repadmin /replsummary` are clean. Never add a DC into broken replication.
- FSMO connectivity: the machine running the install needs the infrastructure master for the first DC of a new
  Windows Server version (and the schema master for `adprep /forestprep`), the domain naming master to add or remove a
  domain, and the RID master for any DC install.
```powershell
Get-ADDomain | FL InfrastructureMaster, RIDMaster, PDCEmulator
Get-ADForest | FL DomainNamingMaster, SchemaMaster
```

## Install the role and run the built-in prerequisite tests
```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
# Additional DC
Test-ADDSDomainControllerInstallation -DomainName corp.example.com -SiteName HQ `
  -Credential (Get-Credential) -InstallDns -SafeModeAdministratorPassword (Read-Host -AsSecureString)
# New forest
Test-ADDSForestInstallation -DomainName corp.example.com -ForestMode WinThreshold -DomainMode WinThreshold -InstallDns
```
Each `Test-` cmdlet runs only the prerequisite checks for the matching `Install-` cmdlet and configures nothing; it
takes the same arguments (except `-SkipPreChecks`). Read every result row; DNS delegation warnings are expected when the
parent zone is not on Windows DNS.

## Common blockers and fixes
| Message | Fix |
|---|---|
| Could not contact a DC for the domain | DNS client wrong; `nltest /dsgetdc:corp.example.com` must succeed |
| adprep needs to run | promotion runs it automatically when the credentials qualify (Enterprise Admins, Schema Admins and Domain Admins for the first DC of a new version); otherwise run adprep separately |
| Domain does not meet the functional level | new forests and replica promotion with Windows Server 2025 need a functional level of Windows Server 2016 or later; remove old DCs and raise the level |
| Site not found | create the site and subnet first |

## Verify readiness
- [ ] `Test-` cmdlet reports success overall.
- [ ] DSRM password stored in the vault.
- [ ] Planned site and IFM media (for large DBs) decided before running `Install-ADDSDomainController`.

## Checked

Date: 2026-10-27. Documentation: Test-ADDSDomainControllerInstallation and Test-ADDSForestInstallation (Windows
Server 2025 module pages), AD DS install overview, Upgrade domain controllers, What's new in Windows Server 2025
(MicrosoftDocs repositories, main branch).
Confirmed: Test- cmdlet behaviour and arguments, preferred DNS server requirement, FSMO connectivity list and the two
Get-AD* commands, adprep credentials, `-ForestMode`/`-DomainMode WinThreshold` values, Windows Server 2025 functional
level floor, nltest `/dsgetdc`.
Removed unconfirmed claims: the IPv6 advice, `w32tm /stripchart` and the 5-minute figure, cumulative-update parity, the
firewall port list, the local-Administrator-password blocker and `New-ADReplicationSite`.

Method: documentation only; no commands were run.
