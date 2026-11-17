---
id: computing-software.systems-network-administration.active-directory.move-and-rename-ad-objects
name: move-and-rename-ad-objects
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-users-and-groups, move-adobject, rename-adobject, protect-from-accidental-deletion]
level: practitioner
status: docs-checked
description: "Move and rename users, groups, computers and OUs with Move-ADObject and Rename-ADObject, handling deletion protection, GPO scope changes and SAM names."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/move-adobject
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/rename-adobject
  - https://learn.microsoft.com/en-us/powershell/module/grouppolicy/get-gpinheritance
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/rename-computer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Moving and renaming AD objects

## Move
```powershell
Get-ADUser jdoe | Move-ADObject -TargetPath "OU=Leavers,DC=corp,DC=example,DC=com"
# Bulk: all disabled computers to a quarantine OU
Search-ADAccount -AccountDisabled -ComputersOnly -SearchBase "OU=Workstations,DC=corp,DC=example,DC=com" |
  Move-ADObject -TargetPath "OU=Disabled,DC=corp,DC=example,DC=com" -WhatIf
```
- A protected OU (`ProtectedFromAccidentalDeletion`) cannot be deleted without clearing the flag. If a move of a
  protected OU or object is denied, clear the flag first
  (`Set-ADOrganizationalUnit <OU> -ProtectedFromAccidentalDeletion $false`), move, then set it back.
- A move changes which **GPOs and delegations** apply. Check with `Get-GPInheritance -Target <new OU>` first;
  moving a server OU under a workstation-hardening GPO can break services.

## Rename
`Rename-ADObject` renames the object by setting its **Name** property (the CN/RDN in the tree):
```powershell
Get-ADUser jdoe | Rename-ADObject -NewName "Jane Doe"
```
The logon names are separate attributes:
```powershell
Set-ADUser jdoe -SamAccountName jsmith -UserPrincipalName jsmith@example.com -DisplayName "Jane Smith" -Surname Smith
```
For a surname change also update `mail`/`proxyAddresses` via Exchange or the sync source.

## Computers
Do not rename computer objects in AD directly; rename the machine
(`Rename-Computer -NewName X -DomainCredential <DOMAIN>\<admin>`) using credentials that may rename it in the domain.

## Cross-domain moves
`Move-ADObject` can move an object or container between domains of the same forest: use `-TargetServer` with the
fully qualified name of a DC in the target domain; both the source DC and the target DC must be the RID master of
their domains, otherwise the move fails with "the directory service is not the master for that type of operation".
User and computer passwords move with the object. Between forests use a migration tool such as ADMT.

## Verify
- [ ] `Get-ADObject <guid>` shows the new DN on more than one DC.
- [ ] GPO result on a moved computer is as expected.

## Checked
2026-10-27. Documentation: Microsoft Learn `Move-ADObject`, `Rename-ADObject`, `Get-GPInheritance` and
`Rename-Computer` references (Windows Server 2025 docset). Confirmed: `-TargetPath`, `-TargetServer`, cross-domain moves within
a forest, the RID-master requirement and its error text, and that passwords move; `Rename-ADObject` sets the Name property;
`Get-GPInheritance -Target`; `Rename-Computer -NewName -DomainCredential`. Corrected: the draft said Move-ADObject works within one
domain only, which is wrong. Removed as unconfirmed: the exact deny-ACE description of the protection flag, the SPN/DNS
follow-through claim and the cached-credentials remark; the repadmin /showobjmeta verify step was replaced.
Method: documentation only; no commands were run.
