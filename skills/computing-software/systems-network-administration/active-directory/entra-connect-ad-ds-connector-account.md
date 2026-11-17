---
id: computing-software.systems-network-administration.active-directory.entra-connect-ad-ds-connector-account
name: entra-connect-ad-ds-connector-account
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-connect, adsync-connector-account, set-adsyncpermissions, adsynctools, least-privilege]
level: advanced
status: docs-checked
description: "Create and lock down the Entra Connect AD DS connector account with Set-ADSyncPermissions: per-feature rights, AdminSDHolder hardening and password changes."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-configure-ad-ds-connector-account
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/reference-connect-accounts-permissions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Connect AD DS connector account permissions

With a custom installation you supply the account Entra Connect uses to read (and write back to) AD. Give it exactly
the rights its features need using the ADSyncConfig module shipped with Connect. Express installs create an
`MSOL_<number>` account with the needed rights; use the module mainly when inheritance is blocked or you pre-create the
account. Since build 1.4, an Enterprise Admin or Domain Admin cannot be used as the connector account.

## Load the module
```powershell
Import-Module "$env:ProgramFiles\Microsoft Azure Active Directory Connect\AdSyncConfig\AdSyncConfig.psm1"
Get-Command -Module AdSyncConfig
```
The module needs the RSAT AD DS tools. You can copy `AdSyncConfig.psm1` to a DC that has them, though some cmdlets only
run on the Connect server.

## Grant per feature
Every `Set-ADSync*Permissions` cmdlet accepts the account as `-ADConnectorAccountName` plus `-ADConnectorAccountDomain`,
or as `-ADConnectorAccountDN`. Without `-ADobjectDN` it sets the rights on the domain root; with `-ADobjectDN` only on
that object (not available for password hash sync, which is domain-root only). `-IncludeAdminSdHolders` also changes
AdminSDHolder and is not recommended.
```powershell
$dn = (Get-ADUser svc-aadc).DistinguishedName; $ou = 'OU=Corp,DC=ad,DC=example,DC=com'
Set-ADSyncBasicReadPermissions           -ADConnectorAccountDN $dn -ADobjectDN $ou
Set-ADSyncMsDsConsistencyGuidPermissions -ADConnectorAccountName svc-aadc -ADConnectorAccountDomain ad.example.com
Set-ADSyncPasswordHashSyncPermissions    -ADConnectorAccountName svc-aadc -ADConnectorAccountDomain ad.example.com
Set-ADSyncPasswordWritebackPermissions   -ADConnectorAccountDN $dn -ADobjectDN $ou
Set-ADSyncExchangeHybridPermissions      -ADConnectorAccountName svc-aadc -ADConnectorAccountDomain ad.example.com
```
Password hash sync grants Replicating Directory Changes and Replicating Directory Changes All on the domain root. Other
cmdlets in the module: `Set-ADSyncUnifiedGroupWritebackPermissions`, `Set-ADSyncExchangeMailPublicFolderPermissions`.

Inspect with `Get-ADSyncADConnectorAccount` (which account the AD connector uses),
`Get-ADSyncObjectsWithInheritanceDisabled -SearchBase '<DN>'` (objects that will not inherit the ACEs) and
`Show-ADSyncADObjectPermissions -ADobjectDN '<DN>'`.

## Harden the account
```powershell
$credential = Get-Credential   # an Enterprise or Domain Admin, different from the connector account
Set-ADSyncRestrictedPermissions -ADConnectorAccountDN $dn -Credential $credential
```
Disables inheritance on the connector account object and removes its ACEs except SELF, then grants Full Control to
SYSTEM, Enterprise Admins, Domain Admins and Administrators. Treat the account as Tier 0 when password hash sync is on,
because it holds replication rights.

## Verify
- [ ] Import, sync and export cycles run clean; `Get-ADSyncADConnectorAccount` shows the intended account.
- [ ] The account's ACL is restricted and it is not a member of Domain Admins or Enterprise Admins.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Connect AD DS connector account (ADSyncConfig) page and the
Connect accounts and permissions reference. Confirmed cmdlet names and parameters, the domain-root default, the
password hash sync rights, the restricted-permissions behaviour and the ban on Domain or Enterprise Admins as the
connector account. Removed the password-change procedure and the `stopped-credential` status name, which neither page
documents.
Method: documentation only; no commands were run.
