---
id: computing-software.it-support-helpdesk.user-support-communication.capturing-environment-and-asset-details
name: capturing-environment-and-asset-details
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, ticket-documentation, environment-details, asset-information, configuration-item, msinfo32, system-information, winver, about-this-mac]
level: intro
status: draft
description: "Capture the environment facts every ticket needs fast: asset and CI, OS build, app version, network location, using one-liners, remote tools and the CMDB instead of asking users."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-computerinfo"
  - "https://support.apple.com/guide/mac-help/welcome/mac"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# capturing-environment-and-asset-details

Goal: tickets record the facts that decide most diagnoses — which device,
which build, which version, which network — without a ten-question
interrogation.

## The minimum set
| Field | Why |
|---|---|
| Asset tag / hostname → **CI** on the ticket | history, warranty, model-wide issues |
| OS and build (e.g. Windows 11 23H2 22631.4317) | update-related faults |
| App and version/channel | known bugs per version |
| Network: office/site, home, VPN on/off, Wi-Fi/wired | half of "it's slow" |
| Account: user, licence, role | permissions/licensing |
| Peripherals/dock if hardware-related | dock firmware issues |

## Get it without asking the user
- Ticket form auto-fills caller's primary device from CMDB/Intune; check
  it's the device in question.
- Remote tool/RMM device panel shows OS, build, uptime, last user.
- Intune device record: OS version, compliance, last check-in, apps.

## One-liners when you're on the device
```powershell
Get-ComputerInfo -Property CsName, OsName, OsVersion, OsBuildNumber, BiosSerialNumber
(Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion').DisplayVersion   # e.g. 23H2
```
- Office: File → Account → About (version and channel).
- `winver`, `msinfo32` (export as .nfo for vendors).
- macOS: Apple menu → About This Mac → More Info; `sw_vers`;
  `system_profiler SPHardwareDataType`.
- Mobile: Settings → General → About / About phone.

## Asking users (when you must)
Ask by what they can see: "What's the number on the sticker on the bottom /
lid?", "Are you in the office or at home today?", "Can you read me the
error exactly?". Teach them where the asset tag is.

## Gotchas
- Users with multiple devices: confirm which one.
- Hostname reuse after reimage — use serial for certainty.
- Keep this in structured fields (CI, location) not just free text, so
  trend reports work.

## Verify
QA sample: tickets with a correct CI and OS/app version ≥ 90 %.
