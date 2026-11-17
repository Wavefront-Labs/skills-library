---
id: computing-software.systems-network-administration.active-directory.group-scopes-and-types
name: group-scopes-and-types
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-users-and-groups, group-scope, universal-groups, domain-local-groups, global-groups, security-groups, distribution-groups, new-adgroup, set-adgroup, agdlp, token-size]
level: practitioner
status: docs-checked
description: "Pick and convert AD group scopes and types: domain local vs global vs universal membership rules, conversions with Set-ADGroup, and token-size effects."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-adgroup
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/kerberos-authentication-problems-if-user-belongs-to-groups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group scopes and types

## Scopes
| Scope | Can contain | Can be granted access to |
|---|---|---|
| Domain local | accounts and global groups from any domain or trusted domain; universal groups from the same forest; other domain local groups from the same domain; accounts, global and universal groups from other forests and external domains | resources in **its own domain** |
| Global | accounts and other global groups from the **same domain** | resources in any domain of the forest or in trusting domains and forests |
| Universal | accounts, global groups and other universal groups from **any domain in the forest** | any domain in the forest or in trusting forests |

Common nesting pattern (AGDLP / AGUDLP): accounts -> Global (role) -> [Universal, multi-domain] -> Domain Local
(resource + permission) -> Permission.

## Types
- **Security**: can be used in DACLs (permission lists) and for rights assignment.
- **Distribution**: for email lists only; not security-enabled, so it cannot appear in DACLs.

## Create
```powershell
New-ADGroup -Name 'DL-FS01-Finance-RW' -GroupScope DomainLocal -GroupCategory Security `
  -Path 'OU=Resource Groups,DC=ad,DC=example,DC=com' -Description 'Modify on \\FS01\\Finance'
```

## Convert scope
Microsoft's allowed conversions:
- Global -> Universal, if the group is not a member of any other Global group.
- Universal -> Global, if it contains no other Universal group.
- Universal -> Domain Local, if it is not a member of any other Universal group.
- Domain Local -> Universal, if it contains no other Domain Local group.
Global <-> Domain Local directly is not on the list; go through Universal.
```powershell
Set-ADGroup 'GG-Project-X' -GroupScope Universal
Set-ADGroup 'GG-Project-X' -GroupCategory Distribution   # type change
```

## Single-domain shortcut
In a single-domain forest, scope barely matters functionally, but keep AGDLP naming so
access reviews read clearly and a future second domain/trust is easy.

## Gotchas
- Token size: users in hundreds of groups (nested) hit Kerberos token limits (`MaxTokenSize`, 48,000 bytes by
  default on Windows Server 2012 and later). Domain-local groups count as `s`-class SIDs and universal groups from other
  domains and SID-history SIDs as `d`-class SIDs in Microsoft's size formula (see the token bloat skill).
  Prefer fewer, nested role groups.

## Verify
- [ ] `Get-ADGroup -Filter * | Group GroupScope` matches your naming convention (no `GG-` that is universal by accident).

## Checked
2026-10-27. Documentation: Microsoft Learn Understand security groups (scope table), `Set-ADGroup` reference and the
Kerberos token-size article. Confirmed: group scope membership rules and the four scope-conversion conditions;
distribution groups are not security-enabled and cannot be in DACLs; `Set-ADGroup -GroupScope/-GroupCategory`; 48,000-byte
MaxTokenSize default from Windows Server 2012. Corrected: Universal -> Domain Local is allowed only when the group is not a
member of another Universal group (the draft said any time), and Universal -> Global requires no nested Universal groups
(the draft added users from other domains). Removed as unconfirmed: the global-catalog replication column and gotcha, and
the Exchange mail-enabled security group remark.
Method: documentation only; no commands were run.
