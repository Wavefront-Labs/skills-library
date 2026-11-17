---
id: computing-software.it-support-helpdesk.intune-mdm.troubleshooting-intune-app-install-failures
name: troubleshooting-intune-app-install-failures
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, app-install-failure, win32-app, intune-management-extension, detection-rules, agentexecutor, company-portal, intune, required-vs-available]
level: practitioner
status: docs-checked
description: "Fix Intune app installs that fail or stay pending: the Troubleshoot pane, IME and AppWorkload logs, targeting and Entra device limit checks, return codes, and install timeout."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-troubleshoot"
  - "https://learn.microsoft.com/en-us/troubleshoot/mem/intune/app-management/troubleshoot-app-install"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-app-management"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-add"
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# troubleshooting-intune-app-install-failures

## Step 1: what does Intune say?
Intune admin center > **Troubleshoot + support** > Select user > pick the device > **Managed Apps** > an app whose
Installation Status shows a failure. The error details name the problem; for a failed Required app you or the help desk can
sync the device and retry. For Win32 apps, the Installation details pane has a **Collect logs** option. For specific
error codes use the "Intune app installation error reference" (not reproduced here).

Self-help: the Microsoft 365 admin center > Help & support > describe the issue, enter the user's email and Run tests; the
"Intune app deployment" diagnostic is read-only (not available in GCC High, DoD or 21Vianet).

## Step 2: app not arriving at the device
- App missing in Company Portal: it must be assigned with **Available** intent and the user must use a device type the app supports.
- Windows BYOD: the user needs to add a Work account to the device.
- Entra device limit: check Microsoft Entra Device Settings > Maximum devices per user, then the user > Devices; delete
  stale records if over the limit.
- iOS/iPadOS ADE: the user must show as Enrolled by User in the device Overview; if NA, deploy a Company Portal config policy.
- Win32 targeting: the IME is installed automatically when a Win32 app or PowerShell script is assigned. The IME checks for
  new Win32 assignments every hour (or on service or device restart).
- A user-targeted Win32 app that needs admin rights fails for a standard user.
- Windows S mode does not support MSI installation.
- Do not mix Win32 and LOB apps during Windows Autopilot enrolment; installs can fail (they can both use the Trusted Installer
  service). Mixing is supported with Autopilot device preparation.

## Step 3: device logs
Folder `%ProgramData%\Microsoft\IntuneManagementExtension\Logs`, readable with CMTrace.
| Log | Use |
|---|---|
| `IntuneManagementExtension.log` | Main client log: check-in, policy request and processing, reporting |
| `AppWorkload.log` | App check-ins, installs, applicability and detection |
| `AppActionProcessor.log` | Detection and applicability checks |
| `AgentExecutor.log` | PowerShell script execution |
| `HealthScripts.log` | Remediation scripts, custom compliance |
| `ClientHealth.log`, `_IntuneManagementExtension.log` | Agent health; rolled-over copy of the main log |

Antimalware should exclude the IME `Content` folder (`%ProgramFiles(x86)%\Microsoft Intune Management Extension\Content` on
x64) and `%windir%\IMECache`.

## Detection, return codes, run time
- To detect a file version with a script rule, `[System.Diagnostics.FileVersionInfo]::GetVersionInfo("<path to binary>").FileVersion`
  and compare; the page shows a script that exits 0 on a match and 1 otherwise.
- Detection rules, file/registry rules: **Associated with a 32-bit app on 64-bit clients** = Yes makes the rule search the
  32-bit registry or expand paths in 32-bit context on a 64-bit client; the default is No (64-bit).
- Return codes: defaults are added at app creation and can be edited. Types are success, soft reboot, hard reboot and retry
  (retry: three attempts, five minutes apart).
- **Installation time required** defaults to 60 minutes, max 1440; exceeding it fails the install.
- `powershell.exe` called in the install or uninstall command launches 32-bit PowerShell; the page gives a command to force 64-bit.
- Installs must be silent; interactive installs and serviceui.exe workarounds are not supported.
- Restart behaviour: "Determine behavior based on return codes" or "force mandatory restart" must be set for the restart grace
  period to apply.
- Deadline: a Required app with a deadline downloads at the start time and installs at the deadline; Company Portal shows
  Installing from download until install.
- Win32 apps are not removed automatically if the device is unenrolled, and Available apps are not reinstalled after being uninstalled.

## Verify
Device install status shows Installed, and the app detection result in `AppWorkload.log` agrees.

## Checked
Date: 2026-11-08. Read in full: Win32 app troubleshooting (updated 2026-04-14), "Troubleshooting Intune app installation
issues" (2026-03-30), Win32 app management (2026-04-14), and the install-time, return-code and 32-bit sections of the
"Add a Win32 app" page. Removed as unconfirmed: the status code table (0x87D1041C, 0x87D1313C and their meanings), the
psexec SYSTEM reproduction, IME retry schedule (hourly, three attempts, then daily), Company Portal Retry steps, the
specific return code list (1707, 3010, 1641, 1618), detection advice for EXE files, and the IMECache cleanup note.
Method: documentation only; no commands were run.
