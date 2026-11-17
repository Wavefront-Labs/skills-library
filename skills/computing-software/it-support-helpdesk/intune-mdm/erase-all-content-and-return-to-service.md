---
id: computing-software.it-support-helpdesk.intune-mdm.erase-all-content-and-return-to-service
name: erase-all-content-and-return-to-service
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, return-to-service, erase-all-content-and-settings, obliteration, macos-wipe, ios-wipe, device-redeployment]
level: practitioner
status: docs-checked
description: "Redeploy Macs fast: Erase All Content and Settings, the Intune Wipe action with its Obliteration Behavior options, Recovery PIN for non-T2 Macs, and wipe limits."
sources:
  - "https://support.apple.com/en-us/102664"
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/devices-wipe"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# erase-all-content-and-return-to-service

Apple's Erase All Content and Settings (EACS) resets a Mac quickly while keeping the
installed operating system. Intune's Wipe action can drive the same flow remotely.

## macOS: Erase All Content and Settings
- Requires macOS Monterey 12 or later and a Mac with Apple silicon or the Apple T2 Security
  Chip. It erases data, settings and apps while keeping the installed OS.
- User path: System Settings > General > Transfer or Reset > Erase All Content and
  Settings; it asks for the administrator password and Apple Account password. If other
  volumes block it (for example a Boot Camp Windows install), remove them first.
- After the erase the Mac restarts, activates and runs Setup Assistant as if new.

## Intune Wipe (Devices > All devices > device > Remove data > Wipe)
- Supported platforms include iOS/iPadOS, macOS, Windows, ChromeOS, tvOS 10.2+, visionOS
  1.1+ and Android Enterprise corporate-owned modes. Roles: Help Desk Operator, School
  Administrator, or a custom role with Remote tasks/Wipe.
- A tenant can submit up to 500 Wipe actions per day (individual, bulk and Graph combined).
- macOS: enter a 6-digit Recovery PIN, required to reinstall the OS on Macs without a T2
  chip (typically 2018 or earlier, or macOS 10.14 or earlier); record it, it is not shown
  after the wipe.
- macOS **Obliteration Behavior** (fallback when EACS fails): Default (preflight failure
  returns Error and the device still attempts to erase), Do not obliterate, Obliterate
  with warning, Always obliterate (EACS not attempted; T2 and later always obliterate).
- iOS/iPadOS eSIM devices keep the cellular plan unless you select the option to remove it.
- Windows options: keep enrolment state and user account (doWipePersistUserData), continue
  even if power is lost (doWipeProtected, can leave some devices unbootable), or no
  options (doWipe).
- After a wipe, also remove the device from Windows Autopilot or Entra ID if applicable.

## Procedure
1. Confirm backups and approval to wipe; record the action in the ticket.
2. Choose Wipe, set the macOS PIN and Obliteration Behavior, and confirm.
3. Watch the device re-enrol and reach Setup Assistant.

## Verify
The device reappears in Intune after the wipe and Setup Assistant starts as for a new Mac.

## Checked
2026-11-08. Confirmed on Apple Support (Erase your Mac) and Microsoft Learn (Wipe devices with Microsoft Intune): everything above. Removed because the pages read do not state them: iPhone/iPad Return to Service requirements (iOS 17+, ReturnToService payload, Wi-Fi profile rules; the Apple Platform Deployment page fetched only returned the guide contents, not the topic), Activation Lock bypass-code and ABM steps, the ObliterationBehavior/EraseDevice command names, and the BYOD Retire advice. Check Apple's Use Return to Service for Apple devices guide before relying on those.

Method: documentation only; no commands were run.
