---
id: computing-software.it-support-helpdesk.desktop-support.m365-license-assignment-and-group-licensing
name: m365-license-assignment-and-group-licensing
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, microsoft-365, m365-support, license-assignment, group-based-licensing, usage-location, service-plans, microsoft-graph-powershell, set-mglicense, license-errors]
level: practitioner
status: docs-checked
description: "Assign Microsoft 365 licences: group-based licensing, usage location, disabling service plans, fixing assignment errors with the admin centre and Graph PowerShell."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/users/licensing-groups-assign"
  - "https://learn.microsoft.com/en-us/entra/identity/users/licensing-groups-resolve-problems"
  - "https://learn.microsoft.com/en-us/microsoft-365/enterprise/assign-licenses-to-user-accounts-with-microsoft-365-powershell"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# m365-license-assignment-and-group-licensing

Goal: users get the right licence from group membership, and "I don't have Teams/Outlook" tickets are resolved in one check.

## Group-based licensing
- Microsoft 365 admin centre, Billing > Licenses > Assign licenses: pick the group (security, mail-enabled or Microsoft 365 group), the subscription, and optionally Turn apps and services on or off, then Assign licenses. Unassign from the product details page, group row, three dots, Unassign.
- Needs at least Groups Administrator, License Administrator or User Administrator. Graph PowerShell alternative: Set-MgGroupLicense.
- Nested groups are not supported: only users in the first-level group are licensed.
- Admin centre limits: licences on at most 20 groups at a time; Reprocess handles up to 20 users at a time; user lists page at 999.
- Large groups (for example 100,000 users) can be slow to process.
- Moving a user between licensed groups: add to the destination group first, confirm the new licence shows on the user's Licenses page, then remove from the original group. Removing first leaves the user unlicensed until processing finishes.
- Users with no usage location inherit the tenant location for group-based licensing.

## Direct assignment with Graph PowerShell
```powershell
Connect-MgGraph -Scopes User.ReadWrite.All, Organization.Read.All
Get-MgSubscribedSku
Get-MgUserLicenseDetail -UserId "belindan@litwareinc.com"
Update-MgUser -UserId "belindan@litwareinc.com" -UsageLocation US
$e5Sku = Get-MgSubscribedSku -All | Where SkuPartNumber -eq 'SPE_E5'
Set-MgUserLicense -UserId "belindan@litwareinc.com" -AddLicenses @{SkuId = $e5Sku.SkuId} -RemoveLicenses @()
```
- UsageLocation must be a valid ISO 3166-1 alpha-2 code (US, FR). Accounts synced from on-premises AD have no location by default.
- Available licences in a plan = ActiveUnits - WarningUnits - ConsumedUnits.
- Unlicensed users: `Get-MgUser -Filter 'assignedLicenses/$count eq 0' -ConsistencyLevel eventual -CountVariable unlicensedUserCount -All`.
- Without -All, Get-MgUser returns only the first 100 accounts.
- To turn services off, pass `DisabledPlans` (service plan IDs from `$e5Sku.ServicePlans`) in the -AddLicenses hashtable. Re-supplying a user's existing disabled plans keeps them disabled.
- Switch plans (E3 to E5): remove the old SkuId with -RemoveLicenses, then add the new one.

## Assignment errors (group licensing)
Find them: admin centre Billing > Licenses > product > Errors & issues; or Entra admin centre Billing > Licenses > Overview, or Groups > the group.
- Not enough licenses: buy more, remove unused direct assignments, free licences elsewhere.
- Conflicting service plans (for example Exchange Online Plan 1 and Plan 2 from different products): disable one plan, remove the redundant direct licence, or adjust the group assignment.
- Other products depend on this license (Audio Conferencing depends on Skype for Business): remove the dependent service first. Removal can fail or the inherited licence can convert to direct.
- Usage location isn't allowed: set a supported location on the user or remove them from the group.
- Duplicate proxy addresses block Exchange Online licensing: fix, then reprocess.
- LicenseAssignmentAttributeConcurrencyException in audit logs: no action, retried automatically.
- Several products on one group: one failing product can stop the others being assigned; find which one failed.
- Add-on products (for example Workplace Analytics) need their prerequisite plan assigned in the same group.
- Before deleting a licensed group, remove its licences; dependencies can convert inherited licences to direct.
- Fix the cause, then Errors & issues > select group or user > Reprocess.

## Verify
`Get-MgUserLicenseDetail` lists the intended SKU, the user's Licenses page shows it from the intended group with no errors.

## Checked
Date: 2026-11-09. Confirmed in the three Microsoft Learn pages (the two Entra URLs both resolve to the admin centre group licensing article). Removed as unconfirmed: Entra ID P1 requirement, Entra Licenses blade navigation, error code names CountViolation / MutuallyExclusiveViolation / DependencyViolation, the 30-day recycle bin and mailbox deletion clocks, inactive-user report steps, provisioning delay times and trial SKU notes.
Method: docs-checked 2026-11-09 against the three Microsoft Learn pages listed in sources, downloaded and read in full.
