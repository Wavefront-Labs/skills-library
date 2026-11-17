---
id: computing-software.it-support-helpdesk.intune-mdm.enrolment-compliance-and-app-deployment
name: enrolment-compliance-and-app-deployment
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, intune, microsoft-intune, mdm, endpoint-management, windows-autopilot, entra-join, win32-app, intunewin, intunewinapputil, assignment, intune-management-extension, company-portal]
level: practitioner
status: docs-checked
description: "Intune Windows deployment for helpdesk: what Autopilot does, packaging Win32 apps, IME behaviour, assignment types, deadlines, restart grace period and limits."
sources:
  - "https://learn.microsoft.com/en-us/autopilot/overview"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-app-management"
  - "https://github.com/microsoft/Microsoft-Win32-Content-Prep-Tool"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intune: Windows Autopilot and Win32 app deployment

The Intune admin center is reorganised often; blade names are approximate.

## Windows Autopilot in brief
Autopilot sets up and pre-configures new Windows devices from the OEM-optimised Windows already on them, with no custom image. It can join devices to Microsoft Entra ID or Active Directory (Entra hybrid join), auto-enroll them in MDM such as Intune (configuration needs Entra ID P1 or P2), assign them to groups by profile, customise OOBE, change the Windows edition (for example Pro to Enterprise), apply settings and policies, and install apps. The user only connects to a network and verifies credentials. Autopilot Reset prepares an existing device for a new user and is useful in break/fix. Autopilot device preparation is a separate feature with its own article. Details of licensing and networking are on the "Windows Autopilot software, networking, configuration, and licensing requirements" page.

## Win32 app management: prerequisites
- Windows Enterprise, Pro or Education; device enrolled in Intune and Entra registered, joined or hybrid joined.
- App size no more than 30 GB.
- Delivered by the Intune management extension (IME), installed automatically when a PowerShell script or Win32 app is assigned. The IME checks for new Win32 assignments every hour (and on service or device restart).
- Installs must be silent; interactive installs (including serviceui.exe style workarounds) are not supported.
- During Autopilot enrollment, avoid mixing Win32 and line-of-business apps (both may use the Trusted Installer service and fail). Mixing is supported with Autopilot device preparation.

## Package the app
```
IntuneWinAppUtil -c <setup_folder> -s <source_setup_file> -o <output_folder> -q
```
- `-c` folder holds only this app's setup files; `-s` is the setup file (setup.exe or .msi; for MSI the tool reads the details Intune needs); `-o` output folder; `-a` catalog folder (Windows 10 S mode); `-q` quiet mode (overwrites existing output, creates the folder); `-qq` also no console output. `-v` shows the tool version (1.8.2 and later), `-h` usage. Needs .NET Framework 4.7.2.
- The `.intunewin` file contains the compressed, encrypted source files and the decryption information, so store it as safely as the source.
- Instead of an install command line, a PowerShell script (50 KB maximum, same context as the installer, silent, return code sets the result) can serve as the installer. With Multi-Admin Approval on, create the app first and add the script afterwards.
- Win32 apps support detection rules, requirements and dependencies; see "Add, assign, and monitor a Win32 app" for the rule types.

## Assign
Types: Required, Available for enrolled devices, Uninstall. Per assignment: Include or Exclude mode; end-user notifications (all toasts, restart toasts only, hide all); UTC or device time zone; availability (when content downloads, and when the app appears in Company Portal for Available); installation deadline; restart grace period; delivery optimization priority.
- Required: content downloads at the start time and installs at the deadline. Company Portal shows Installing from download until the install completes.
- With multiple assignments the deadline chosen is a specific one over ASAP, and the earlier of two specific ones.
- Restart grace period: defaults to 1,440 minutes (maximum two weeks), countdown dialog 15 minutes before restart, snooze 240 minutes (not above the grace period). It only works when the app's Device restart behavior is "Determine behavior based on return codes" (and the code is a hard reboot) or "Intune will force a mandatory device restart".
- Available apps removed by a user are not reinstalled automatically.
- Apps Intune installed are not uninstalled when the device is unenrolled, so assign only to corporate managed devices where that matters.
- Delivery Optimization (peer-to-peer on by default) downloads Win32 content; it can be set to background or foreground per assignment, and Connected Cache can run on Configuration Manager distribution points.
- Relationship viewer on the app shows dependent and superseded child apps.

## Verify
The device is enrolled and joined as expected, the app shows Installed in Company Portal and Intune, and its detection rule matches reality.

## Checked
Method: documentation only; no commands were run. Checked 2026-11-08 against the Autopilot overview, the Intune Win32 app management page and the Content Prep Tool readme (all read in full). The earlier draft also covered enrolment methods by ownership, compliance and Conditional Access, the settings catalog, remote actions, dsregcmd/mdmdiagnosticstool/log-path troubleshooting, return codes and check-in intervals; none of that is stated on these three pages, so it was removed and the description narrowed (the skill name is kept for stability).
