---
id: computing-software.it-support-helpdesk.intune-mdm.assignment-filters-and-group-targeting
name: assignment-filters-and-group-targeting
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, assignment-filters, group-targeting, dynamic-groups, include-exclude, rule-syntax, intune]
level: practitioner
status: docs-checked
description: "Target Intune policies and apps correctly: user vs device groups, include/exclude matrix, dynamic group latency, assignment filter limits, rule syntax and where to review them."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/fundamentals/filters"
  - "https://learn.microsoft.com/en-us/mem/intune/fundamentals/filters-device-properties"
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/device-profile-assign"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# assignment-filters-and-group-targeting

## User groups vs device groups
| Target | Settings follow | Good for |
|---|---|---|
| Device group | The device, whoever is signed in | Devices without a dedicated user: ticket printing, inventory scanning, shift/shared devices |
| User group | The user, on all their devices | Features that belong to a user, such as email or user certificates |

Rule from the assignment article: if you do not care who is signed in, use a device
group; if the setting should go with the user, use a user group. On Azure Virtual Desktop
multi-session, device CSPs must target device groups and user CSPs user groups.
Selecting All Devices and All Users together disables adding other Entra groups.

## Include and exclude
- The Entra group is the limiting group; use the smallest scope and refine with filters.
- Static groups and dynamic user groups can be included or excluded. Dynamic device
  groups can be included, but avoid them in exclusions: dynamic membership needs
  processing time, so a new device can receive the policy before it lands in the
  excluded group (documented example: a dynamic group on `enrollmentProfileName`).
- Exclusion support matrix: dynamic-device-include with dynamic-device-exclude is
  partially supported (not recommended when latency matters); static-include with
  dynamic-device-exclude is partially supported; static-include with static-device-exclude
  is supported; including a device group (static or dynamic) while excluding user
  groups is not supported, because Intune does not evaluate user-to-device relationships.
- For latency-sensitive cases, assign to user groups (or All devices for userless
  devices) with an assignment filter instead of a device group.

## Dynamic groups vs filters
Use filters for Intune-only targeting by device properties (OS, model, manufacturer,
ownership, category): they evaluate at check-in with no group processing delay. Use
dynamic groups for cross-workload targeting (Conditional Access, licensing), Autopilot
profile assignment, or user-based grouping.

## Assignment filters
Create: Intune admin center > Tenant administration > Assignment filters > Create (also
under Devices > Organize devices and Apps). Choose Managed devices or Managed apps, a
platform (Windows 10 and later, macOS, iOS/iPadOS, Android Enterprise, AOSP, Android
device administrator for devices; Android, iOS/iPadOS, Windows for apps), then build rules
with the rule builder or rule syntax editor. Select Preview devices to list matching
enrolled devices (not available for properties in preview).

Rule examples taken from the properties page:
```text
(device.manufacturer -eq "Microsoft")
(device.model -startsWith "Surface Book")
(device.deviceOwnership -eq "Corporate")
(device.enrollmentProfileName -startsWith "Autopilot Profile")
(device.operatingSystemVersion -eq 14.2.1)
```
`deviceOwnership` takes Personal, Corporate or unknown with `-eq`/`-ne`.
`enrollmentProfileName` is set at enrollment and matches the Autopilot, ADE or Google
enrollment profile. `operatingSystemVersion` takes `-eq -ne -gt -ge -lt -le`; `osVersion`
is a string property with string operators. Partial operators are `-startsWith`,
`-contains`, `-notcontains`. Nested parentheses disable the basic rule builder.

Limits: up to 200 assignment filters per tenant; each filter limited to 3,072
characters; devices must be enrolled; for managed apps, filters apply only to app
protection and app configuration policies, not to compliance or configuration profiles.

Use a filter on an assignment: Edit filter > **Include filtered devices in
assignment** or **Exclude filtered devices in assignment** (or Do not apply a filter).
Filters are evaluated when the device enrolls, checks in or a policy evaluates.

## Checking where a filter is used
Tenant administration > Assignment filters > the filter > **Associated Assignments**
tab lists the apps and policies, groups and Include/Exclude mode. Deleting a filter still
in use fails with "Unable to delete assignment filter - An assignment filter is
associated with existing assignments." The page also points to "Assignment filter
reports and troubleshooting" for evaluation results (not read for this skill).

## Gotchas
- Older iPad Pro models use a double prime in the model name; use partial operators
  (`-contains "iPad Pro 12.9"`) rather than a full string match.
- The Android device administrator platform is deprecated for GMS devices.

## Verify
Use Preview devices to confirm the expected devices match, then check the filter's
Associated Assignments tab.

## Checked
Date: 2026-11-07. Read in full: the assignment filters overview and the device
assignment article (its exclusion matrix rows 1, 2, 3, 4, 5, 6 and 7 as listed). The
device and app properties page (22k characters) was searched for the properties and
operators quoted above rather than read end to end; the support table for workloads and
the filter reports page were not opened.
Removed or corrected: "excludes win over includes" and the blanket "do not mix types"
claim (replaced by the documented matrix), the dynamic group examples with
`devicePhysicalIds` and `user.department`, the filter rule `device.osVersion -startsWith
"10.0.22"` example, the `Tenant administration > Filters` path (now Assignment filters),
"All users / All devices are faster to evaluate" and "device without primary user
gets no user-targeted assignments", and the troubleshooting paths that were not on the pages.
Method: documentation only; no commands were run.
