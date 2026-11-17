---
id: computing-software.systems-network-administration.active-directory.protect-ous-from-accidental-deletion
name: protect-ous-from-accidental-deletion
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ou-delegation, protect-from-accidental-deletion, protectedfromaccidentaldeletion, deny-delete, ou-design, recycle-bin, set-adorganizationalunit]
level: intro
status: docs-checked
description: "Turn on ProtectedFromAccidentalDeletion for every OU (and key objects), understand the deny ACE it adds, and how to remove an OU deliberately."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-adorganizationalunit
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/remove-adorganizationalunit
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/adac/active-directory-recycle-bin
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protect OUs from accidental deletion

**Goal:** a mis-click or `Remove-ADObject -Recursive` cannot wipe out an OU tree.

## What the flag does
`ProtectedFromAccidentalDeletion` prevents the object from being deleted: while it is `$true` you cannot delete the
object without changing the value. It is implemented as deny entries in the object's ACL, so inspect the Security
tab (Advanced Features) if you need the exact ACEs. ADUC and ADAC offer it as a check box when you create an OU;
check every OU regardless of how it was created.

## Find and fix unprotected OUs
```powershell
Get-ADOrganizationalUnit -Filter * -Properties ProtectedFromAccidentalDeletion |
  ? { -not $_.ProtectedFromAccidentalDeletion } | Select DistinguishedName
Get-ADOrganizationalUnit -Filter * | Set-ADOrganizationalUnit -ProtectedFromAccidentalDeletion $true
```
Also consider critical objects such as privileged groups and service accounts; `Set-ADObject` has the same
parameter:
```powershell
Get-ADGroup 'GG-Tier0-Admins' | Set-ADObject -ProtectedFromAccidentalDeletion $true
```

## Deliberately delete an OU
```powershell
Set-ADOrganizationalUnit 'OU=Old,DC=ad,DC=example,DC=com' -ProtectedFromAccidentalDeletion $false
# child OUs are protected too; unprotect recursively only after checking contents
Get-ADOrganizationalUnit -SearchBase 'OU=Old,DC=ad,DC=example,DC=com' -Filter * |
  Set-ADOrganizationalUnit -ProtectedFromAccidentalDeletion $false
Remove-ADOrganizationalUnit 'OU=Old,DC=ad,DC=example,DC=com' -Recursive -WhatIf
```

## Gotchas
- Moving a protected OU can be denied as well; if it is, unprotect, move, re-protect.
- It is not a backup: enable the AD Recycle Bin too (it needs a Windows Server 2008 R2 or later forest functional
  level and cannot be turned off once enabled).
- Some provisioning tools delete and recreate OUs; they need an exception workflow.

## Verify
- [ ] The query for unprotected OUs returns nothing.
- [ ] A test deletion of a protected OU fails with "Access is denied".

## Checked
2026-10-27. Documentation: Microsoft Learn `Set-ADOrganizationalUnit`, `Set-ADObject`, `New-ADOrganizationalUnit` and
`Remove-ADOrganizationalUnit` references and the AD Recycle Bin article. Confirmed: `-ProtectedFromAccidentalDeletion`
exists on both Set cmdlets and prevents deletion until cleared; `Remove-ADOrganizationalUnit -Recursive`; Recycle Bin
prerequisites. Removed as unconfirmed: the exact Delete/Delete Subtree/Delete Child ACE description, the statement that
scripted OUs are often unprotected, the DC-computer-object remark and the claim that moving is always blocked (now stated
as possible).
Method: documentation only; no commands were run.
