---
id: computing-software.it-support-helpdesk.intune-mdm.update-ring-deferrals-and-deadlines
name: update-ring-deferrals-and-deadlines
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, update-deadlines, update-rings, deferral, grace-period, active-hours, windows-update-for-business]
level: practitioner
status: docs-checked
description: "Set Windows update ring deferrals, deadlines, grace periods and restart behaviour in Intune so patches land in days without surprise reboots, and explain them to users."
sources:
  - "https://learn.microsoft.com/en-us/intune/device-updates/windows/manage-update-rings"
  - "https://learn.microsoft.com/en-us/windows/deployment/update/wufb-compliancedeadlines"
  - "https://learn.microsoft.com/en-us/intune/device-updates/windows/ref-update-ring-settings"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# update-ring-deferrals-and-deadlines

Deferral controls *when a device is offered* an update. Deadline controls *how long the
user can postpone installing and restarting* once offered. Most "patching is slow" or
"PC rebooted during my meeting" tickets trace back to these numbers.

## Settings (Devices > Windows > Update rings)
| Setting | Range | Meaning |
|---|---|---|
| Quality update deferral period (days) | 0 to 30 | Days quality updates are deferred, in addition to any channel deferral |
| Feature update deferral period (days) | 0 to 365 | Starts when Microsoft releases the update; leave 0 when a feature update policy pins the version |
| Deadline for quality updates (days) | 2 to 30 | Days before quality updates install automatically |
| Deadline for feature updates (days) | 2 to 30 | Same for feature updates |
| Grace period (days) | 0 to 7 | Minimum days after the deadline until restarts occur automatically |
| Auto reboot before deadline | Yes / No | Yes (recommended) restarts outside active hours before deadline and grace expire; No waits for them, possibly restarting in active hours |

Deadline settings only appear when **Use deadline settings** is set to Allow. Active hours
and notification level are also set in the ring.

## Ring design
Update rings suit staged groups such as test, pilot and production, each with its own
settings. Give every ring a deadline so no device is left unpatched indefinitely. Use
dynamic groups or Autopatch to populate rings.

## Explaining to users
"Windows will install updates in the background. You can postpone the restart for up to
N days; after that the PC restarts outside your working hours, or at the deadline if it's
been off." Pair with a KB showing the toast and the Restart now/Schedule options.

## Troubleshooting
- Device not getting updates: conflicting policies (a device in two rings, or other update
  policy), or the ring is paused. Check Intune profile status per device.
- Users complain of restarts mid-day: Auto reboot before deadline is No, or the deadline and
  grace period have expired. Review those settings.

## Gotchas
- Pausing a ring (feature or quality separately) blocks that type for up to 35 days, then
  the pause expires and the device scans; Extend resets it to 35 days. Devices learn of the
  pause at their next check-in.
- Grace period 0 with a short deadline can produce restarts at the deadline.
- Feature update deferral plus a feature update policy = confusion; use one.

## Verify
Windows Update reports show the ring reaching the current cumulative update within the
planned window, with few restart complaints.

## Checked
2026-11-01. Confirmed against the Intune Learn pages on update rings and update ring settings
and the Windows Update for Business deadlines page: deferral ranges (0-30, 0-365), deadline
range (2-30), grace period (0-7), auto reboot before deadline, 35-day pause behaviour.
Removed: typical-value columns, ring percentages and day counts, the timeline, active-hours
example, WSUS registry key, Get-WindowsUpdateLog and event-log tips, and the >95% target,
none confirmed by those pages.
Method: documentation only; no commands were run.
