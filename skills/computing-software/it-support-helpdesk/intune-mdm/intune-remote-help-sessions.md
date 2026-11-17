---
id: computing-software.it-support-helpdesk.intune-mdm.intune-remote-help-sessions
name: intune-remote-help-sessions
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, intune-remote-help, remote-help, rbac, elevation, android-remote-help, remote-support]
level: practitioner
status: docs-checked
description: "Run Intune Remote Help: helper and sharer sign-in, launching from the device page, view vs full control, elevation, unattended control, unenrolled devices, reports and audit logs."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/fundamentals/remote-help"
  - "https://learn.microsoft.com/en-us/mem/intune/fundamentals/remote-help-windows"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# intune-remote-help-sessions

Remote Help is Intune's cloud remote support tool. The **helper** (support) and **sharer**
(end user) must both sign in with Microsoft Entra accounts from your organization, so it
cannot assist users in another tenant.

## Tenant behaviour
- Not enabled by default; turning it on is tenant-wide, and it must be on before users can
  authenticate through your tenant.
- Support for **unenrolled devices** is off by default; it does not apply to the helper's
  device or to unattended control (Intune-enrolled devices only). Auditing of unenrolled
  sessions is limited.
- RBAC controls who can help, who can only view, who can request full control and who can
  run elevated.
- Conditional Access can require MFA or compliant devices for helpers and sharers; it
  applies to attended sessions, not unattended access.
- Reports in the Intune admin center show who helped whom, on which device and for how
  long, plus active sessions; audit logs are under Tenant Administration > Audit Logs.
- A web app lets a sharer who cannot install the native app share their screen
  (view-only for the helper).

## Attended session from Intune (Windows)
1. Intune admin center > Devices > All devices > the device > remote actions bar > **New
   remote assistance session > Remote Help > Continue**.
2. **Initiate attended control** to request view or full control. A notification is sent
   to the sharer; use **Retry** if it did not arrive. An offline device shows an error;
   a noncompliant device shows a warning banner.
3. Both sides sign in. Each sees the other's name, job title, company, profile picture and
   verified domain; the sharer chooses Allow or Decline. The helper can start with screen
   sharing and ask for full control, which the sharer can decline.
4. A compliance warning appears if the device fails its assigned compliance policies.
5. **Elevation**: a helper with the elevation permission can enter UAC credentials on the
   sharer's device. If the EnableSecureCredentialPrompting policy is enabled it blocks
   elevation in Remote Help sessions. If a helper used elevation and the sharer ends the
   session, the sharer is signed out (a dialog warns them); if the helper ends it, they
   are not.
6. Either side ends with **Leave**.
- Without Intune launch, the sharer can open the Remote Help app and enter the helper's
  session code (8 digits on macOS). Unenrolled Windows: helper opens the app > Give help >
  Get a security code.

## Unattended control
- Windows: **Initiate unattended control** from the same menu. Only for physical,
  corporate-owned, Intune-managed Windows devices; BYOD is not supported, and missing
  prerequisites are listed. One helper and one session per device. If a user is signed
  in they get a prompt, and if they do not respond within 30 seconds the session starts;
  their session is locked and preserved, and they can reclaim the device by signing in.
  Remote Help opens the Windows App web client in a new tab where the helper signs in
  inside the session; a standard account does not gain admin rights.
- Android: needs the device enrolled as Android Enterprise dedicated. Attended requests
  time out after 5 minutes; unattended starts after 30 seconds without a response. On
  Android 13 the PIN/pattern UI cannot be shown remotely, but keyboard input can unlock.

## macOS
- Native app needs Accessibility and Screen and System Audio Recording permissions on
  first run (Settings > Privacy & Security). The helper can request screen sharing or
  full control from the Intune admin center; web-app sharers allow screen sharing only.
- Unenrolled macOS: helper goes to the helper page (aka.ms/rhh), shares the 8-digit code;
  sharer goes to aka.ms/rh.
- Remote Help warns, without blocking, when the sharer's device is unenrolled.

## Azure Virtual Desktop
An AVD desktop session gives the whole remote desktop; RemoteApp gives only the published
app. Intune-launched requests to AVD desktop broadcast to all active users on the host,
so use the security code method.

## Checked
Date: 2026-11-07. Read in full: Intune "Use Remote Help" overview and "Using Remote Help with Microsoft Intune" (get help,
provide help, unattended, unenrolled, AVD, macOS, Android sections). Removed as unconfirmed (these pages do not cover them):
licensing statements, the Tenant administration > Remote Help > Settings path, the Help Desk Operator built-in role claim and
specific permission names, "disable chat" setting, Samsung/Zebra specifics, the endpoints/WebView2 troubleshooting, "licence propagation takes hours",
the Monitor/Session report path, and the Verify step. Remote-help-android source dropped (it redirects to the same overview page).
Method: documentation only; no commands were run.
