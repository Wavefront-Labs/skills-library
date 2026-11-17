---
id: computing-software.systems-network-administration.patch-management.intune-update-rings-and-feature-update-policies
name: intune-update-rings-and-feature-update-policies
category: computing-software
field: systems-network-administration
product: patch-management
tags: [update-rings, feature-update-policy, windows-update-for-business, intune, deployment-rings, wufb]
level: practitioner
status: docs-checked
description: "Configure Windows updates in Intune: update ring profiles per deployment ring, feature update policies to pin versions, quality and expedited updates, and reports."
sources:
  - https://learn.microsoft.com/en-us/intune/device-updates/windows/update-rings
  - https://learn.microsoft.com/en-us/mem/intune/protect/windows-10-feature-updates
  - https://learn.microsoft.com/en-us/intune/device-updates/windows/configure-expedite-policy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intune update rings and feature update policies

Intune admin center: Devices > Windows Updates (menu name per the expedite policy page; check the Learn pages for current navigation).

## Update rings (one profile per ring)
Example values only; tune to your risk appetite.
| Setting | Pilot | Broad |
|---|---|---|
| Microsoft product updates / Windows drivers | Allow / Allow (or block drivers and use driver policies) | same |
| Quality update deferral (days) | 0 | 5-7 |
| Feature update deferral (days) | 0 (use feature update policy instead) | 0 |
| Servicing channel | General Availability | General Availability |
| Deadline for quality updates (days) | 2 | 3 |
| Deadline for feature updates (days) | 5 | 7 |
| Grace period (days) | 1 | 2 |
| Auto reboot before deadline | Yes | Yes |
| Active hours | 8-18 | 8-18 |
Assign to Entra ID groups (dynamic groups per ring). A device should get **one** ring; overlapping assignments of the same setting cause conflicts, so keep ring groups mutually exclusive.

## Feature update policies
Pin devices to a Windows version; devices stay on it until you change the policy. Feature update policies support scheduled and gradual rollout options (see Microsoft's rollout options page).
Set Feature update deferral period to 0 in rings, and make sure feature updates in the ring are not paused, when using these policies (per the Learn page).

## Expedite policies
For zero-days: Devices > Windows Updates > Quality updates > Create > Expedite policy, selecting one supported security update and a restart deadline. Requires the licensing and device prerequisites in the windows-expedited-quality-updates skill.

## Driver updates
Driver update policies (manual or automatic approval) via the deployment service; block
drivers in rings if you manage them separately.

## Reports
Intune reports for feature update and expedite policies, plus Windows Update for Business reports for detailed install states and error codes.

## Gotchas
- GPO or registry WSUS settings on devices can override Intune policy; for co-managed devices check the Windows Update policies workload setting.
- Pausing a ring stops quality and/or feature updates for up to 35 days, after which the pause expires automatically; set a reminder to review it.
- Update ring policies support Windows Pro, Pro Education, Enterprise, Education, IoT Enterprise and Team editions (not Windows Server); use other tooling for servers.

## Verify
Per-ring reports show the current quality update installed by the deadline date; no
devices in conflict; feature version distribution matches the policy.

## Checked
Date: 2026-10-27. Documentation: Microsoft Learn update rings page (35-day pause, supported editions), feature update policies page (set ring feature deferral to 0, rollout options) and expedite policy page. Removed the unconfirmed Windows 10 eligibility option, the old expedite setting name and the exact blade names; example ring values are labelled as examples.
Method: documentation only; no commands were run.
