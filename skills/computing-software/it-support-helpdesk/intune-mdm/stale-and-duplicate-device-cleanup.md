---
id: computing-software.it-support-helpdesk.intune-mdm.stale-and-duplicate-device-cleanup
name: stale-and-duplicate-device-cleanup
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, stale-device-cleanup, duplicate-devices, entra-stale-devices, autopilot-records, graph-powershell, intune, graph-device-queries]
level: practitioner
status: docs-checked
description: "Clean stale and duplicate device records across Intune, Entra ID and Autopilot: activity timestamp, disable then delete, Autopilot deregistration order, BitLocker keys."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/devices-wipe"
  - "https://learn.microsoft.com/en-us/entra/identity/devices/manage-stale-devices"
  - "https://learn.microsoft.com/en-us/autopilot/registration-overview"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# stale-and-duplicate-device-cleanup

A Windows device can have three separate records: an **Intune managed device**, a **Microsoft Entra device object** and a
**Windows Autopilot registration**. They are cleaned up in different places, and order matters.

## Entra ID: what "stale" means
A stale device is registered but has not accessed cloud apps for a timeframe you define. The property is
`ApproximateLastSignInDateTime` (the activity timestamp, the Activity column on the All devices page). Entra evaluates it
when a Conditional Access policy requiring managed devices or approved apps triggers, when Entra joined or hybrid joined
Windows 10 or newer devices are active on the network, and when Intune managed devices check in. The value is replaced only
if it differs from the existing value by more than 14 days (plus or minus 5 days variance), so do not treat a timestamp
younger than 21 days as stale. Some active devices have a blank timestamp. It is not an audit; use sign-in logs for frequent updates.

Roles needed to update devices: Cloud Device Administrator or Intune Administrator.

## Process
1. Define the timeframe and a policy; allow for long leave, which can make a device look stale.
2. If the device is under Intune or other MDM control, retire it in the management system before disabling or deleting it.
3. **Disable** first and wait a grace period; a deletion cannot be undone.
4. Delete after the grace period. Back up any BitLocker recovery keys you need first: keys are stored on the device object in
   Entra, so deleting it deletes them with no recovery.

```powershell
Connect-MgGraph -Scopes Device.ReadWrite.All
$dt = (Get-Date).AddDays(-90)
Get-MgDevice -All | Where {$_.ApproximateLastSignInDateTime -le $dt} |
  Select-Object AccountEnabled, DeviceId, OperatingSystem, DisplayName, TrustType, ApproximateLastSignInDateTime
# disable: Update-MgDevice -DeviceId $Device.Id -BodyParameter @{ accountEnabled = $false }
# delete only the disabled, older ones: Remove-MgDevice -DeviceId $Device.Id   (no prompt, no undo)
```
The page's examples disable at 90 days and delete devices inactive for 120 days that are already disabled.

Disabling denies any authentication that uses the device as identity: hybrid joined users may still sign in to on-premises
but cannot reach Entra resources such as Microsoft 365; Entra joined users cannot sign in to the device.

## By join type
- Entra hybrid joined Windows 10 or newer: disable or delete in on-premises AD and let Entra Connect sync it. Deleting only
  in Entra re-syncs it as a new object in Pending state needing re-registration. Removing it from sync scope deletes the
  Entra device; adding it back creates a Pending object.
- Entra joined and Entra registered: disable or delete in Entra ID.
- Deleting the object does not remove registration on the client; it only blocks resource access that uses the device as identity.

## Autopilot
Autopilot devices are system-managed: do not delete them in Entra. Deleting the Entra object of a registered Autopilot device
breaks later redeployments (user-driven creates a new object without the ZTDID tag; self-deploying and pre-provisioning fail).
Deregister only when a device permanently leaves the organisation (repair or end of life):
1. Delete the device from Intune (Devices > Windows; note the serial number first).
2. Devices > Enrollment > Windows Autopilot > Devices: find it by serial number, Unassign user if available, then Delete; use
   Sync and Refresh until it disappears.
3. Entra joined: no further steps; avoid manually deleting the Entra object. Hybrid joined: delete the computer object in
   on-premises AD DS; avoid deleting it in Entra. Wrong order can leave orphaned or unrecoverable records.
A partner deregistering in Partner Center only removes the Autopilot registration, not MDM enrolment or Entra join.
Use `Get-MgDeviceManagementWindowsAutopilotDeviceIdentity` to compare Autopilot devices with your cleanup list.

## Duplicates
Typical causes: OS reinstall, reimage or recovery, broken hybrid join trust, incomplete registration (Pending objects).
Duplicates make it hard for the helpdesk to find the active device; compare activity timestamps and clean up the stale one.

## Verify
Counts reconcile between Intune, Entra and your asset register, and no in-use device loses access (watch sign-in failures).

## Checked
Date: 2026-11-08. Read in full: Entra "Manage stale devices" (page updated 2025-06-27) and Autopilot "registration
overview" (2026-02-05). The Intune wipe page was read and gives no cleanup rule detail. Removed as unconfirmed: Intune
Device clean-up rules and its 30-270 day range, LAPS passwords stored on the device object, the Windows 10 1803 automatic
registered-object cleanup, Apple ADE reappearing from ABM, same-serial keep-latest advice, and the Conditional Access
noncompliant-duplicate claim. Corrected: Autopilot order is Intune then Autopilot, with no manual Entra delete.
Method: documentation only; no commands were run.
