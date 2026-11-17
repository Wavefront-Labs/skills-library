---
id: computing-software.it-support-helpdesk.intune-mdm.intune-management-extension-logs
name: intune-management-extension-logs
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, ime-logs, intune-management-extension, agentexecutor, appworkload, healthscripts, cmtrace, win32-app, intune]
level: practitioner
status: docs-checked
description: "Read Intune Management Extension logs: which file covers apps, scripts and remediations, CMTrace, forcing an IME check-in, why IME may not install, and antimalware exclusions."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/apps/intune-management-extension
  - https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-troubleshoot
  - https://learn.microsoft.com/en-us/mem/configmgr/core/support/cmtrace
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# intune-management-extension-logs

The Intune Management Extension (IME) is an installer agent that supplements Windows MDM. It
installs automatically once its prerequisites are met and one of these is assigned: PowerShell
scripts, remediations, custom compliance discovery scripts, Win32 apps, Endpoint analytics,
Remote Help, Managed Installers, or the BIOS update configuration policy. It does not support
Windows Home or S mode.

## Location
`%ProgramData%\Microsoft\IntuneManagementExtension\Logs`. View with CMTrace.exe.
| File | Microsoft's description |
|---|---|
| `IntuneManagementExtension.log` | Main log: IME check-ins, policy requests, policy processing, reporting |
| `_IntuneManagementExtension.log` | Saved copy after the log rolls over |
| `AppWorkload.log` | Main app workload log: app check-ins, installs, applicability, detection |
| `AppActionProcessor.log` | Detection and applicability checks for assigned apps |
| `AgentExecutor.log` | PowerShell script execution |
| `HealthScripts.log` | Remediation script execution, including custom compliance scripts, managed installer, hardware configuration and on-demand remediations |
| `ClientHealth.log` | Health of the IME |
| `ClientCertCheck.log` | Device client certificate checks |
| `DeviceHealthMonitoring.log` | Hardware readiness, device inventory and other data collectors |
| `NotificationInfra.log` | Notifications over the real-time communication channel |
| `Sensor.log` | Endpoint analytics data collector |
| `Win32AppInventory.log` | App inventory collector |

## Other sources of detail
- For a failing Win32 app, the Installation details pane has a **Collect logs** option, and the Troubleshoot + support pane shows when the app was created, targeted and delivered.
- Win32 apps targeted to a user that need admin rights the standard user lacks fail to install.

## Force a check-in
- The IME checks for assignments every 8 hours, independent of the MDM check-in. After the ESP or Autopilot device preparation finishes it checks immediately.
- Company Portal > Settings > Sync starts an MDM check-in and an IME check-in. The Sync action from the Intune admin center also does both; progress shows on the Device sync status tab.
- Or restart the IntuneManagementExtension service in Task Manager > Services; it checks in immediately.

## IME will not install or download
Microsoft lists: device not joined to Entra ID, nothing assigned that needs the IME, no connectivity (including to WNS), S mode, a corrupted or edited `Microsoft.Management.Services.IntuneWindowsAgent.exe.config`, installing the agent by a non-supported method, or a user-level-only proxy with no user signed in. To check automatic enrollment, create the Advanced Diagnostic Report (Settings > Accounts > Access work or school > Info) and look for `MDMDeviceWithAAD` in the MDMDiagReport. The IME is removed when it has been in an irrecoverable state for over 24 hours of device-awake time.

## Antimalware exclusions
Microsoft says to exclude from scanning `%ProgramFiles(x86)%\Microsoft Intune Management Extension\Content` and `%windir%\IMECache` on x64 clients (the `Program Files` path without (x86) on x86 clients).

## Checked
Date: 2026-11-08. Read in full: "Intune Management Extension for Windows" (updated 2026-09-24) and "Troubleshoot Win32 App Issues" (updated 2026-04-14). The CMTrace page is cited only as the viewer. Removed as unconfirmed: the sequence of an app trace, searching by portal GUID, OneTrace, the Policies\Results output folder, Restart-Service, retry behaviour for failed apps and scripts, the Win32Apps registry keys, local time versus UTC timestamps, and the claim that IME logs the Store app flow. The MDM event log sentence was removed with it.
Method: documentation only; no commands were run.
