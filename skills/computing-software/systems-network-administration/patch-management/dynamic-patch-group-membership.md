---
id: computing-software.systems-network-administration.patch-management.dynamic-patch-group-membership
name: dynamic-patch-group-membership
category: computing-software
field: systems-network-administration
product: patch-management
tags: [dynamic-groups, collection-query, patch-groups, configmgr, entra-id, patch-management]
level: practitioner
status: docs-checked
description: "Build self-maintaining patch groups with ConfigMgr query, include and exclude collection rules and Entra dynamic device groups, including rule syntax limits and security cautions."
sources:
  - https://learn.microsoft.com/en-us/mem/configmgr/core/clients/manage/collections/create-collections
  - https://learn.microsoft.com/en-us/entra/identity/users/groups-dynamic-membership
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic patch group membership

**Goal:** a new device lands in the right patch wave from its attributes and leaves it when they change; no hand-maintained lists.

## ConfigMgr collections
- Rule types: direct (manual, more administrative overhead), query (re-evaluated on a schedule, for example all users in an AD organizational unit), include collection and exclude collection. A collection holds users or devices, not both. If include and exclude conflict, the exclude rule wins.
- A collection only contains members of its limiting collection, so set the limiting collection to your managed-server (or workstation) collection.
- "Use incremental updates" scans for new or changed resources, by default at 5-minute intervals, independent of the full evaluation. Query rules that use certain classes cannot use it: for example SMS_G_System_CollectedFile, SMS_G_System_LastSoftwareScan, SMS_G_System_AppClientState, the SMS_G_System_DCM* deployment classes, SMS_G_System_SoftwareUsageData, SMS_G_System_CI_ComplianceState, SMS_G_System_EndpointProtectionStatus, SMS_GH_System_* and SMS_GEH_System_*. The page's full list is longer.
- "Schedule a full update on this collection": disabling it clears the schedule. Built-in collections such as All Systems cannot have evaluation disabled; the page advises changing only the time, not the recurrence pattern.
- New members appear after the first scheduled update, or after Update Membership.
- Since version 2010 you can preview query results (green triangle in Query Statement Properties); from 2103 the preview row limit is 1 to 10,000 with a default of 5,000.
- PowerShell: New-CMCollection, Set-CMCollection, Import-CMCollection.
- Use an exclude collection for devices with a patch exception, as the page's own example (include Dell desktops, exclude low-RAM machines) shows the pattern.

## Entra dynamic device groups (for Intune rings and similar)
- Rules are evaluated automatically when device attributes change: devices that satisfy the rule are added, others removed. You cannot manually add or remove members. A rule cannot mix users and devices, and a device rule can reference only device attributes.
- Device rules must be written in the text box (the rule builder supports only user-based groups). Maximum rule body length is 3,072 characters; a tenant can have up to 15,000 dynamic groups. No licence is needed for devices in device-based dynamic groups.
- Documented device attributes include deviceOSType, deviceOSVersion, deviceOwnership (value `Company`), deviceTrustType (`AzureAD`, `ServerAD`, `Workplace`), enrollmentProfileName, devicePhysicalIds (Autopilot values such as `[OrderID]:...`) and extensionAttribute1 to extensionAttribute15 (you must set the value on the device object).
- Example forms from the page: `device.deviceOSType -eq "Windows"` and `device.extensionAttribute1 -eq "some string value"`; combine with `-and`, `-or`, `-not`. For Windows 10 use `device.deviceOSVersion -startsWith "10.0.1"`. Property names are case sensitive; operators and string comparisons are not.
- Minimise `-match` and `-contains`; Microsoft has a separate article on simpler, more efficient rules for faster processing.
- All-devices rule: `device.objectId -ne null`.
- For Intune app and policy assignment, Microsoft recommends assignment filters where they meet the need, and dynamic groups for non-Intune or cross-workload cases (Conditional Access, licensing, Autopilot profiles).

## Rules for good groups
- One attribute you control decides membership, not a fragile combination of name patterns.
- Security: a dynamic rule is only as safe as who can write the attribute it uses. Check write permissions, including on-premises attributes that can be self-written, before using an attribute for groups that control access.
- Waves should be mutually exclusive and cover all managed devices; report devices that match none.

## Verify
Count per group plus unassigned equals total managed; a newly enrolled test device appears in its group after the next evaluation. The pages do not state a processing time for Entra, so measure it before relying on it for urgent moves.

## Checked
Date: 2026-11-07. Read in full: How to create collections in Configuration Manager and Manage rules for dynamic membership groups in Microsoft Entra ID. Removed as unconfirmed: the WQL example (SystemOUName, Caption filter), "incremental updates only on small collections", the "minutes to hours" Entra processing claim, `devicePhysicalIds` ZTDId/Pilot example, and all AWS Systems Manager patch group and Ansible inventory content (the AWS page was not read and is not in the allowed vendor set for this pass).
Method: documentation only; no commands were run.
