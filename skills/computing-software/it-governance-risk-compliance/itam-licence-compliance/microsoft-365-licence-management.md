---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.microsoft-365-licence-management
name: microsoft-365-licence-management
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [microsoft-365-licence-management, microsoft-licensing, microsoft-365, m365, group-based-licensing, usage-reports, entra, sign-in-activity, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Right-size Microsoft 365 plans using usage reports, Entra last sign-in data, group-based licensing and Graph PowerShell licence cmdlets."
sources:
  - https://learn.microsoft.com/en-us/microsoft-365/admin/activity-reports/activity-reports
  - https://learn.microsoft.com/en-us/entra/identity/monitoring-health/howto-manage-inactive-user-accounts
  - https://learn.microsoft.com/en-us/microsoft-365/admin/manage/manage-group-licenses
  - https://learn.microsoft.com/en-us/microsoft-365/enterprise/assign-licenses-to-user-accounts-with-microsoft-365-powershell
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft 365 licence management

Goal: assign the cheapest plan that matches usage, and reclaim seats nobody uses.

## Find unused seats
- Admin center usage reports (Reports > Usage) show who uses a service heavily and who barely uses it and might not need a licence. Reports cover the last 7, 30, 90 and 180 days and typically appear 24 to 72 hours after the period, sometimes later.
- Viewing reports needs a role such as Global Administrator, Reports Reader, Exchange, SharePoint or Teams Administrator, or Usage Summary Reports Reader (no user details). Prefer the least privileged role.
- By default reports conceal usernames, display names, groups and sites. A Global Administrator can turn off "Conceal user, group, and site names in all reports" in Org settings > Services > Reports if privacy practice allows; showing names is a logged event in the Purview audit log.
- The last activity date in user details is the most recent intentional activity, regardless of the report period selected. Usage data for a deleted user is removed within 30 days. Usage reports do not cover perpetual licence models.
- Billing > Licenses shows assigned and unassigned counts; Users > Active users shows who is licensed, unlicensed or a guest.
- Entra sign-in data: Microsoft Graph `signInActivity` (needs `$select=signInActivity`, not returned by default) exposes `lastSignInDateTime` (last interactive attempt, including failures), `lastNonInteractiveSignInDateTime` and `lastSuccessfulSignInDateTime`. Reading it needs an Entra ID P1 or P2 licence and the AuditLog.Read.All and User.Read.All permissions; Reports Reader is the least privileged role for the activity logs.
- Entra's guidance: there is no built-in inactive-user report; define "for a while" yourself (many organisations use 90 to 180 days) and allow for leave. The value can be blank for accounts that never signed in or whose last attempt predates April 2020, and may take up to 24 hours to update.

## Assign through groups
- Group-based licensing assigns licences to a group so members receive them and leavers lose them when removed from the group. In the admin center, one assignment applies to at most 20 groups, and nested groups are not supported.
- A user needs a usage location set before a licence can be assigned.
- When moving users between plans, add the new licence first and then remove the old one.

## Bulk work in Graph PowerShell
- `Set-MgUserLicense` adds and removes licences for a user (`-AddLicenses` and `-RemoveLicenses`); `Get-MgSubscribedSku` lists the SKUs and service plans you own. Use them for scripted reclaim and reporting.

Verify: unassigned seats and inactive accounts are reported on a fixed schedule.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the Microsoft Learn usage reports, Entra inactive accounts, group-based licensing and Graph PowerShell licensing pages. Removed: the ISO, SPDX and CycloneDX sources (unrelated to Microsoft 365), the "shared mailboxes under 50 GB need no licence" claim (the Exchange shared mailbox page does not state it), the E3 versus E5 comparison and the mid-term refund claim.
