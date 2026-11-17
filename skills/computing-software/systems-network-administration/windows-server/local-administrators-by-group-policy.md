---
id: computing-software.systems-network-administration.windows-server.local-administrators-by-group-policy
name: local-administrators-by-group-policy
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, security-policy-settings, gpo-security-settings, restricted-groups, local-administrators-gpo, local-users-and-groups, group-policy-preferences, member-of, server-admin-groups]
level: practitioner
status: docs-checked
description: "Control local Administrators membership by GPO: Restricted Groups (replace) vs GPP Local Users and Groups (update), per-server admin groups via %ComputerName%, and pitfalls."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/description-of-group-policy-restricted-groups
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-preferences
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/gpresult
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local Administrators membership by Group Policy

## Option 1: Restricted Groups (enforce exact membership)
*Computer Configuration > Policies > Windows Settings > Security Settings > Restricted Groups*
- **"Members of this group"** on `Administrators`: when enforced, any current member that is not on the list is
  removed (except the built-in administrator in the Administrators group) and listed members are added.
- **"This group is a member of"**: only inclusion is enforced; the restricted group is added to the listed groups and
  not removed from others.
- Microsoft does not support using Restricted Groups to manage membership of domain groups; it is designed for local groups.

## Option 2: GPP Local Users and Groups (flexible, recommended)
*Computer Configuration > Preferences > Control Panel Settings > Local Users and Groups >
New > Local Group* `Administrators (built-in)`, action **Update**:
- Use the delete-all-members options only if you want an enforced state, then add the groups you need (for example
  `AD\GG-Tier1-ServerAdmins`).
- Item-level targeting can vary membership by OU, security group or operating system.

Per-server admin groups (`LA-APP01`, targeted with item-level targeting) give least privilege: admin on exactly one
server.

## Rules
- Do not add Domain Admins to member servers beyond the default; plan a recovery path before removing default members.
- Test enforcement on a pilot OU first: enforced membership removes accounts that are not listed.

## Check
```powershell
Get-LocalGroupMember Administrators
gpresult /scope computer /h report.html
```

## Verify
- [ ] A manually added local admin disappears after `gpupdate /force`.
- [ ] `LA-<server>` members have admin only on that server.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed in the restricted groups article: Members and Member Of behaviour (members not listed are removed except the administrator in the Administrators group; Member Of enforces inclusion only) and that Restricted Groups is unsupported for domain groups; Group Policy Preferences include Local Users and Groups and item-level targeting by security group, OU and operating system; gpresult /scope computer with /h. Removed as unconfirmed: the claim that multiple Restricted Groups GPOs do not merge, the GPP delete-all checkbox labels, LAPS and RID 500 handling, the per-machine variable example, the time-bound membership remark and the Domain Admins join behaviour.

Method: documentation only; no commands were run.
