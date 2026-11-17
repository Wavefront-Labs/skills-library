---
id: computing-software.systems-network-administration.active-directory.delegated-managed-service-accounts
name: delegated-managed-service-accounts
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, dmsa, delegated-managed-service-accounts, windows-server-2025, service-accounts]
level: advanced
status: docs-checked
description: "Windows Server 2025 delegated MSAs: migrating a legacy service account to a dMSA, how the machine-bound key works, and the permissions risk to lock down."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/delegated-managed-service-accounts/delegated-managed-service-accounts-overview
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/delegated-managed-service-accounts/delegated-managed-service-accounts-set-up-dmsa
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delegated managed service accounts (dMSA)

**What:** a Windows Server 2025 account type that can **replace an existing legacy service account** (a normal account
with a static password) without reconfiguring every service. Microsoft describes dMSAs as authenticating specific
machine identities mapped in AD, with secrets derived from the machine account credential and held by the DC; the secret
can be protected further with Credential Guard. Legacy accounts are disabled after migration, which helps against
credential harvesting from a compromised account (kerberoasting).

## Requirements (from the setup page)
- The AD DS role and a domain controller; Windows Server 2025 is the documented platform.
- Membership of Domain Admins or Enterprise Admins (or equivalent AD permissions) to create or migrate to a dMSA.
- A **KDS root key** generated on the DC before a dMSA is created or migrated (`Get-KdsRootKey` to check;
  `Add-KdsRootKey -EffectiveTime ((get-date).addhours(-10))` as shown in the page for the key).
- A two-way forest trust between forests for cross-domain and cross-forest scenarios.
- On the client, to use the dMSA as a standalone MSA or to supersede a legacy account, the page sets the registry
  DWORD `DelegatedMSAEnabled` = 1 under `HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Kerberos\Parameters`.

## Create a standalone dMSA
```powershell
New-ADServiceAccount -Name dmsaPayroll -DNSHostName dmsaPayroll.ad.example.com `
  -CreateDelegatedServiceAccount -KerberosEncryptionType AES256
Set-ADServiceAccount -Identity dmsaPayroll -PrincipalsAllowedToRetrieveManagedPassword 'HOST01$'
```
For standalone use the page also requires the `msDS-DelegatedMSAState` attribute of the dMSA to be set to 3 (it does
this with Set-ADServiceAccount; check the attribute with `Get-ADServiceAccount -Properties msDS-DelegatedMSAState`).

## Migrate a legacy account
```powershell
Start-ADServiceAccountMigration -Identity dmsaPayroll -SupersededAccount '<DN of legacy account>'
# restart the running services that use the account, then finish
Complete-ADServiceAccountMigration -Identity dmsaPayroll -SupersededAccount '<DN of legacy account>'
# wrong account: undo everything done during migration
Undo-ADServiceAccountMigration -Identity dmsaPayroll -SupersededAccount '<DN of legacy account>'
# return to an inactive/unlinked state
Reset-ADServiceAccountMigration -Identity dmsaPayroll -SupersededAccount '<DN of legacy account>'
```
`Start-` links the accounts (state 1; the legacy account's access carries over via attributes such as
`msDS-ManagedAccountPrecededByLink`), `Complete-` marks migration complete (state 2) and disables the traditional
account. Microsoft's warning: when finalizing, **never delete the original service account**, in case you need to
revert. If the legacy account was used on several devices, update `PrincipalsAllowedToRetrieveManagedPassword`
manually after migration. Migration needs access to a read-write DC; unconstrained delegation on the old account
stops working after migration.

## Events
Enable the Microsoft-Windows-Security-Kerberos/Operational log (disabled by default): event 307 dMSA migration, 308
dMSA permission add, 309 dMSA key fetch.

## Verify
- [ ] The legacy account is disabled and services run as the dMSA.
- [ ] Only the intended principals can create or migrate dMSAs (the docs require Domain Admins or Enterprise Admins or
  equivalent for these operations; review delegated permissions accordingly).

## Checked

Documentation: Microsoft Learn "Delegated Managed Service Accounts overview in Windows Server 2025" and "Set up
delegated managed service accounts", from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: the New-/Set-/Start-/Complete-/Undo-/Reset-ADServiceAccount(Migration) commands and parameters, the
`DelegatedMSAEnabled` registry value, KDS root key requirement, msDS-DelegatedMSAState values, event IDs 307-309, the
never-delete warning. Wrong or removed: the object class name, the claim that Undo applies without `-SupersededAccount`,
and the third-party "BadSuccessor" security section (not covered by the docs repo, so not confirmed here; review
current Microsoft security guidance on who may create dMSAs).

Method: documentation only; no commands were run.
