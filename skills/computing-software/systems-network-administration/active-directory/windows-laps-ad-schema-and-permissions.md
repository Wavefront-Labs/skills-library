---
id: computing-software.systems-network-administration.active-directory.windows-laps-ad-schema-and-permissions
name: windows-laps-ad-schema-and-permissions
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, windows-laps, laps, update-lapsadschema, set-lapsadcomputerselfpermission, set-lapsadreadpasswordpermission, find-lapsadextendedrights, mslaps-password, schema-update]
level: practitioner
status: docs-checked
description: "Prepare AD for Windows LAPS: extend the schema, grant computers self-write on their OU, delegate password read/reset to admin groups, and audit extended rights."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-scenarios-windows-server-active-directory
  - https://learn.microsoft.com/en-us/powershell/module/laps/update-lapsadschema
  - https://learn.microsoft.com/en-us/powershell/module/laps/set-lapsadreadpasswordpermission
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows LAPS: AD schema and permissions

Windows LAPS is built into supported Windows versions; no MSI. The `LAPS` PowerShell module ships in-box.

## 1. Extend the schema (once per forest)
```powershell
Import-Module LAPS
Update-LapsADSchema -Verbose
```
Adds `msLAPS-Password`, `msLAPS-EncryptedPassword`, `msLAPS-PasswordExpirationTime`,
`msLAPS-EncryptedPasswordHistory`, `msLAPS-EncryptedDSRMPassword` and related attributes to
computer objects. Independent from legacy LAPS attributes (`ms-Mcs-AdmPwd`).

## 2. Let computers write their own password
```powershell
Set-LapsADComputerSelfPermission -Identity 'OU=Servers,DC=ad,DC=example,DC=com'
Set-LapsADComputerSelfPermission -Identity 'OU=Workstations,DC=ad,DC=example,DC=com'
```
Run these on a Windows Server 2019 or later DC updated with Windows LAPS, or on a server that has the LAPS module.

## 3. Who can read and reset
```powershell
Set-LapsADReadPasswordPermission  -Identity 'OU=Servers,DC=ad,DC=example,DC=com' -AllowedPrincipals 'AD\GG-Tier1-Admins'
Set-LapsADResetPasswordPermission -Identity 'OU=Servers,DC=ad,DC=example,DC=com' -AllowedPrincipals 'AD\GG-Tier1-Admins'
```
- With **encryption enabled** (recommended; needs domain functional level 2016 or later), only the principal set by `ADPasswordEncryptionPrincipal` (the authorized decryptor) can decrypt; the default when not configured is Domain Admins.
- Domain Admins have password query permission by default.

## 4. Audit who else can read
Users with the extended rights permission on the OU can read confidential attributes, and all Windows LAPS password attributes are confidential:
```powershell
Find-LapsADExtendedRights -Identity 'OU=Servers,DC=ad,DC=example,DC=com'
```
Remove broad extended rights from helpdesk/delegation groups.

## Verify
- [ ] `Get-ADObject (Get-ADRootDSE).schemaNamingContext -Filter "name -like 'ms-LAPS*'"` lists the new attributes.
- [ ] `Find-LapsADExtendedRights` shows only intended principals.

## Checked
Checked 2026-10-27 against Microsoft Learn (Get started with Windows LAPS and Windows Server Active Directory; Windows LAPS technical reference; Update-LapsADSchema, Set-LapsADComputerSelfPermission, Set-LapsADReadPasswordPermission and Find-LapsADExtendedRights references, Windows Server 2025).
- Confirmed: schema update is a one-time forest operation; attribute names msLAPS-Password, msLAPS-EncryptedPassword, msLAPS-PasswordExpirationTime, msLAPS-EncryptedPasswordHistory, msLAPS-EncryptedDSRMPassword and the legacy mapping; cmdlet names and the -Identity and -AllowedPrincipals parameters; encryption needs DFL 2016; ADPasswordEncryptionPrincipal defaults to Domain Admins; Domain Admins can query by default; extended rights expose confidential attributes.
- Removed: the April 2023 update claim, the Schema Admins statement and OU inheritance remark, none confirmed.

Method: documentation only; no commands were run.
