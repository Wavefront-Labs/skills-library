---
id: computing-software.systems-network-administration.active-directory.rodc-administrator-role-separation
name: rodc-administrator-role-separation
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, rodc, rodc-admin-role-separation, dsmgmt, delegated-administration]
level: advanced
status: gated
description: "Delegate local admin rights on an RODC without domain admin: ManagedBy during staging and dsmgmt local roles, plus what the delegated admin can and cannot do."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/rodc/install-a-windows-server-2012-active-directory-read-only-domain-controller--rodc---level-200-
  - https://learn.microsoft.com/en-us/powershell/module/addsdeployment/add-addsreadonlydomaincontrolleraccount
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RODC administrator role separation

Branch staff need to patch and reboot the RODC; they must not become Domain Admins. RODCs support local
administrators that have no rights in AD.

## Option 1: set at staging time
```powershell
Add-ADDSReadOnlyDomainControllerAccount -DomainControllerAccountName BR01-RODC `
  -DomainName corp.example.com -SiteName Branch01 -DelegatedAdministratorAccountName 'CORP\BR01-RODC-Admins'
```
The delegated administrator account gets local administrative permissions on the RODC and is not a member of Domain Admins or the domain Builtin Administrators group. Delegation is optional. The group lands in the RODC computer object's `managedBy` attribute (gated: unconfirmed, source is paywalled or blocked). Use a **group**, not a user, so staff changes do not need a domain admin.

## Option 2: change later
- ADUC or ADAC, RODC computer object, **Managed By** tab, set group (gated: unconfirmed, source is paywalled or blocked).
- Legacy local roles with dsmgmt on the RODC (gated: unconfirmed, source is paywalled or blocked):
```cmd
dsmgmt
local roles
add CORP\BR01-RODC-Admins administrators
show role administrators
quit
quit
```

## What the delegated admin gets
- Privileges equivalent to the local Administrators group on that RODC.
- No membership in Domain Admins or the domain built-in Administrators group.

## Rules
- Keep the delegated group's members out of privileged groups.
- Do not add the group to Builtin\Administrators on the domain (that is domain-wide on writable DCs).
- Review `managedBy` on all RODCs quarterly:
```powershell
Get-ADDomainController -Filter {IsReadOnly -eq $true} | ForEach-Object {
  Get-ADComputer $_.Name -Properties managedBy | Select Name,managedBy }
```

## Verify
- [ ] A member of the group can sign in to the RODC and restart a service.
- [ ] The same account has no rights over domain objects (not in Domain Admins or domain Builtin Administrators).

## Checked
Checked 2026-10-27 against Microsoft Learn (Install an RODC, Windows Server 2012 article; Add-ADDSReadOnlyDomainControllerAccount and Get-ADDomainController references, Windows Server 2025).
- Confirmed: Add-ADDSReadOnlyDomainControllerAccount -DelegatedAdministratorAccountName; delegated accounts get local-administrator-equivalent rights without Domain Admins or domain Builtin Administrators membership; delegation is optional; Get-ADDomainController -Filter "IsReadOnly -eq $true" pattern.
- Gated: the managedBy attribute mapping, the Managed By tab and the dsmgmt local roles procedure. Reason: only previous-versions pages cover them and they could not be read.
- Removed: Windows Server Backup rights, other-DC logon and password-cache remarks that no readable page covers.

Method: documentation only; no commands were run.
