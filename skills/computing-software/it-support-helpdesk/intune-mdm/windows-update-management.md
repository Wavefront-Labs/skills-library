---
id: computing-software.it-support-helpdesk.intune-mdm.windows-update-management
name: windows-update-management
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, windows-update-for-business, update-rings, feature-updates, quality-updates, driver-updates, deferral, deadline, servicing-channel, update-compliance, windows-autopatch, wufb]
level: practitioner
status: docs-checked
description: "Plan Windows Update client policies (was Update for Business) in Intune: update types, deferral and pause limits, deadlines, grace periods and pilot rings."
sources:
  - "https://learn.microsoft.com/en-us/windows/deployment/update/waas-manage-updates-wufb"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# windows-update-management

Goal: patch the fleet on a predictable cadence without one bad update reaching every machine on the same day.

## What the policies are
Windows Update client policies (formerly Windows Update for Business) are a free service for Pro (including Pro for
Workstations), Education and Enterprise (including LTSC, IoT Enterprise) editions of Windows 10 and 11. Configure them with
Group Policy or MDM (CSP policies; Intune also uses cloud policies). Not every policy exists in every format.

## Update types
- **Feature updates**: released as soon as available; not available for LTSC devices.
- **Quality updates**: typically released on the second Tuesday of each month, though they can come any time; include
  security, critical and driver updates.
- **Driver updates**: non-Microsoft drivers relevant to the device; on by default, and can be turned off with policy.
- **Microsoft product updates**: other Microsoft products, such as MSI-installed Office. Click-to-Run Office cannot be updated
  this way. Off by default and can be turned on.

## Deferral and pause
- A deferral is a number of days after an update is released on Windows Update before it is offered to the device.
- Maximum deferral: feature updates 365 days, quality updates 30 days.
- Pause: up to 35 days from a start date you set, for feature or quality updates (policies "Select when Preview Builds and
  feature updates are Received" and "Select when Quality Updates are Received"). Pausing feature updates does not stop quality
  updates.
- The branch readiness level can enrol devices in the Windows Insider Experimental, Beta or Release Preview channels.
- Staged waves: use deferral to validate a deployment on a pilot group before the rest. A reasonable layout is a pilot ring
  with little or no deferral, then broader rings with longer deferral; the exact days are your choice within the limits above.
  This is a design suggestion, not a Microsoft figure.

## Deadlines
The compliance deadline policy sets separate deadlines and grace periods for feature and quality updates. The deadline is
the number of days from the update's publication until it must be installed; the grace period is the number of days from
install until the device is forced to restart. The grace period helps users returning from leave. Microsoft recommends
automatic download, install and restart, default notifications, and set deadlines, and says fewer controls is better because
Windows Update has built-in intelligence.

## Device recommendations
Devices in use at least 6 hours a month including 2 hours continuous, kept charged (plugged in overnight), with at least
10 GB free space and unobstructed access to the Windows Update service.

## Related services
- Windows Update for Business reports: cloud reporting on Entra joined devices' update compliance (security, quality, driver
  and feature updates).
- Windows Autopatch: works with these policies to add control over approval, scheduling and safeguarding of updates.
- Update Baseline toolkit: Group Policy only, Windows 10 only (not supported on Windows 11); it does not affect offering policies.

## Troubleshooting a device that is behind
1. Check the update report or the device's update status in Intune before touching the machine.
2. Confirm the device is in the intended ring (group membership, including dynamic groups) and that no Group Policy or other
   manager is setting conflicting update policy.
3. Check free space against the 10 GB recommendation and that the device can reach Windows Update.
4. For a stuck client, see resetting-windows-update-components.

## Verify
Rings show the expected device counts, the pilot ring installs a new update first, and later rings converge on the same patch
level within deferral plus deadline.

## Checked
Date: 2026-11-08. Read in full: "What are Windows Update client policies?" (updated 2026-08-20). Removed as unconfirmed: Intune
feature update profile and driver update policy descriptions, the 0 to 14 day ring example numbers as fact, the Autopatch
licensing and "fighting" claims, Get-WindowsUpdateLog and 0x8024 error advice, the manual reset steps, safeguard hold detail,
the co-management workload note, and the deadline "force install after weeks off" claim (only the grace period is documented).
Method: documentation only; no commands were run.
