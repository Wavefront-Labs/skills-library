---
id: computing-software.it-support-helpdesk.device-provisioning.recovering-and-wiping-returned-devices
name: recovering-and-wiping-returned-devices
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, device-return, offboarding, asset-recovery, remote-wipe, autopilot-reset, data-sanitisation, mobile-device-sanitization]
level: practitioner
status: draft
description: "Get leaver devices back and ready: return kits and tracking, chasing unreturned kit, intake checks, legal hold quarantine, wipe or reset for reuse, and disposal paths."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/devices-wipe"
  - "https://csrc.nist.gov/pubs/sp/800/88/r1/final"
  - "https://learn.microsoft.com/en-us/autopilot/windows-autopilot-reset"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# recovering-and-wiping-returned-devices

## Getting it back
- Office leavers: collect on the last day against the asset record (laptop, charger, dock,
  phone, tokens, badge).
- Remote leavers: send a prepaid return kit with tracking a week before the last day; log
  the tracking number on the asset record.
- Unreturned devices: chase via HR/manager per policy; meanwhile lock (Intune Lock / Lost
  Mode) and disable the account so the device is useless; wipe when recovery is unlikely.

## Intake
1. Match serial to the asset record; note condition, damage, missing accessories (photos).
2. Check for legal hold or investigation flags with HR/legal. If held: do not wipe; seal,
   label, store securely with chain of custody.
3. Otherwise apply a standard quarantine (e.g. 14-30 days) if policy wants a window to
   recover forgotten data.

## Prepare for reuse
- Windows corporate: Intune **Wipe** (keeps Autopilot registration so it re-enrols) or
  Autopilot Reset; confirm it lands at OOBE.
- iOS/iPadOS/macOS: wipe via MDM; make sure Activation Lock is cleared (see
  clearing-activation-lock-and-account-locks).
- Android: wipe; check Factory Reset Protection does not block setup.
- Clean, test (battery health, keyboard, screen), update firmware, return to stock with
  status "Ready".

## Dispose instead when
Out of warranty and beyond refresh age, damaged beyond economic repair, or failed
battery health. Sanitise per NIST SP 800-88 (crypto erase or secure erase, then verify),
remove from Autopilot, Intune and Entra, and send to the ITAD vendor with certificates of
destruction recorded.

## Gotchas
- Wiping before checking legal hold destroys evidence.
- Deleting the Autopilot registration on a device you plan to reuse forces a re-import.

## Verify
Asset record shows returned, wiped and status (stock or disposed), device boots to OOBE
or setup for its next user, and no lock blocks enrolment.
