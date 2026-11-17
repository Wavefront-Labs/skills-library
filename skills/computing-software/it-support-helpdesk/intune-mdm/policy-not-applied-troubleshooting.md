---
id: computing-software.it-support-helpdesk.intune-mdm.policy-not-applied-troubleshooting
name: policy-not-applied-troubleshooting
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, policy-not-applied, profile-status, conflict, not-applicable, assignment-filters, filter-evaluation, intune-troubleshooting, profile-deployment-status]
level: practitioner
status: docs-checked
description: "Work through an Intune policy not applying: check-in and assignment status reports, conflict lookup, and assignment filter evaluation, modes and precedence."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/configuration/device-profile-monitor
  - https://learn.microsoft.com/en-us/mem/intune/fundamentals/filters-reports-troubleshoot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# policy-not-applied-troubleshooting

Roles: Read Only Operator can view policies and reports; Policy and Profile manager can also change them.

## Step 1: policy status
Devices > Manage devices > Configuration > Policies tab > the policy. Device and user check-in status shows, per user or device (a multi-user device shows each user):
| Status | Meaning |
|---|---|
| Succeeded | Policy applied |
| Error | Failed to apply; the message usually carries an error code that links to an explanation |
| Conflict | Two settings apply to the same device and Intune cannot resolve it; an admin should review |
| Pending | Device has not checked in to receive the policy yet |
| Not applicable | Device cannot receive it, for example a setting specific to iOS 11.1 on a device running iOS 10 |

Further reports on the same page:
- **Per setting status**: each setting and its state.
- **Device assignment status** (Generate report): latest assignment state for devices that received the policy, filterable to errors or conflicts. It shows the user that last checked in.
- **View report**: devices, user names, check-in status and last check-in; select a device to see assignment filter options.
- Counts differ between check-in status and assignment status. The assignment report can take 24-48 hours to reflect assignment or group membership changes on large tenants; other reports depend on each device's last check-in, so stale devices show outdated status.
- Devices > Manage devices > Configuration > Monitor tab has the Configuration policy assignment failures report, plus quick links to Devices with restricted apps, Device encryption status and Certificates.

## Step 2: conflicts
Devices > All devices > the device > Device configuration lists every policy applying to it. Select a policy to see its settings; select a row in Conflict state to see every policy and profile name containing the conflicting setting. Fix by removing the duplicate setting. An end user can read the device name from the Company Portal.

## Step 3: assignment filters
A filter is evaluated at enrollment and at device check-in, and can also run at other times such as a compliance check.
- Per device: Devices > All devices > the device > **Filter evaluation**. It shows filters evaluated, evaluation time, Match or No match, Include or Exclude mode, filter name, description and rules, and the properties evaluated (for example deviceName).
- Per app: Apps > All Apps > the app > Device install status > Filter column > Filters evaluated.
- Results can take up to 30 minutes to appear, and are kept for 30 days (afterwards: "We were not able to retrieve any filter evaluation results").
- The filter name, rules and metadata shown are the current ones, not from the log. Compare Evaluation time with Last modified.
- Available-intent apps do not show in Device install status; use the device Filter evaluation report, and the user must open the app list in the Company Portal to generate results.
- Excluded groups do not show in workload device status reports.
- The device filter report does not show Conditional Access results; use the Entra sign-in logs.

| Filter mode | Result | Outcome |
|---|---|---|
| Include | Match | Apply |
| Include | Not match | Do not apply |
| Exclude | Match | Do not apply |
| Exclude | Not match | Apply |

Overlapping assignments to one device: Exclude beats No filter, which beats Include. Several filters in the same mode combine with OR. A "Not evaluated" result can mean a conflicting assignment exists.
Race: a filter on device category evaluates as null at enrollment, before the user picks a category in the Company Portal; the later result changes at the next check-in, but an app already installed is not removed.
Intune does not let you assign one Entra group twice, and one group cannot have both Available and Required for the same app.
An operatingSystemVersion filter on Available apps for Android, AOSP or iOS gives an inconclusive result (known issue).

## Checked
Date: 2026-11-08. Read in full: "View and monitor device configuration policies" and "Assignment filter reports and troubleshooting" (both updated 2026-04-16). Removed as unconfirmed: the device-side steps (Settings sync, PolicyManager registry path, event IDs 404 and 454, macOS `profiles show`, Android checks), the edition-limit, baseline, MDMWinsOverGP and scope-tag causes, the force re-delivery by removing group membership, and the Verify section. The device-profile-troubleshoot source was dropped as no claim was kept from it.
Method: documentation only; no commands were run.
