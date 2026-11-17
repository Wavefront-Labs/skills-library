---
id: computing-software.systems-network-administration.windows-server.delegate-gpo-management
name: delegate-gpo-management
category: computing-software
field: systems-network-administration
product: windows-server
tags: [group-policy, gpo, gpo-delegation, group-policy-creator-owners, delegation-of-control]
level: practitioner
status: docs-checked
description: "Delegate GPO creation, editing and linking separately: Group Policy Creator Owners, per-GPO edit rights, gPLink rights on OUs and WMI filter permissions."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/grouppolicy/set-gppermission
  - https://learn.microsoft.com/en-us/powershell/module/grouppolicy/get-gppermission
  - https://learn.microsoft.com/en-us/powershell/module/grouppolicy/get-gpinheritance
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-scope
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delegating GPO management

Three separate rights, often confused:

| Right | Where it lives | How to grant |
|---|---|---|
| Create GPOs | Group Policy Objects container in the domain | GPMC > Group Policy Objects > Delegation tab, or membership of Group Policy Creator Owners |
| Edit a GPO | the GPO's ACL | `Set-GPPermission` (levels such as `GpoRead`, `GpoApply`, `GpoEdit`, `GpoEditDeleteModifySecurity`) |
| Link GPOs to a site, domain or OU | the *modify* permission on that container (by default only Domain Admins and Enterprise Admins hold it) | GPMC > container > Delegation tab |

## Patterns
```powershell
# Desktop team can edit only its own GPOs
Set-GPPermission -Name 'WKS - Browser Settings' -TargetName 'GP-Desktop-Editors' -TargetType Group -PermissionLevel GpoEdit
# Read-only reviewers
Set-GPPermission -All -TargetName 'GP-Auditors' -TargetType Group -PermissionLevel GpoRead
# Who can do what on a GPO
Get-GPPermission -Name 'WKS - Browser Settings' -All
```
- Anyone who can link GPOs to a container can also change link order and set block inheritance there.
- WMI filters have their own permission levels (`WmiFilterEdit`, `WmiFilterFullControl`, `WmiFilterCustom`), granted separately from GPO rights.

## Tier 0 rule
GPOs linked to the Domain Controllers OU or domain root are Tier 0. Limit their edit rights to Tier 0 admins, because
they change the configuration of every domain controller. Audit:
```powershell
(Get-GPInheritance -Target "OU=Domain Controllers,$((Get-ADDomain).DistinguishedName)").InheritedGpoLinks |
  ForEach-Object { $g = Get-GPO -Guid $_.GpoId; Get-GPPermission -Guid $_.GpoId -All |
  Where-Object Permission -in 'GpoEdit','GpoEditDeleteModifySecurity' |
  Select @{n='GPO';e={$g.DisplayName}},Trustee,Permission }
```

## Verify
- [ ] Delegated team can edit their GPOs and link to their OU, cannot edit DC-linked GPOs.
- [ ] Group Policy Creator Owners membership reviewed.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed: Set-GPPermission parameters (-Name, -All, -TargetName, -TargetType Computer/User/Group, -PermissionLevel values including GpoEdit, GpoRead, GpoEditDeleteModifySecurity, WmiFilterEdit, WmiFilterFullControl), Get-GPPermission -All, Get-GPInheritance InheritedGpoLinks, and that linking requires modify permission on the site, domain or OU (default Domain Admins and Enterprise Admins) and also allows link order and block inheritance changes. Fixed: the audit snippet used a DisplayName property that permission objects do not carry, so the GPO name now comes from Get-GPO. Removed as unconfirmed: gPLink and gPOptions attribute names, the Creator Owners ownership behaviour and the SYSTEM code execution wording.

Method: documentation only; no commands were run.
