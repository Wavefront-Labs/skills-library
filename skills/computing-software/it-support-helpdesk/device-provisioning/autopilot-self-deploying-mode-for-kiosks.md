---
id: computing-software.it-support-helpdesk.device-provisioning.autopilot-self-deploying-mode-for-kiosks
name: autopilot-self-deploying-mode-for-kiosks
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, self-deploying-mode, autopilot, kiosk, shared-devices, tpm-attestation]
level: practitioner
status: draft
description: "Deploy kiosks and shared devices with Autopilot self-deploying mode: requirements, profile settings, device-only targeting, pairing with kiosk policy, and attestation errors."
sources:
  - "https://learn.microsoft.com/en-us/autopilot/self-deploying"
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/kiosk-settings-windows"
  - "https://learn.microsoft.com/en-us/autopilot/troubleshooting-faq"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# autopilot-self-deploying-mode-for-kiosks

## When to use
Devices with no assigned user: reception kiosks, digital signage, shared shop-floor PCs,
meeting room PCs. The device enrols itself; nobody types credentials.

## Requirements
- Windows 10 1903+ / Windows 11, TPM 2.0 with attestation, physical device.
- Network at OOBE (Ethernet strongly recommended, otherwise a pre-provisioned Wi-Fi).
- Autopilot profile Deployment mode = **Self-Deploying**, join type Microsoft Entra joined
  (hybrid join is not supported).
- ESP enabled so the device does not reach the desktop before apps and kiosk policy land.

## Targeting
Everything must target the **device** group (by group tag, e.g. `[OrderID]:KIOSK`).
User-targeted apps and policies never apply because there is no enrolling user; nor do
user-based licences or OneDrive.

## After enrolment
- Kiosk configuration profile (single-app or multi-app kiosk with an auto-logon account),
  or a Shared multi-user device profile for shared PCs.
- Lock down with restrictions, Windows Update rings suited to always-on devices, and
  scheduled restarts.

## Troubleshooting
| Error | Meaning |
|---|---|
| Attestation failure (often 0x801C03EA, 0x800705B4 timeouts) | TPM not ready, firmware old, clock wrong, or attestation endpoints blocked |
| Device lands at a user sign-in page | Profile not self-deploying, or not assigned when the device first booted |
| ESP stuck | A device app requires user context or a reboot loop |

Collect logs with `mdmdiagnosticstool.exe -area Autopilot;TPM -cab <file>.cab`.

## Gotchas
- Re-using a device previously self-deployed needs the old Entra device object removed
  first or enrolment can fail.
- Kiosks still need a primary owner group for support and an asset record.

## Verify
Device boots from OOBE to the kiosk app with no human input, shows in Intune with no
primary user, and kiosk policy reports Succeeded.
