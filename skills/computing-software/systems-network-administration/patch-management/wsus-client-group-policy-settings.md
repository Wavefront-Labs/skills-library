---
id: computing-software.systems-network-administration.patch-management.wsus-client-group-policy-settings
name: wsus-client-group-policy-settings
category: computing-software
field: systems-network-administration
product: patch-management
tags: [wsus-gpo, client-side-targeting, wsus-approval, windows-update-management, group-policy, wsus]
level: practitioner
status: docs-checked
description: "Point Windows clients and servers at WSUS correctly with Group Policy: intranet service location, client-side targeting groups, automatic update options, dual scan, and verifying."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-server-update-services/deploy/4-configure-group-policy-settings-for-automatic-updates
  - https://learn.microsoft.com/en-us/windows/deployment/update/waas-wu-settings
  - https://learn.microsoft.com/en-us/windows/deployment/update/wufb-wsus
  - https://learn.microsoft.com/en-us/windows/deployment/update/windows-update-error-reference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WSUS client Group Policy settings

Path: Computer Configuration → Policies → Administrative Templates → Windows Components →
Windows Update (newer ADMX: "Manage updates offered from Windows Server Update Service").

## Core settings
| Policy | Value |
|---|---|
| Specify intranet Microsoft update service location | `https://wsus01:8531` style URL for the update service and the statistics server (WSUS uses ports 8530 and 8531 by default; HTTPS needs TLS configured on the WSUS IIS site) |
| Enable client-side targeting | target group name e.g. `Servers-Ring2` (must match WSUS computer group; WSUS Options → Computers → "Use Group Policy or registry settings") |
| Configure Automatic Updates | 3 = download and notify (servers with orchestrated install) or 4 = auto download and schedule (desktops) |
| Do not connect to any Windows Update Internet locations | Enabled (stops the periodic connection to the public Windows Update service even when an intranet service is set) |
| Specify source service for specific classes of Windows Updates (Windows 10 version 2004 and later, Windows 11) | WSUS for each class you want from WSUS (feature, quality, driver/firmware, other products); located under Manage updates offered from Windows Server Update Service |
| Automatic Updates detection frequency | hours between checks; default 22 h when not configured, and the actual wait is a random value close to (up to 20% below) the configured hours; needs the intranet service location policy enabled |
| No auto-restart with logged on users | Enabled for servers |

One GPO per ring/target group, linked to OUs or filtered by security group.

## Registry view (for troubleshooting)
`HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate` → `WUServer`, `WUStatusServer`;
`...\WindowsUpdate\AU` → `UseWUServer=1`, `AUOptions` (1 disabled, 2 notify download and install, 3 auto download and notify install, 4 auto download and scheduled install, 5 local admin chooses). Microsoft recommends Group Policy or CSP over editing the registry.

## Dual scan trap
On Windows 10, a WSUS server plus deferral policies sends scans to Windows Update unless the scan source policy is set or dual scan is disabled; with a WSUS server and the scan source policy, updates come from the source chosen in that policy. Dual scan is no longer supported on Windows 11, and on Windows 10 configuring both the dual-scan opt-out and the scan source policy leaves the device without Windows Update updates. Set the scan source policy and avoid the older opt-out.

## Verify on a client
```powershell
gpresult /h gp.html
Get-ItemProperty HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate
(New-Object -ComObject Microsoft.Update.ServiceManager).Services | Select Name, IsDefaultAUService
# then trigger a scan (Settings > Windows Update > Check for updates) and check the computer appears in WSUS under the right group
```
WSUS console: computer reports in the expected group with a recent "Last Status Report".

## Gotchas
- HTTPS (8531) needs the WSUS certificate trusted by clients. Update error codes in the log are documented in the Windows Update error reference (for example 0x8024402C: proxy or target server name cannot be resolved; 0x80244022: HTTP 503, service unavailable).
- Cloned machines can show up as one computer in WSUS; check the Microsoft troubleshooting guidance for duplicate client IDs before resetting client identity.

## Verify
Every machine appears once in the correct target group and reports within 24 h.

## Checked

Checked 2026-10-27 against Microsoft Learn: WSUS Group Policy settings for Automatic Updates, Manage additional Windows Update settings, Windows Update for Business with WSUS (scan source policy), the WSUS configure page and the Windows Update error reference.
- Policy names, `UseWUServer`, `AUOptions` values 1-5, `WUServer`, `WUStatusServer`: confirmed. Default ports 8530 and 8531: confirmed.
- Scan source policy name, location and applicability (Windows 10 2004 and later, Windows 11) and the dual-scan statements: confirmed; the previous "older builds" wording is replaced with the documented behaviour.
- Detection frequency default 22 hours and the randomised wait: confirmed (the earlier "8-22 h" range could not be confirmed and was removed).
- Removed unconfirmed: TargetGroup registry values, `UsoClient StartScan` (not documented by Microsoft), the SusClientId reset procedure, 0x80072f8f.
Method: documentation only; no commands were run.
