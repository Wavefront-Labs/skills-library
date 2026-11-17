---
id: computing-software.it-support-helpdesk.intune-mdm.windows-kiosk-and-assigned-access
name: windows-kiosk-and-assigned-access
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, windows-kiosk, assigned-access, single-app-kiosk, multi-app-kiosk, autologon, edge-kiosk-mode, configuration-profile]
level: practitioner
status: docs-checked
description: "Build Windows kiosks with Intune: Assigned Access requirements, single-app and multi-app kiosk profiles, logon types, Edge kiosk mode types, idle reset and maintenance windows."
sources:
  - "https://learn.microsoft.com/en-us/windows/configuration/assigned-access/"
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/kiosk-settings-windows"
  - "https://learn.microsoft.com/en-us/deployedge/microsoft-edge-configure-kiosk-mode"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# windows-kiosk-and-assigned-access

Assigned Access is the Windows feature behind kiosks and restricted user experiences. Intune configures it with the
**Kiosk** profile (Assigned Access CSP) in Devices > Configuration.

## Requirements (Assigned Access overview)
- Editions: Pro, Enterprise / Enterprise LTSC, Education, IoT Enterprise / IoT Enterprise LTSC.
- UAC must be enabled for a kiosk experience.
- Sign in from the console; the kiosk experience is not supported over Remote Desktop.

## Modes
| Mode | What the user gets |
|---|---|
| Kiosk (single app) | One UWP app or Microsoft Edge in full screen, above the lock screen. If the app is closed it restarts automatically |
| Restricted user experience (multi-app) | Only a defined list of apps, with a tailored Start menu and taskbar; policy settings and AppLocker rules are enforced |

The Intune kiosk settings page says multi-app kiosk is configured in Intune on Windows 10 with this profile; for Windows 11
it points to a separate "Set up a multi-app kiosk on Windows 11 devices" article.

## Single-app kiosk profile
1. Create a Windows kiosk profile; select **Single app, full-screen kiosk**.
2. **User logon type**: Auto logon (Windows 10 1803 and newer; for public-facing kiosks, uses the AssignedAccess CSP), Local
   user account, or Microsoft Entra user or group.
3. **Application type**: Microsoft Edge browser (Edge 87 and newer), Edge Legacy, Kiosk browser (Store app you add to Intune
   as a client app and assign), or a Store app.
4. Edge settings: Edge Kiosk URL; kiosk mode type **Public Browsing (InPrivate)** or **Digital/Interactive Signage
   (InPrivate)**; **Refresh browser after idle time** 0-1440 minutes.
5. Other Edge settings are configured with the settings catalog (device restrictions profile for Edge 45 and older). Assign the
   kiosk profile to the same devices as the Edge profile.
6. Optional maintenance window for app restarts: start time defaults to midnight; if blank, apps restart at an unscheduled
   time 3 days after an update. Daily recurrence is recommended.

The kiosk profile loads for standard user accounts, not for members of the local admin group.

## Multi-app kiosk (Windows 10 profile)
Settings: target Windows 10 in S mode (Yes allows Store and AUMID apps, excludes Win32), logon type (adds HoloLens visitor),
browser and apps (Store app, Win32 app with executable path and AUMID, inbox app by AUMID), one AutoLaunch app, tile size,
optional alternative Start layout XML, taskbar show or hide (hidden by default), Downloads folder access (off by default)
and the same maintenance window. If an app depends on another, allow both (the page's example is 32-bit and 64-bit iexplore.exe).

## Edge kiosk mode
- Edge 87 or later. Both types run an InPrivate session.
- `--kiosk-idle-timeout-minutes` defaults to 0 (off) for full screen and 5 for public browsing; range 1-1440. It only closes
  the browser; Assigned Access or Shell Launcher is needed to restart Edge after the idle timeout.
- Supported policies include URLAllowlist and URLBlocklist (both types). Open/save dialogs are not locked down automatically;
  use ConfigureKeyboardShortcuts to disable the shortcuts.
- Edge via Assigned Access single app on Windows 10 needs 2004 with KB4601382 or later, or 1909 with KB4601380 or later.

## Gotchas
- Kiosk Browser with Autologon on Windows 10 needs an offline license from the Microsoft Store for Business, because
  Autologon uses a local account with no Entra credentials.
- Files, scripts and shortcuts referenced by the profile must be on the local system.
- Windows 10 reached end of support on October 14, 2025; it is still an allowed version in Intune with no guarantees.

## Verify
The device signs in to the kiosk app, the idle reset clears the session, and Intune shows the profile Succeeded.

## Checked
Date: 2026-11-08. Read in full: "Assigned Access overview" (updated 2026-07-15), "Windows device settings to run as a kiosk in
Intune" (2026-04-14) and the Edge kiosk mode page. Removed as unconfirmed: the kioskUser0 account name, the Windows 11 22H2
multi-app JSON Start layout claim, Shell Launcher as a separate mode, Ctrl+Alt+Del admin exit, remote action and group-removal
maintenance steps, update ring advice, the Event Viewer AssignedAccess log path, black-screen causes, the legal-notice
auto logon cause, Windows Hello and BitLocker PIN conflict, and the "kiosk accounts must not be admins" statement (the
page says only that the profile does not load for local admin group members).
Method: documentation only; no commands were run.
