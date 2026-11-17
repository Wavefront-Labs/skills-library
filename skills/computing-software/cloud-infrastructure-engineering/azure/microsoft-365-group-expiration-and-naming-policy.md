---
id: computing-software.cloud-infrastructure-engineering.azure.microsoft-365-group-expiration-and-naming-policy
name: microsoft-365-group-expiration-and-naming-policy
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, group-expiration, group-naming-policy, microsoft-365-groups, group-creation-restriction]
level: practitioner
status: docs-checked
description: "Control Microsoft 365 group sprawl in Entra ID: expiration (lifecycle) policy, prefix/suffix naming policy, blocked words and restricting who can create groups."
sources: ["https://learn.microsoft.com/entra/identity/users/groups-lifecycle", "https://learn.microsoft.com/entra/identity/users/groups-naming-policy", "https://learn.microsoft.com/entra/identity/users/groups-settings-cmdlets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft 365 group expiration and naming policy

**Goal:** stop orphaned Teams/M365 groups piling up and make group names predictable, without breaking
active collaboration.

## Expiration (group lifecycle) policy
- Applies to Microsoft 365 groups. Lifetime is a preset or custom value of 30 days or more.
- Owners get renewal emails 30, 15 and 1 day before expiry. Groups with user activity (Outlook, SharePoint,
  Teams, Viva Engage) are **auto-renewed**, so only genuinely idle groups expire.
- Ownerless groups: set a fallback email that receives the notices.
- Expired groups are deleted and can be restored within 30 days (not customizable).
```powershell
Connect-MgGraph -Scopes Directory.ReadWrite.All
New-MgGroupLifecyclePolicy -GroupLifetimeInDays 365 -ManagedGroupTypes Selected `
  -AlternateNotificationEmails "it-groups@contoso.com"
# scope to selected groups first, then switch ManagedGroupTypes to All
Add-MgGroupToLifecyclePolicy -GroupLifecyclePolicyId <id> -GroupId <groupId>
```
Licence: Entra ID P1 for members of groups the policy applies to.

## Naming policy and group creation (directory settings Group.Unified)
```powershell
$tpl = Get-MgBetaDirectorySettingTemplate | ? DisplayName -eq "Group.Unified"
$setting = Get-MgBetaDirectorySetting | ? DisplayName -eq "Group.Unified"   # create from $tpl if null
$values = @(
  @{Name="PrefixSuffixNamingRequirement"; Value="GRP_[Department]_[GroupName]"},
  @{Name="CustomBlockedWordsList";        Value="CEO,Payroll,HR"},
  @{Name="EnableGroupCreation";           Value="false"},
  @{Name="GroupCreationAllowedGroupId";   Value="<security-group-id>"})
Update-MgBetaDirectorySetting -DirectorySettingId $setting.Id -Values $values
```
- Prefix/suffix can be fixed strings or user attributes such as [Department]. Only one [GroupName] is allowed;
  prefix, suffix and group name together are limited to 63 characters.
- Blocked words: up to 5,000 phrases, exact match only, no substring matching.
- Some admin roles (Global Administrator, User Administrator and others the page lists) are exempt from the naming policy.
- `EnableGroupCreation=false` + allowed group restricts creation of M365 groups (and Teams) to that group's
  members; the setting concerns nonadmin users.

## Gotchas
- The naming policy applies to group name and alias on create or edit across Outlook, Teams, SharePoint, Exchange and Planner.
- Expiration deletes the group; its Planner, Sites and Teams data is permanently deleted 30 days after deletion - communicate before enabling for All.

## Verify
- [ ] `Get-MgGroupLifecyclePolicy` shows the lifetime and scope; a test group created by a normal user gets the prefix.
- [ ] A user outside the allowed group cannot create a Team.

## Checked
2026-11-01. Confirmed against Microsoft Learn groups-lifecycle, groups-naming-policy and groups-settings-cmdlets: 30-day minimum, 30/15/1-day notices, auto-renewal activity, 30-day restore, P1 licence, Group.Unified settings, 5,000 blocked phrases, exempt admin roles. Corrected the 264-character limit to 63, Yammer to Viva Engage. Removed the preset list, attribute list beyond [Department], Graph renaming and propagation-delay claims (not stated).
Method: documentation only; no commands were run.
