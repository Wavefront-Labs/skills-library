---
id: computing-software.systems-network-administration.active-directory.ad-recycle-bin-and-restore-adobject
name: ad-recycle-bin-and-restore-adobject
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-recovery, ad-backup, ad-recycle-bin, restore-adobject, enable-adoptionalfeature, deleted-objects, msds-deletedobjectlifetime]
level: practitioner
status: docs-checked
description: "Enable the AD Recycle Bin and restore deleted users, groups and OUs with Restore-ADObject or ADAC, including parent-first order and lifetime limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/adac/active-directory-recycle-bin
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/enable-adoptionalfeature
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/restore-adobject
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD Recycle Bin and Restore-ADObject

## Enable (forest-wide, irreversible)
Prerequisites from Microsoft: forest and domain functional level Windows Server 2008 R2 or higher, Domain Admins membership
in the domain, and ADAC or the AD PowerShell module. It is not enabled by default and cannot be disabled once enabled.
```powershell
Enable-ADOptionalFeature -Identity 'Recycle Bin Feature' -Scope ForestOrConfigurationSet -Target corp.example.com
```
Only objects deleted **after** enabling can be restored with the Recycle Bin; objects deleted before are not recoverable
this way. If you get an error, Microsoft suggests moving the schema master and domain naming master to the same DC in the
root domain and running the cmdlet there.

## Find and restore
```powershell
Get-ADObject -Filter 'isDeleted -eq $true -and samAccountName -eq "jsmith"' -IncludeDeletedObjects -Properties * |
  Select Name,LastKnownParent,whenChanged,ObjectGUID
Get-ADObject -Filter 'samAccountName -eq "jsmith"' -IncludeDeletedObjects | Restore-ADObject
# restore to a different place or name
Restore-ADObject -Identity <ObjectGUID> -NewName 'Kim Abercrombie' -TargetPath 'OU=Finance,OU=UserAccounts,DC=corp,DC=example,DC=com'
```
`Restore-ADObject` takes the object from `Get-ADObject ... -IncludeDeletedObjects` through the pipeline.
In ADAC you can also open the **Deleted Objects** container, select the objects and choose **Restore** or **Restore To**.
Microsoft states a restored user regains its group memberships and access rights as they were immediately before deletion.

## Deleted OU with children
Restore objects whose parent was deleted by filtering on `lastKnownParent` in the Deleted Objects container, as the
Restore-ADObject reference does for Configuration objects:
```powershell
Get-ADObject -Filter 'isDeleted -eq $true -and lastKnownParent -eq "OU=Sales,DC=corp,DC=example,DC=com"' `
  -IncludeDeletedObjects -SearchBase (Get-ADDomain).DeletedObjectsContainer | Restore-ADObject
```
Restore the OU itself first so its path exists again.

## Verify
- [ ] The restored user's group memberships are present (`Get-ADPrincipalGroupMembership`).

## Checked

Documentation: Microsoft Learn "Active Directory Recycle Bin" (prerequisites, enable, restore), and the
Enable-ADOptionalFeature and Restore-ADObject references, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: 2008 R2 prerequisite, irreversibility, Domain Admins requirement, the Enable-ADOptionalFeature call shape,
`-IncludeDeletedObjects | Restore-ADObject`, `-NewName`/`-TargetPath`, the lastKnownParent filter pattern, restore
regains memberships. Removed unconfirmed: `msDS-DeletedObjectLifetime` and the recycled-object lifetime description,
`Get-ADOptionalFeature` output check, the "parent does not exist" error text, the same-name-blocks-restore gotcha and the
`-Confirm:$false` switch.

Method: documentation only; no commands were run.
