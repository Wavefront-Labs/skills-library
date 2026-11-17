---
id: computing-software.cloud-infrastructure-engineering.azure.entra-dynamic-membership-rules
name: entra-dynamic-membership-rules
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, dynamic-groups, dynamic-membership-rules, membership-rules, rule-syntax, rule-builder, validate-rules, extension-attributes, memberof, dynamic-device-groups, group-based-licensing, graph-api]
level: practitioner
status: docs-checked
description: "Write, validate and troubleshoot Entra dynamic membership rules: operator syntax, extension attributes, device rules, memberOf, processing delays and the licence prerequisite."
sources: ["https://learn.microsoft.com/entra/identity/users/groups-dynamic-membership", "https://learn.microsoft.com/entra/identity/users/groups-dynamic-rule-validation", "https://learn.microsoft.com/entra/identity/users/groups-troubleshooting"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra dynamic membership rules — write rules that converge, and prove they do

**Goal:** groups whose membership is computed from user/device attributes, with a rule you
have validated against real objects before licences, Conditional Access or app roles hang off it.

## 1. Prerequisites and limits
- Each unique user who is a member of one or more dynamic groups needs a Microsoft Entra ID P1 (or Intune for Education) licence;
  devices need none.
- Role-assignable groups require assigned (not dynamic) membership.
- A tenant can have at most 15,000 dynamic membership groups.

## 2. Syntax
```
(user.department -eq "Finance") and (user.accountEnabled -eq true)
(user.userPrincipalName -notContains "#EXT#") -and (user.userType -eq "Member")
user.extensionAttribute5 -eq "contractor"
(device.deviceOSType -eq "Windows") and (device.deviceOSVersion -startsWith "10.0.2")
user.memberOf -any (group.objectId -in ['<GROUP-ID-1>', '<GROUP-ID-2>'])
```
- Operators include `-eq -ne -startsWith -notStartsWith -contains -notContains -match -notMatch -in -notIn`.
- Multi-value properties (`assignedPlans`, `otherMails`, `proxyAddresses`): use `-any`/`-all`,
  e.g. `user.assignedPlans -any (assignedPlan.servicePlanId -eq "<SKU-PLAN-GUID>" -and assignedPlan.capabilityStatus -eq "Enabled")`.
- **Extension attributes**: `user.extensionAttribute1` and directory extensions as `user.extension_<appId>_<name>`.

## 3. Create and validate
Create the group in the Microsoft Entra admin center and choose a dynamic membership type, then enter the rule
(the dynamic membership article walks through the rule builder and text editor).
- Portal **Validate Rules** tab (group → Dynamic membership rules) tests up to 20 users or devices at a time — do this before saving.

## 4. Operate
- Processing is asynchronous: depending on tenant size a group can take up to 24 hours to populate the first time or after a rule change.
- Members who don't match a newly configured rule are removed — expected behaviour, so validate before saving.

## Gotchas
- `-contains` is substring match, not list membership — `user.department -contains "Fin"`
  matches "Refinery". Use `-eq` or `-in`.
- Users whose `accountEnabled` flips to false stay members unless the rule checks it.
- Guest objects match user rules; filter on `user.userType -eq "Member"` for internal-only groups.

## Verify
- [ ] Validate Rules reports expected true/false for 5 known in-scope and 5 out-of-scope users.
- [ ] `az ad group member list -g <GROUP-ID> --query length(@)` matches the expected count after processing status shows Updated.
- [ ] Changing a test user's attribute adds/removes them once processing completes (allow up to 24 hours).

## Checked
2026-10-27. Confirmed on Microsoft Learn: groups-dynamic-membership (15,000 dynamic groups per tenant, Entra ID P1 or Intune for Education licence per unique user, devices need no licence,
role-assignable groups need assigned membership, operator set, `memberOf`, device and user properties, extension attributes), groups-dynamic-rule-validation (Validate Rules tab, 20 users or devices),
groups-troubleshooting (up to 24 hours to populate, members removed after rule change).
Removed: 3072-character rule length, nesting statement, .NET regex note, boolean/null and case-insensitivity notes, custom security attributes and memberOf limits, CLI and Graph create examples
(flags and property names could not be read), evaluateDynamicMembership, pause and audit-log tips, static/dynamic conversion claims, null-handling and extension-string gotchas.

Method: documentation only; no commands were run.
