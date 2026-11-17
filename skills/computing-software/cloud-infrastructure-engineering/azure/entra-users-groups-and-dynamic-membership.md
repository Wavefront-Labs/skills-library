---
id: computing-software.cloud-infrastructure-engineering.azure.entra-users-groups-and-dynamic-membership
name: entra-users-groups-and-dynamic-membership
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, groups, dynamic-membership, dynamic-groups, membership-rules, extension-attributes, licensing, security-groups]
level: practitioner
status: docs-checked
description: "Write and operate Microsoft Entra dynamic membership groups: rule syntax and limits, user and device attributes, license requirement, and security of the attributes used."
sources: ["https://learn.microsoft.com/en-us/entra/identity/users/groups-dynamic-membership"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra dynamic membership groups — membership that maintains itself

**Goal:** access and licences follow directory attributes automatically; nobody hand-edits
group members, and the attributes a rule trusts are ones only the right people can write.

## 1. Rules and limits
- A dynamic group is for users or for devices; a rule cannot mix both. A device rule can reference only device attributes, not the owner's user attributes.
- A rule body can be at most 3,072 characters. A single expression needs no parentheses.
- When a user or device attribute changes, the system evaluates all dynamic-group rules in the directory for additions and removals.
- The portal rule builder works only for user-based groups; device groups use the text box. Rules with `-contains`/`-notContains` or complex expressions may not display in the builder.
- Supported operators: `-eq -ne -startsWith -notStartsWith -contains -notContains -match -notMatch -in -notIn`. Microsoft advises minimising `-match` and `-contains` for performance.
- Licence: Microsoft Entra ID P1 (or Intune for Education) for each unique user who is a member of any dynamic group; devices need none.

## 2. Examples
```
user.department -eq "Sales"
(user.userType -eq "Member") and (user.accountEnabled -eq true)
user.mail -notEndsWith "@Contoso.com"
user.displayName -match "^Da.*"
(user.extensionAttribute15 -eq "Marketing")
(device.deviceOSType -eq "iPad") -or (device.deviceOSType -eq "iPhone")
```
- `userType` takes member, guest or null; `usageLocation` is a two-letter code.
- Extension attributes are `ExtensionAttribute1` to `ExtensionAttribute15`; multi-value extension properties are not supported in rules.

## 3. Security of the rule
Group membership is only as trustworthy as who can write the attributes the rule references.
Before choosing an attribute, audit its write permissions in Entra and at the source (for
example on-premises AD). Agent accounts are not distinguished from other users by default;
add a condition if they should be excluded.

## Gotchas
- Group names are not unique; script by object ID.
- A rule that is too narrow or wrong empties the group; for groups that gate Conditional Access, test the rule against sample users first.

## Verify
- [ ] The group's member list matches the expected attribute filter.
- [ ] Every attribute used in the rule has restricted write access.

## Checked
2026-10-28. Confirmed on the Learn page "Manage rules for dynamic membership groups in Microsoft Entra ID": user/device exclusivity, 3,072-character limit, evaluation on attribute change, rule builder limits, operator list, Match/Contains guidance, licence requirement, attribute notes, security guidance. Removed (not on that page or unconfirmed): role-assignable group limits, group-based licensing steps, B2B/cross-tenant guidance, SSPR, break-glass, bulk scripts, deletion and token-size gotchas, `Validate rules`/status wording, nested-group licensing claim, `az ad user update` example.
Method: documentation only; no commands were run.
