---
id: computing-software.it-support-helpdesk.intune-mdm.driver-and-firmware-update-policies
name: driver-and-firmware-update-policies
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, driver-update-policy, windows-driver-updates, firmware-updates, manual-approval, automatic-approval, bad-driver-rollback, intune]
level: practitioner
status: docs-checked
description: "Control Windows driver and firmware updates from Intune: automatic vs manual approval policies, deferral, pausing a bad driver, statuses, bulk actions and prerequisites."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/protect/windows-driver-updates-overview"
  - "https://learn.microsoft.com/en-us/mem/intune/protect/windows-driver-updates-policy"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# driver-and-firmware-update-policies

Intune **driver update policies** (Devices > Windows updates > Driver updates tab)
let you review, approve or pause driver and firmware updates that Windows Update
installs. They are built on Windows Autopatch orchestration and work alongside
feature and quality update policies; restarts and user notifications stay under
the normal Windows Update policy settings.

## Prerequisites
- Licences: Microsoft Intune Plan 1 and a Windows licence with the Autopatch
  entitlement.
- Editions: Pro, Pro Education, Enterprise, Education. Enterprise LTSC is not
  supported (use update rings).
- Devices Intune-managed and Entra joined or hybrid joined; telemetry at
  Required or higher; the Microsoft Account Sign-In Assistant service (`wlidsvc`)
  enabled and running; internet access to Intune, Windows Update and Autopatch
  endpoints. Allow Intune to use Windows diagnostic data for reporting.
- Role: Policy and Profile manager (or a custom role with the Device
  configurations permissions); reports need Endpoint Security Manager, Read Only
  Operator, Help Desk Operator or Managed devices/View Reports.
- Nothing may block drivers: in an update ring set the Windows driver setting to
  Allow; in a settings catalog policy set Exclude WU Drivers in Quality Update
  (Windows Update client policies) to Allow Windows Update drivers.

## Approval modes
| Mode | Behaviour | Use |
|---|---|---|
| Automatically approve all recommended driver updates | New recommended drivers are added as Approved and install after the deferral | Most of the fleet |
| Manually approve and deploy | Every new update is added as Needs review; an admin approves each, optionally with a Make available in Windows Update date | Pilot or sensitive hardware |

- The approval type cannot be changed after creation. For automatic policies you
  can still edit Make updates available after (days).
- Deferral: 0 to 30 days, counted from the day the update is added to the
  policy, not the OEM publish date. Example: three days and added June 1 means
  offered June 4.
- In an automatic policy, non-recommended updates (older versions, firmware,
  optional drivers) go to the Other drivers tab as Needs review and need manual
  approval.
- Policies do not enforce OEM Computer Hardware ID (CHID) targeting, so devices
  can get a newer recommended driver instead of a CHID-targeted one.

## The driver list
Two tabs: Recommended drivers (latest version the OEM marked required) and Other
drivers (superseded versions, firmware, optional drivers). It lists what Windows
Autopatch found applicable, not what is installed; Intune holds no inventory of
installed drivers. Columns: name, version, manufacturer, class, release date,
status, applicable devices. Assign devices and save the policy before the list
populates. The Drivers to review column flags policies with updates awaiting
review.

## Statuses
- Needs review: new in the policy (only new updates get it).
- Approved: Windows Update installs the latest approved version, and only if
  newer than the installed driver, so there is no downgrade.
- Paused: stops deployment to more devices and can halt an install in progress;
  it does not roll back a completed install.
- Declined: only from Needs review; an approved update can never be declined,
  only paused (indefinitely if needed).
Re-approving always uses the Make available in Windows Update date (blank means
immediately).

## Handling a bad driver
1. Pause the driver in the policy (select it, Manage driver pane, Actions).
2. If an earlier version is still Approved, Windows Update starts offering that
   one instead (with Autopatch-managed devices the next most recent approved
   version).
3. Driver update policies have no remove or roll-back option, so fix devices
   that already installed it by other means (for example reinstalling the
   previous driver through your normal software deployment).
4. Report to the OEM; approve the fixed version when it appears.

## Bulk actions
Policy page > Bulk actions: Approve, Pause or Decline, up to 100 drivers at a
time, one action type per run (cannot mix). Approve asks for a start date.

## Assignment and rollout
Target each device with a single driver policy, otherwise a driver declined in
one can be approved in another. Stage with test groups first, and consider
aligning availability with your quality update cadence.

## Verify
Driver appears Approved in the policy, pilot devices report it in the driver
update reports, and the device shows the new version after Windows Update scans.

## Checked
2026-11-08. Confirmed against the Microsoft Learn pages Manage Windows driver
updates and Configure Windows driver update policies (both last updated
2026-04-09): prerequisites, approval modes, 0 to 30 day deferral, driver list,
statuses and rules, pause behaviour, bulk actions (100 limit), single-policy
assignment. Removed as unconfirmed: pnputil and Device Manager rollback steps,
OEM tool names, the BitLocker firmware note, and the Autopatch programmatic
controls source.
Method: documentation only; no commands were run.
