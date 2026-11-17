---
id: computing-software.it-support-helpdesk.intune-mdm.windows-automatic-mdm-enrollment
name: windows-automatic-mdm-enrollment
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, intune, mdm-user-scope, automatic-enrollment, entra-join, windows-enrollment, wip-user-scope, enrollment-restrictions]
level: practitioner
status: docs-checked
description: "Configure and support Windows automatic Intune enrollment: MDM user scope, WIP scope clash, enrollment paths, restrictions that block enrollment, and duplicate records."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/windows-enroll"
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/windows-enrollment-methods"
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/enrollment-restrictions-set"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# windows-automatic-mdm-enrollment

Automatic enrollment lets a Windows device enroll in Intune when it joins or registers in Microsoft Entra ID: a user adds a
work or school account to a personal device, or a corporate-owned device joins Entra ID. It is used with BYOD, bulk
enrollment, Group Policy, Windows Autopilot (user-driven and self-deploying) and co-management.

## Enable it
Needs a Microsoft Intune subscription and Microsoft Entra ID P1 or P2 (automatic MDM enrollment is a premium Entra feature),
and the built-in Global Administrator role. In the Intune admin center: Devices > Device onboarding > Enrollment > Windows
tab > **Automatic Enrollment**.

| Setting | Value | Notes |
|---|---|---|
| MDM user scope | None, Some, All | None: disabled, users must start enrollment themselves (you can still manage devices). Some: selected users. All: all users |
| MDM terms of use, discovery and compliance URLs | Defaults | Use the default values |
| WIP user scope | None (or Some, with no overlap) | For BYOD, set MDM scope to All or Some and keep users out of both scopes |
| Disable MDM enrollment when adding work or school account | Off by default (public preview) | Turn on if you enforce Windows MAM; affects the registration flow only, not the Settings flow |

If a user is in both MDM and WIP scope: MDM scope wins on a corporate-owned device (it enrolls automatically); WIP scope
wins on a BYOD device (no Intune device management). Likewise, in BYOD scenarios where both the MDM and MAM user scopes are
enabled for a user, MAM takes precedence and the device is not enrolled.

Microsoft recommends requiring multifactor authentication during registration (Conditional Access; Entra ID P1 or P2) and
starting with a pilot group. If you are not using automatic enrollment, create a CNAME DNS alias to the Intune enrollment server.

## How a device enrolls
- **Entra join** in OOBE or from Settings with a work account: the device becomes corporate-owned.
- **Windows Autopilot** user-driven or self-deploying.
- **Group Policy** for Entra hybrid joined devices: a scheduled task runs after an Entra-synced user signs in.
- **Co-management** with Configuration Manager.
- **BYOD** (Entra registered): Connect a work or school account in Settings, the Company Portal app, or a Microsoft 365 app
  sign-in with "Allow my organization to manage my device".
- **Bulk** with a provisioning package from Windows Configuration Designer.

## When "it didn't enroll"
1. The user must be in MDM user scope and licensed; check the automatic enrollment settings above.
2. Enrollment restrictions: a personal-device block rejects unauthorised Windows enrollments. Authorised paths are Autopilot,
   GPO or Configuration Manager auto-enrollment, bulk provisioning package, and a device enrollment manager account. Blocked
   for personal devices: Add Work Account from Settings, MDM-only enrollment from Settings, Company Portal enrollment and
   Microsoft 365 app enrollment. The Entra join methods are marked corporate-owned and blocked unless registered with Autopilot.
3. Device limit restriction (1 to 15) applies to user-driven enrollments; a standard non-admin account can enroll 15
   devices. Device enrollment managers can enroll up to 1000 corporate devices. Shared-device-mode scenarios (co-managed,
   GPO, Entra joined, Autopilot, DEM) are not covered by Intune device limits.
4. Restriction changes use assignment filters; allow about 15 minutes after adding a user to a group.
5. A workplace-joined device that was ever Entra joined to the tenant can be blocked: deregister and remove its Entra object first.

## Gotchas
- If automatic MDM enrollment is disabled and devices are Entra joined, you see two records after enrollment. Tell users to go
  to Settings > Accounts > Access work or school and Connect with the same account.
- Users reach the Company Portal website through Microsoft Edge to see version-specific app filtering.

## Verify
The device appears in Intune and Settings > Accounts > Access work or school shows the account managed; enrollment
reports track incomplete user enrollments.

## Checked
Date: 2026-11-08. Read in full: "Set up automatic enrollment for Windows devices" (updated 2026-04-09), "Enroll devices in
Microsoft Intune" (2026-04-29) and "What are enrollment restrictions?" (2026-04-09). Removed as unconfirmed: the Entra admin
center Mobility path, a default device limit of 5, dsregcmd checks, Event Viewer event 75, Windows Home edition
limitation, re-join advice for users who joined before being in scope, and the DEM "bypass the device limit" and
Conditional Access claims. Corrected: the page names the WIP user scope (not MAM) for the setting clash.
Method: documentation only; no commands were run.
