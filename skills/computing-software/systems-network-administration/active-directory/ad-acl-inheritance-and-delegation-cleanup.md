---
id: computing-software.systems-network-administration.active-directory.ad-acl-inheritance-and-delegation-cleanup
name: ad-acl-inheritance-and-delegation-cleanup
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ou-delegation, ad-acl-inheritance, dsacls, ad-acl-audit]
level: advanced
status: docs-checked
description: "Manage AD ACL inheritance: find objects with inheritance disabled, remove stale delegations and reset objects to schema default security safely."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc771151(v=ws.11)
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/appendix-c--protected-accounts-and-groups-in-active-directory
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# AD ACL inheritance and delegation cleanup

Years of delegation wizard runs leave ACEs for groups that no longer exist, and objects that silently stopped
inheriting the OU's ACL.

## Find objects with inheritance blocked
```powershell
Get-ADObject -SearchBase "OU=Corp,DC=corp,DC=example,DC=com" -LDAPFilter '(objectClass=*)' -Properties nTSecurityDescriptor |
  Where-Object { $_.nTSecurityDescriptor.AreAccessRulesProtected } | Select DistinguishedName
```
Expected exceptions: protected accounts and groups. AdminSDHolder/SDProp turns inheritance off on them and, by
default, resets their permissions every 60 minutes on the PDC emulator. Everything else needs a reason.

## Find stale and explicit ACEs
```powershell
(Get-Acl "AD:OU=Workstations,OU=Corp,DC=corp,DC=example,DC=com").Access |
  Where-Object { -not $_.IsInherited } | Select IdentityReference,ActiveDirectoryRights,ObjectType,InheritanceType
```
Unresolved SIDs (`S-1-5-21-...`) usually belong to deleted principals: remove them.

## Remove a delegation
```cmd
dsacls "OU=Workstations,OU=Corp,DC=corp,DC=example,DC=com" /R "CORP\Old-Helpdesk"
```
`/R` deletes all ACEs for the users or groups named.

## Re-enable inheritance / reset to default
```cmd
dsacls "CN=svc-app,OU=Service,DC=corp,DC=example,DC=com" /P:N      # object can inherit again
dsacls "CN=svc-app,OU=Service,DC=corp,DC=example,DC=com" /S        # restore schema default security
dsacls "OU=Staging,DC=corp,DC=example,DC=com" /S /T                # same for the whole tree
```
`/P:N` marks the object as not protected so it can inherit from its parent (`/P:Y` blocks inheritance). `/S` restores
the security on the object to the default for its object class from the schema, which removes every explicit
delegation on it; `/T` extends that to the tree and is valid only with `/S`. Use `/S` on single objects; run `/S /T`
on an OU only after exporting the ACLs.

## Before any change
```cmd
dsacls "OU=Corp,DC=corp,DC=example,DC=com" > ou-corp-acl-before.txt
```

## Verify
- [ ] Only documented explicit ACEs remain on delegated OUs.
- [ ] No orphan SIDs; objects that are not protected accounts all inherit.

## Checked
2026-10-27. Documentation: Microsoft Learn dsacls reference (Windows Server 2012 R2 library, the page the current
docs link to) and Appendix C (Protected Accounts and Groups). Confirmed: `/P:{Y|N}` protects or unprotects the object from
inheritance, `/R` deletes ACEs for the named principals, `/S` restores class-default security and `/T` is valid only with
`/S`, and the output-redirect pattern; SDProp runs every 60 minutes by default on the PDC emulator and disables inheritance
on protected objects. The adminCount reference was removed as unconfirmed. The two generic source links were replaced.
Method: documentation only; no commands were run.
