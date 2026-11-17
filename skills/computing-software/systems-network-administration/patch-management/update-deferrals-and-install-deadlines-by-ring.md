---
id: computing-software.systems-network-administration.patch-management.update-deferrals-and-install-deadlines-by-ring
name: update-deferrals-and-install-deadlines-by-ring
category: computing-software
field: systems-network-administration
product: patch-management
tags: [update-deferral, install-deadline, deployment-rings, maintenance-groups, windows-update-for-business, patch-tiers]
level: practitioner
status: docs-checked
description: "Design deferral and deadline values per deployment ring so updates flow pilot to broad within the remediation SLA, with grace periods, pause handling and worked examples."
sources:
  - https://learn.microsoft.com/en-us/windows/deployment/update/waas-wufb-group-policy
  - https://learn.microsoft.com/en-us/windows/deployment/update/wufb-compliancedeadlines
  - https://learn.microsoft.com/en-us/mem/intune/protect/windows-update-settings
  - https://learn.microsoft.com/en-us/mem/configmgr/sum/deploy-use/automatically-deploy-software-updates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deferrals and install deadlines by ring

Two knobs per ring:
- **Deferral** (offer delay): days after release before devices in the ring are offered
  the update (offer date = release date + deferral). Gives earlier rings time to find problems.
- **Deadline**: days after which installation is forced, plus a **grace period** that
  starts from the pending restart and delays the forced restart (useful for devices that were away).

The last ring's deferral + deadline + grace must fit inside the remediation SLA you set (for example 14 or
30 days for high/critical; your own policy, not a Microsoft figure).

## Documented limits (Windows Update client policies and Intune update rings)
- Quality update deferral 0-30 days; feature update deferral 0-365 days; pause up to 35 days from a start date you set.
- Intune update rings deadlines for quality and feature updates are 2-30 days; grace period 0-7 days.
- The deadline is counted from when the client's update scan first discovered the update, not from the release date.

## Example (monthly cumulative updates, 14-day SLA; illustrative numbers)
| Ring | Members | Deferral | Deadline | Grace | Fully patched by day |
|---|---|---|---|---|---|
| 0 Test | IT lab, test VMs | 0 | 1 | 1 | 2 |
| 1 Pilot | IT staff, small representative group | 2 | 2 | 1 | 5 |
| 2 Early | about a quarter of devices | 4 | 3 | 2 | 9 |
| 3 Broad | the rest | 7 | 3 | 2 | 12 |
| Critical servers | by maintenance window | 7 | window-based | n/a | 10-14 |

The table sums deferral + deadline + grace per ring. A deadline of 1 day is below the 2-day Intune minimum, so for
Intune rings use at least 2 for deadline in ring 0 and recompute the last column. Microsoft's own example uses
three quality-update rings with deferrals of 0, 5 and 10 days. Plan feature updates as separate rings with their own
(much longer) deferrals.

## Implementing
- Group Policy (Computer Configuration > Administrative Templates > Windows Components > Windows Update > Windows
  Update for Business): "Select when Quality Updates are Received" (deferral days, pause) and "Select when Preview
  Builds and feature updates are Received". Deadlines are in "Specify deadline for automatic updates and restarts"
  (separate quality and feature policies from Windows 11 22H2, with a grace period and an option to not auto-restart
  until the grace period ends).
- Intune update ring: Quality update deferral period (days), Feature update deferral period (days), and under
  "Use deadline settings": Deadline for quality updates, Deadline for feature updates, Grace period, Auto reboot
  before deadline.
- ConfigMgr automatic deployment rule (ADR): "Software available time" and "Installation deadline" on the Deployment
  Schedule page (deadline specific time is added to the available time; a random delay of up to two hours is added
  to the displayed deadline). Deadlines apply to Required deployments only.
- Linux repository-snapshot rings are a design choice, not covered by these Microsoft pages.

## Pause handling
When ring 1 finds a regression, pause later rings (Group Policy "Pause quality updates" check box: all devices in
the policy are paused for 35 days; for ConfigMgr, disable or adjust the ADR), log the issue, and restart the clock
once a fix or workaround exists. Record any SLA breach as an exception.

## Gotchas
- Deferral counts from the release date, not from when you approve.
- A device offline for weeks installs once it returns; the grace period (counted from the pending restart) avoids an
  instant forced restart.
- Out-of-band and zero-day updates use the emergency plan (compressed or zero deferral).
- With a target feature update version policy set, feature update deferrals are not in effect.

## Verify
Compliance by ring and days since release matches the table; the last ring reaches your target installed percentage
before the SLA date each month.

## Checked
Date: 2026-11-07. Read in full: Group Policy walkthrough for Windows Update client policies (defer feature 365 and quality 30 days, pause 35 days, offer date formula, 0/5/10-day ring example, Pause quality updates check box, target version note, policy paths), Enforcing compliance deadlines (deadline from scan discovery, grace starting at pending restart; searched with Grep for deadline lines, not read end to end), Intune update ring settings (deferral 0-30 and 0-365, deadlines 2-30, grace 0-7, Auto reboot before deadline), ConfigMgr ADR page (Software available time, Installation deadline, two-hour randomization; read the Deployment Schedule section only). Corrected: deadline is counted from scan discovery, not offer; "60-180 day" feature deferral range removed (documented maximum is 365); ADR setting names corrected; flagged that 1-day deadlines are below the Intune minimum of 2. Removed: Linux snapshot-ring product claims, 95 percent figure.
Method: documentation only; no commands were run.
