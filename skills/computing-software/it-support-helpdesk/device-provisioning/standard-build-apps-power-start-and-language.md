---
id: computing-software.it-support-helpdesk.device-provisioning.standard-build-apps-power-start-and-language
name: standard-build-apps-power-start-and-language
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, core-applications, power-settings, start-layout, build-versioning, language-packs, standard-build]
level: practitioner
status: draft
description: "Define the standard Windows build contents: core application set, power settings, default Start and taskbar layout, language and regional settings, and versioned build records."
sources:
  - "https://learn.microsoft.com/en-us/windows/configuration/start/layout"
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/languages-overview"
  - "https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-power"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# standard-build-apps-power-start-and-language

## Core application set
- Everyone: M365 Apps (channel per policy), Teams, Edge (default browser), OneDrive,
  Company Portal, security agents (EDR, DLP), VPN/ZTNA client, PDF reader, compression
  tool if needed. Everything else is role-based or self-service available.
- Deployed as Required in Intune to all devices (or via ESP blocking list for the
  critical few), each with an owner and an update method (auto-update, Intune
  supersedence, or Store via winget).

## Power settings
- Intune settings catalog (Power CSP) or `powercfg`:
  - Display off: 10 min on battery, 15-20 min plugged in.
  - Sleep: 15-30 min on battery, 30-60 min plugged in (or never for desktops that need
    overnight patching, with Wake-on-LAN instead).
  - Lid close: sleep; power button: sleep or shut down.
  - Require sign-in on wake.
- Check: `powercfg /getactivescheme`, `powercfg /a` (Modern Standby S0 vs S3),
  `powercfg /sleepstudy` for battery drain on Modern Standby.

## Start and taskbar layout (Windows 11)
- Start pinned apps: export from a reference machine
  (`Export-StartLayout -Path <OUTPUT_DIR>\start.json`), deploy with Intune settings catalog
  **Start > Configure Start Pins** (JSON). Applies the pins; users can change them unless
  locked.
- Taskbar pins: XML layout with `<taskbar:TaskbarPinList>` via the "Start Layout" policy
  (Windows 11 22H2+); `PinListPlacement="Replace"` vs append.
- Keep pins few: Edge, Outlook, Teams, File Explorer, Company Portal.

## Language packs and regional settings
- Install language at build time (Autopilot device language from OOBE, or Settings >
  Time & language; `Install-Language de-DE` on Windows 11), then set system locale,
  user locale, keyboard and time zone (`Set-WinSystemLocale`, `Set-WinUserLanguageList`,
  `Set-TimeZone`, or automatic time zone with location services).
- Intune: language packs via Store apps or scripts; "Region/time zone" in Autopilot
  profile (or user selects in OOBE).
- Copy settings to the welcome screen and new users (Region > Administrative) for shared
  devices.

## Build versioning
- Version the build like software: `2026.10` = Windows 11 24H2, baseline policy set v12,
  app set v8. Record changes in a changelog (what changed, why, tested by, date).
- Stamp the build version on devices (registry value or Intune custom attribute) so
  tickets can say which build a device has.
- Pilot every build change on a test ring before production.

## Verify
A new device shows the core apps, power plan, Start pins and the user's language and
time zone, and reports the current build version.
