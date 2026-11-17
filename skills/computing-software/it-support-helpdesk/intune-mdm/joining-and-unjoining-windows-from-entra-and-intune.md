---
id: computing-software.it-support-helpdesk.intune-mdm.joining-and-unjoining-windows-from-entra-and-intune
name: joining-and-unjoining-windows-from-entra-and-intune
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, entra-join-oobe, oobe-local-account, mdm-unenroll, entra-join, windows-enrollment, re-enrollment]
level: practitioner
status: docs-checked
description: "Join Windows to Entra ID in OOBE, tell join from registration, and clear the 'already enrolled' error 8018000a by removing the other work or school account."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/devices/device-join-out-of-box"
  - "https://learn.microsoft.com/en-us/mem/intune/user-help/enroll-windows-10-device"
  - "https://learn.microsoft.com/en-us/troubleshoot/mem/intune/device-enrollment/troubleshoot-windows-enrollment-errors"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# joining-and-unjoining-windows-from-entra-and-intune

## User-driven Entra join in OOBE
- Needs the device registration service configured to allow registering devices, and an
  internet connection; the device may restart several times.
- At "How would you like to set up this device?" choose **Set up for work or school**, then
  sign in with the credential the organisation gave you (password or a method such as a
  passkey).
- Entra ID checks whether MDM enrolment is required and starts it; Windows registers the
  device in the directory and enrols it in MDM if applicable. Managed users go straight to
  the desktop; federated users get the Windows sign-in screen.
- Windows Home editions do not support Entra join; they can use Entra registration (the
  personal-device path) instead. Join and registration are different states.
- Autopilot and Intune pair with OOBE join to configure devices to your standards.

## Enrolling an already-set-up device in Intune
- Windows 10 version 1607 and later and Windows 11 enrol through the Company Portal app or
  website: sign in with the work or school account, Next, Connect, sign in again, Go on
  "Setting up your device", then Done.
- After enrolling, if work resources are unreachable, sync the device.

## Error 8018000a: the device is already enrolled
Cause (per the troubleshooting page): another user already enrolled the device in Intune or
joined it to Entra ID. Settings > Accounts > Work Access shows a message like "Another user
on the system is already connected to a work or school."
1. Sign out, then sign in as the account that enrolled or joined the device.
2. Settings > Accounts > Work Access: remove the work or school account.
3. Sign out and sign in with your own account.
4. Enrol in Intune or join Entra ID again.
Related: error 0x8007064c ("The machine is already enrolled") can come from a cloned image
of an already-enrolled computer.

## Pitfalls
- Registry and Task Scheduler clean-up of enrolment leftovers is risky; follow Microsoft's
  troubleshooting page (it warns to back up the registry first) rather than deleting keys
  from memory.

## Verify
Settings > Accounts > Access work or school shows the device connected to Microsoft Entra
ID with the areas managed by IT, the device appears in Intune, and a sync succeeds.

## Checked
2026-11-08. Confirmed on the Entra OOBE join tutorial: prerequisites, the OOBE choices, MDM enrolment step, Home edition limitation, verification via Access work or school. Confirmed on the Intune user-help enrolment page: Company Portal steps and supported versions. Confirmed on the enrolment troubleshooting page: 8018000a cause and fix, 0x8007064c cloned-image cause. Removed (not on the pages read): Settings join path and `AzureAD\user` sign-in detail, device-limit and MFA prerequisites, OOBE Microsoft-account and answer-file advice, the Task Scheduler GUID and HKLM Enrollments key procedure, hybrid-join and BitLocker-escrow statements, and the dsregcmd step.

Method: documentation only; no commands were run.
