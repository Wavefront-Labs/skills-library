---
id: computing-software.systems-network-administration.active-directory.rodc-staged-install
name: rodc-staged-install
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, rodc, read-only-domain-controller, rodc-deployment, rodc-staging, add-addsreadonlydomaincontrolleraccount, delegated-rodc-admin, branch-office, useexistingaccount, admin-role-separation]
level: practitioner
status: docs-checked
description: "Two-stage RODC deployment: pre-create the account with Add-ADDSReadOnlyDomainControllerAccount, delegate a local admin, let branch staff attach the server."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/rodc/install-a-windows-server-2012-active-directory-read-only-domain-controller--rodc---level-200-
  - https://learn.microsoft.com/en-us/powershell/module/addsdeployment/add-addsreadonlydomaincontrolleraccount
  - https://learn.microsoft.com/en-us/powershell/module/addsdeployment/install-addsdomaincontroller
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Staged RODC install

**Goal:** put a read-only DC in a branch where nobody holds Domain Admin, without shipping a
Domain Admin credential to the site.

## When an RODC fits
Physically insecure location, no local IT, poor WAN. It caches only the passwords you allow; accounts that cannot cache
and cannot reach a writable DC cannot use AD resources (see the PRP skill).

## Stage 1: Domain Admin pre-creates the account (HQ)
```powershell
Add-ADDSReadOnlyDomainControllerAccount -DomainControllerAccountName BR01-RODC `
  -DomainName ad.example.com -SiteName BRANCH01 `
  -DelegatedAdministratorAccountName 'AD\GG-BR01-RODC-Admins' `
  -AllowPasswordReplicationAccountName 'AD\GG-BR01-Users','AD\GG-BR01-Computers' `
  -InstallDns
```
`-DomainControllerAccountName`, `-DomainName` and `-SiteName` are required; `-Credential` is only needed if you are not
already a member of Domain Admins.
- The user or group in `-DelegatedAdministratorAccountName` can attach the server to the account and gains local
  administrative permissions on the RODC (privileges equivalent to the computer's Administrators group), without
  membership of Domain Admins or the domain built-in Administrators. Delegation is optional.
- `-AllowPasswordReplicationAccountName` and `-DenyPasswordReplicationAccountName` set the Password Replication Policy
  (see the PRP skill for the defaults).
- By default the RODC is a global catalog unless `-NoGlobalCatalog` is given.

## Stage 2: branch tech attaches the server
The server must reach a writable DC over the network for DNS and replication. A member of the delegated group (or a
Domain Admin) runs, on the server that has the AD DS role installed:
```powershell
Install-ADDSDomainController -DomainName ad.example.com -UseExistingAccount `
  -Credential (Get-Credential AD\br01-tech) `
  -SafeModeAdministratorPassword (Read-Host -AsSecureString) -Force
```
`-UseExistingAccount` attaches the server to the pre-created account. For slow links, install from media with
`-InstallationMediaPath` (and `-ReplicationSourceDC` / `-SystemKey` as needed); Microsoft's page describes creating RODC
IFM media with ntdsutil.

## Verify
- [ ] `Get-ADDomainController BR01-RODC | Select IsReadOnly,Site` shows True and the right site.
- [ ] The branch tech can manage the RODC but is not a member of Domain Admins.

## Checked

Documentation: Microsoft Learn "Install a Windows Server 2012 AD RODC (Level 200)" (staged and attach workflows, updated
2025-05) and the Add-ADDSReadOnlyDomainControllerAccount and Install-ADDSDomainController references, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: required parameters, delegation semantics (local admin equivalent, no Domain Admins), PRP parameters, global
catalog default, `-UseExistingAccount`, `-InstallationMediaPath`. Removed unconfirmed: the "writable 2008+ DC" and
application-compatibility remarks, `Install-WindowsFeature` line, the ntdsutil IFM command string, `dsmgmt` local roles,
RODC DNS behaviour and the `repadmin /showrepl` check.

Method: documentation only; no commands were run.
