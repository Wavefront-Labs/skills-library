---
id: computing-software.it-support-helpdesk.intune-mdm.mam-for-windows-edge
name: mam-for-windows-edge
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, mam-for-windows, app-protection-policy, edge-work-profile, unmanaged-devices, mobile-threat-defense, conditional-access]
level: advanced
status: docs-checked
description: "Protect org data on unmanaged Windows PCs with MAM for Windows: Edge app protection policy settings, health checks, threat level, CA grant and eligibility limits."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/apps/protect-mam-windows
  - https://learn.microsoft.com/en-us/mem/intune/apps/app-protection-policy-settings-windows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mam-for-windows-edge

MAM for Windows gives protected access to org data through Microsoft Edge on personal Windows devices without fully managing them. It combines app configuration policies, app protection policies, Windows Security Center client threat defense, and App Protection Conditional Access.

## Who is eligible
- Unmanaged devices only. If the device is already managed, MAM enrollment is blocked and policy settings are not applied; if it becomes managed after MAM enrollment, settings stop applying.
- The device must not be Entra joined or MDM enrolled to any tenant (including the MAM user's), and not Workplace Joined to more than two users besides the MAM user (three total).
- The Mobile Threat Defense connector for Windows Security Center needs Windows 11 version 22631 (23H2) or later. Windows 10 reached end of support on 14 October 2025 but remains an allowed Intune version with no guarantee of functionality.

## Policy settings (Windows)
Two categories: Data protection and Health checks.
| Setting | Options (default) |
|---|---|
| Receive data from | All sources (default) / No sources; in Edge, No sources controls file upload |
| Send org data to | All destinations (default) / No destinations; in Edge, blocks file download |
| Allow cut, copy and paste for | Any destination and any source (default), org destinations and any source, org destinations and org sources, or none; in Edge it blocks web content only, not the address bar |
| Printing org data | Allow (default) / Block |
| Offline grace period | Block access after 720 minutes (default); wipe data after 90 days (default) |
| Min app version, Min SDK version, Disabled account | Warn, Block or Wipe (not all offer Warn); Disabled account actions are not enforced when the status cannot be confirmed |
| Min OS version / Max OS version | Warn, Block or Wipe; use a Command Prompt style version such as 10.0.22631.3155, not the winver build |
| Max allowed device threat level | Secured, Low, Medium or High, from the MTD connector; Block or Wipe |

## Conditional Access
Use a CA policy targeting all potential users that allows Edge for Windows and blocks other web browsers from Microsoft 365 endpoints (Microsoft's "Require an app protection policy on Windows devices"). The MAM service syncs compliance state per user, per app and per device to Entra CA and includes MTD health. Entra guides users through remediation when blocked.

## Threat health
Windows Security Center supplies a health assessment through a tenant connector. The health state (user, app and device identifiers, predefined state, last update time) is sent only for MAM-enrolled users. Users stop it by signing out of the org account; admins stop it by removing the Windows Security connector.

## Support notes
- Wipe is a selective wipe of protected app data.
- A policy not applying on a device that is Entra joined or MDM enrolled is expected: see eligibility.

## Checked
Date: 2026-11-08. Read in full: "Data Protection for Windows MAM" and "App Protection Policy Settings for Windows" (both updated 2026-04-14). The Edge security page returned 404 and was dropped. Corrections: eligibility is unmanaged devices only, with Workplace Join limits; Windows 11 is required only for the MTD connector. Removed as unconfirmed: the admin center menu paths, the user sign-in flow and work profile registration, edge://policy and DLP internals pages, the Chrome/Firefox user message, kiosk or shared-PC statements, and the Verify steps.
Method: documentation only; no commands were run.
