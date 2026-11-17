---
id: computing-software.it-support-helpdesk.intune-mdm.collect-diagnostics-remote-action
name: collect-diagnostics-remote-action
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, collect-diagnostics, remote-actions, device-diagnostics, mdm-logs, log-collection, intune]
level: practitioner
status: docs-checked
description: "Pull logs from a managed device with Intune's Collect diagnostics action: platforms, roles, tenant switches, what the Windows zip contains, retention, and known issues."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/collect-diagnostics"
  - "https://learn.microsoft.com/en-us/windows/client-management/mdm/diagnosticlog-csp"
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/device-management"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# collect-diagnostics-remote-action

**Collect diagnostics** gathers troubleshooting data from a managed device without
interrupting the user; only nonuser locations and file types are accessed.

## Prerequisites
- Platforms: Windows (corporate-owned), Windows Holographic, and Android and
  iOS/iPadOS via app protection.
- Role: Help Desk Operator, School Administrator, or a custom role with the permission
  Remote tasks/Collect diagnostics plus visibility permissions such as Organization/Read
  and Managed devices/Read.
- The device must be online and able to reach the service; the regional storage URLs on
  the Microsoft page must not be blocked.
- The action is enabled by default; admins can disable it under Tenant administration >
  Device diagnostics (the setting names Windows 10 1909 and later, or Windows 11).
- Diagnostics cannot be collected or downloaded by calling Microsoft Graph directly; use
  the Intune admin center.

## Run it (Windows)
1. Intune admin center > Devices > All devices > pick the device.
2. In the action icons at the top, select **Collect diagnostics**, then **Collect data**.
   A pending notification appears on the Overview page.
3. Check status under Monitor > Device diagnostics.
4. When complete, select ... > Download on that row, then Yes.
- Retention: a collection is stored for 28 days and then deleted; each device can hold up
  to 10 collections.
- Bulk: Collect diagnostics is also a bulk device action for up to 25 Windows devices.
- Autopilot: diagnostics can be captured automatically on a Windows Autopilot failure
  (enabled by default; one set of logs per day per device). Find them via Diagnostics >
  Download in the device's action row.

## What the Windows zip contains
Four kinds of item: registry keys, commands, Event Viewer logs and files. Examples from
the page:
- Commands: `dsregcmd.exe /status`, `ipconfig.exe /all`, `certutil.exe -store`,
  `mdmdiagnosticstool.exe`, `netsh.exe winhttp show proxy`, `netsh.exe advfirewall show
  allprofiles`, `powercfg.exe /batteryreport`.
- Registry: `HKLM\SOFTWARE\Microsoft\IntuneManagementExtension`,
  `HKLM\SOFTWARE\Microsoft\DeviceInventory`, the PolicyManager DeviceHealthMonitoring key.
- Event logs: Application, System, Setup, BitLocker Management, HelloForBusiness
  Operational, AppLocker, Windows Firewall, WinRM, WMI-Activity, AppXDeployment.
- Files: Intune Management Extension logs under ProgramData, the DiagnosticLogCSP
  collector ETLs, Windows Update ETLs, CBS log, Defender `MpSupportFiles.cab`, SetupDiag
  results, WLAN report.
- With KB5011543 (Windows 10) or KB5011563 (Windows 11) the zip is flattened, logs are
  named for what they hold, and multi-file items get a folder.

## Use it well
- Collect as soon as the user reports the fault, before a reboot or fix changes state.
- Diagnostics might include user or device names. Microsoft personnel might access them
  while resolving incidents.
- Handle the zip under your data policy before attaching it to a ticket.

## Gotchas
- Known failure causes: a time-out on devices without KB4601315 or KB4601319 (fix to the
  DiagnosticLog CSP; reboot after install), and a device that could not receive the action
  within a 24-hour window because it was offline or off.
- Windows only for the device-level zip; mobile app diagnostics go through app protection
  (Troubleshooting + support > Troubleshoot > select a user > App protection). App
  protection diagnostics take about 30 minutes to arrive, and uploads over 50 diagnostics
  or 4 MB cannot be downloaded from the portal; contact Intune support.

## Checked
Date: 2026-11-07. Read in full: Intune "Device action: collect diagnostics" (prerequisites, admin center steps, data
collected lists, disable settings, known issues). Removed as unconfirmed: "Entra or hybrid joined" requirement, the
"autopilot auto-collection must be enabled" prerequisite wording (page says both settings are enabled by default), the
Monitor > Device diagnostics > zip folder table (numbered folders, `MDMDiagReport`, battery/systeminfo claims, Get-WindowsUpdateLog), "large logs may
truncate", the iOS/macOS sysdiagnose advice, and the Verify step. Command and registry lists were quoted from the page
sample; the DiagnosticLog CSP and device-actions pages were not needed for any retained claim.
Method: documentation only; no commands were run.
