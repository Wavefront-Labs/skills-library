---
id: computing-software.it-support-helpdesk.device-provisioning.autopilot-device-preparation
name: autopilot-device-preparation
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, autopilot-device-preparation, autopilot-v2, intune, entra-join, provisioning]
level: practitioner
status: draft
description: "Set up and support Windows Autopilot device preparation (v2): device group owned by the provisioning service principal, policy settings, app limits, monitoring and v1 precedence."
sources:
  - "https://learn.microsoft.com/en-us/autopilot/device-preparation/overview"
  - "https://learn.microsoft.com/en-us/autopilot/device-preparation/tutorial/user-driven/entra-join-workflow"
  - "https://learn.microsoft.com/en-us/autopilot/device-preparation/compare"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# autopilot-device-preparation

## What is different from classic Autopilot
- No hardware hash pre-registration: the user signs in at OOBE and the policy that targets
  that **user** group applies. Corporate identifiers can restrict enrolment to known
  devices.
- Devices are added to a chosen **device security group** at enrolment; apps and scripts
  assigned to that group install during OOBE.
- Entra join only; requires Windows 11 22H2 or later with recent updates.
- Better reporting: Devices > Monitor > Windows Autopilot device preparation deployments.

## Setup
1. Create an assigned device security group. Its **owner** must be the service principal
   "Intune Provisioning Client" (AppID `f1346770-5b25-470b-88bd-d5744ab7952c`); in some
   tenants it appears as "Intune Autopilot ConfidentialClient". Without this, devices are
   never added.
2. Create the device preparation policy: deployment mode user-driven, join type Entra, user
   account type (standard/admin), timeout, the device group, and the apps/scripts to install
   during OOBE (there is a cap on the number of apps; check the current limit).
3. Assign the policy to a **user** group.
4. Make sure users can join devices to Entra and enrol in Intune (MDM user scope).

## Precedence
If the device is registered for classic Autopilot (has a v1 profile), the v1 profile wins.
Remove the Autopilot registration for devices that should use device preparation.

## Troubleshooting
- Apps not installing in OOBE: not assigned to the device group, group owner wrong, or
  app type not supported in OOBE (check the docs list of supported types).
- Deployment report shows the phase and the app/script that failed.
- Device not added to the group: check the group owner first.

## Verify
The deployment report shows Success for the device, it is a member of the device group,
and the selected apps are installed at first desktop.
