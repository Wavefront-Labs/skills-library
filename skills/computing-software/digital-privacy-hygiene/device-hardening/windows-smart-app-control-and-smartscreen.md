---
id: computing-software.digital-privacy-hygiene.device-hardening.windows-smart-app-control-and-smartscreen
name: windows-smart-app-control-and-smartscreen
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, smart-app-control, smartscreen, windows, windows-security, reputation-based-protection, potentially-unwanted-apps, app-control, windows-11]
level: intro
status: docs-checked
description: "Check Smart App Control modes and SmartScreen reputation-based protection settings in Windows Security to reduce risk from untrusted downloads."
sources:
  - "https://support.microsoft.com/en-us/topic/what-is-smart-app-control-285ea03d-fa88-4d56-882e-6698afdb7003"
  - "https://support.microsoft.com/en-us/windows/app-browser-control-in-the-windows-security-app-8f68fb65-ebb4-3cfb-4bd7-ef0f376f3dc3"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows Smart App Control and SmartScreen

**Goal:** block untrusted apps and downloads, a common infection route on home PCs.

## Smart App Control (SAC)
Windows Security > App & browser control > **Smart App Control settings**. Modes:
- **Evaluation**: Windows decides whether you are a good candidate; SAC blocks nothing in this mode. Once evaluation ends,
  or you switch SAC on or off manually, you cannot return to evaluation unless you reinstall or reset Windows.
- **On**: untrusted apps are blocked.
- **Off**: no notifications about untrusted apps; occurs when turned off manually or when evaluation found you were not a
  good candidate.
Recent Windows updates allow SAC to be turned on, or re-enabled, in Windows Security without a clean installation. If
optional diagnostic data was off, turning SAC on may need a reset or reinstall with optional diagnostic data selected.
Back up your files before any reset or reinstall.

## Reputation-based protection (SmartScreen)
App & browser control > Reputation-based protection. Review these settings:
- Check apps and files,
- Phishing protection (by default you are protected only against typing your password into malicious content),
- Potentially unwanted app blocking,
- SmartScreen for Microsoft Store apps.

## Gotchas
- Overriding a SmartScreen warning is a user choice; teach family not to override it for downloads from unknown sites.
- These complement Defender antivirus and a standard (non-admin) account; they do not replace them.

## Checked
2026-10-28. Confirmed on Microsoft Support (Smart App Control FAQ; App and browser control in Windows Security): menu
paths, SAC modes and evaluation behaviour, clean-install relaxation, diagnostic data note, reputation-based settings
named above. Removed (not confirmed): Windows 11 22H2 version gate, script and macro blocking, the no-allowlist claim,
the "Run anyway" button wording, the SmartScreen for Microsoft Edge item.
Method: documentation only; no commands were run.
