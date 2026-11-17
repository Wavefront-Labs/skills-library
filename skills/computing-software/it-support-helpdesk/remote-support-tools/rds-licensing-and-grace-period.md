---
id: computing-software.it-support-helpdesk.remote-support-tools.rds-licensing-and-grace-period
name: rds-licensing-and-grace-period
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, rds-licensing, rds-cal, grace-period, license-server, remote-desktop-services, rdp]
level: advanced
status: draft
description: "Fix Remote Desktop Services licensing: the 120-day grace period, licence server and mode settings, per-user vs per-device CALs, and 'no Remote Desktop license servers available'."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-client-access-license"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/licensing-mode-change-rds"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/no-licenses-available-rd-licensing"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# rds-licensing-and-grace-period

Admin RDP to a server (2 concurrent sessions, "administrative mode") needs no CALs. Once
the **Remote Desktop Session Host** role is installed, every user session needs an RDS
CAL, after a 120-day grace period.

## Symptoms
- "The remote session was disconnected because there are no Remote Desktop License Servers
  available to provide a license."
- "The remote session was disconnected because the Remote Desktop client access license
  stored on this computer has been modified."
- Server Manager notice that the grace period ends in N days.
- Event ID 1128/1130 (TerminalServices-RemoteConnectionManager) about licensing.

## Check configuration
- RD Licensing Diagnoser (`lsdiag.msc`) on the session host: shows licensing mode,
  licence server(s) discovered, CALs available, and specific problems.
- Settings via GPO (Computer > Administrative Templates > Windows Components > Remote
  Desktop Services > RD Session Host > Licensing): **Use the specified Remote Desktop
  license servers** and **Set the Remote Desktop licensing mode** (Per User / Per Device).
  Or in a deployment: Server Manager > RDS > Deployment properties > RD Licensing.
- Grace period remaining (PowerShell, elevated):
  ```powershell
  (Invoke-CimMethod -InputObject (Get-CimInstance -Namespace root/cimv2/TerminalServices -ClassName Win32_TerminalServiceSetting) -MethodName GetGracePeriodDays).DaysLeft
  ```

## Licence server
- Install the RD Licensing role, **activate** the server (RD Licensing Manager >
  right-click > Activate), install CAL packs (agreement number for volume licensing).
- Add the licence server to the **Terminal Server License Servers** group in AD (for
  per-user CAL reporting/issuance tracking).
- Per-device CALs are issued permanently-ish (temporary then permanent); per-user CALs
  aren't enforced technically but must be owned (audit).
- Mode mismatch: session host Per Device but only Per User CALs installed = refusals.

## Fixes
1. Point session hosts at the licence server and set the matching mode via GPO;
   `gpupdate /force`; restart the Remote Desktop Services service in a maintenance window.
2. Firewall: session host -> licence server RPC (TCP 135 + dynamic) must be open.
3. Corrupt client per-device licence: on the client, delete
   `HKLM\SOFTWARE\Microsoft\MSLicensing` (run mstsc as admin once to recreate).
4. Grace expired in a lab with no CALs: don't reset grace by deleting the registry
   `GracePeriod` key in production; buy/install CALs.

## Gotchas
- CAL version must be >= the session host OS version (2022 CALs for 2022 hosts).
- Azure Virtual Desktop/Windows 365 multi-session use Microsoft 365 licensing, not RDS CALs.

## Verify
RD Licensing Diagnoser shows no problems and available CALs; users connect without
licensing errors; licence manager shows issued CALs incrementing (per device).
