---
id: computing-software.it-support-helpdesk.intune-mdm.feature-update-policies-target-version
name: feature-update-policies-target-version
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, feature-update-policy, windows-feature-updates, target-version, windows-11-upgrade, gradual-rollout, wufb-ds, intune]
level: practitioner
status: docs-checked
description: "Pin and move Windows versions with Intune feature update policies: required vs optional, rollout, multiple-policy evaluation, safeguard holds, and moving off ring deferrals."
sources:
  - "https://learn.microsoft.com/en-us/intune/device-updates/windows/manage-feature-updates"
  - "https://learn.microsoft.com/en-us/intune/device-updates/windows/configure-feature-update-policy"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# feature-update-policies-target-version

A **feature update policy** names one Windows version and keeps devices on it
until the policy is changed or removed. Update-ring deferrals only delay; they
do not pin. Unlike pausing feature updates in a ring (which expires after
35 days), a feature update policy stays in force.

## Prerequisites
- Microsoft Intune Plan 1 plus a Windows licence with the Autopatch entitlement.
- Pro, Pro Education, Enterprise or Education (Enterprise LTSC not supported;
  use update rings).
- Intune-managed, Entra joined or hybrid joined; telemetry at Required or
  higher; Microsoft Account Sign-In Assistant service (`wlidsvc`) running; the
  device can reach Intune, Windows Update and Autopatch endpoints.
- Diagnostic data allowed for Intune so reports work.
- Role: Policy and Profile manager (or a custom role with Device
  configurations permissions).

## Create
Devices > Windows > Windows updates > Feature updates > Create profile.
- Deployment settings: name, then Feature update to deploy (only versions still
  in support are listed).
- Availability: **required** (installs automatically per device settings) or
  **optional** (the user must open Windows Update and select Download; optional
  needs a Windows Autopatch licence).
- Rollout options: when and how fast the update becomes available (scheduled
  or gradual; see the Rollout options for Windows Updates page).
- Assignments: device groups.
The latest applicable monthly quality update is included when a feature update
installs.

## Behaviour to remember
- No downgrade: a device already on a newer version is left alone.
- Each policy targets one version. With several policies on a device, Windows
  Update offers only one feature update at a time, always the latest applicable
  version. Windows 11 counts as later than Windows 10, so a Windows 10 device
  targeted by both gets Windows 11.
- Same version in two policies, one required and one optional: offered as
  required.
- Optional to required: devices that have not started install at the next
  Windows Update scan. Required to optional: devices already pending restart
  usually continue; only devices not yet started switch.
- Policies do not apply during the Autopilot OOBE; they apply at the first
  Windows Update scan after provisioning.
- Policy changes are evaluated by Windows Update, normally within about 10
  minutes but sometimes longer.
- A policy that no longer targets an Autopatch-managed device leaves it
  enrolled in Autopatch and offered no feature update until it gets a new
  policy, is unenrolled from Intune, or is removed through the Autopatch Graph
  API.

## Interaction with update rings
- Set the ring's Feature update deferral period (days) to 0 and do not pause
  feature updates in the ring. Microsoft recommends dropping ring deferrals
  entirely once you use feature update policies; rings still govern restarts,
  deadlines and notifications.
- Safe switch order: create and assign the feature update policy, wait several
  minutes, confirm the Feature updates (Organizational) report shows OfferReady
  for the targeted devices, then set the ring deferral to 0. Removing the
  deferral first can let a device scan and be offered an unintended update.

## Co-management
With Configuration Manager co-management, a newly moved Windows Update
workload can briefly let devices update past the target. Create and assign the
policy first, check the report (Reports > Windows updates > Feature Updates
report) shows OfferReady or later, then switch the workload.

## Managing policies
The list shows feature update version, assigned, Support (Supported, Support
Ending when within two months of end of support, Not supported) and Support End
Date (Enterprise and Education dates). A Last Scanned Time of Not scanned yet
means no user has logged on and run a scan yet.

## Stuck upgrades
- Safeguard holds: the device is not offered a version while a hold applies;
  the hold lifts when Microsoft resolves the issue. Known issues are on the
  Windows release health pages.
- Check the feature update report for per-device state, and confirm the ring
  deferral is 0 and not paused.

## Verify
`winver` shows the target version on pilot devices and the feature update report
shows them updated without errors.

## Checked
2026-11-08. Confirmed against the Microsoft Learn pages Manage Windows feature
updates and Configure Windows feature update policies (both last updated
2026-04-09): prerequisites, create steps, required vs optional, multi-policy
evaluation, ring interaction, switch order, co-management, support status
column. Removed as unconfirmed: the Windows 11 ineligibility option, error code
list, SetupDiag, disk space figure, licence list, user-initiated option, and the
Windows Autopatch overview and release health sources (not read for claims).
Method: documentation only; no commands were run.
