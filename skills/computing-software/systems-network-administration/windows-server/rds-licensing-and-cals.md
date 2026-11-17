---
id: computing-software.systems-network-administration.windows-server.rds-licensing-and-cals
name: rds-licensing-and-cals
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, remote-desktop-services, rds, rds-licensing, rds-cals, per-user-cal, per-device-cal, license-server, grace-period]
level: practitioner
status: docs-checked
description: "Set up RD Licensing: activate a license server, install RDS CALs, per-user vs per-device mode, configure session hosts, grace period and licensing diagnostics."
sources:
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-client-access-license
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-activate-license-server
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/troubleshoot-rds-licensing-guidance
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/cannot-connect-rds-no-license-server
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/set-rdlicenseconfiguration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RD Licensing and CALs

## License server
```powershell
Install-WindowsFeature RDS-Licensing -IncludeManagementTools
Add-RDServer -Server rdlic01 -Role RDS-LICENSING -ConnectionBroker rdcb01
```
Activate in RD Licensing Manager: automatic connection (recommended; outbound TCP 443 to the Microsoft Clearinghouse),
web browser, or telephone. Make sure the license server is in the "Terminal Server License Servers" domain group,
then install CAL packs.

## Mode
- **Per User**: one CAL per user, any number of devices; licensing is not enforced, so you must track usage (RD Licensing
  Manager reports). Per user CALs show as expiring 60 days after issue and are extended at sign-in; 90 days is the
  minimum before a CAL can be reassigned to another user.
- **Per Device**: one CAL per device; a temporary CAL (valid 90 days) is issued at first connection and upgraded to a
  permanent CAL when the license server is activated and CALs are available.
CAL version must be the same as or later than the session host OS (a 2025 session host needs 2025 CALs; later CALs
can serve earlier hosts). The license server must run the same Windows Server version as the CALs or later.

## Configure session hosts
```powershell
Set-RDLicenseConfiguration -LicenseServer rdlic01.corp.example.com -Mode PerUser -ConnectionBroker rdcb01
```
Standalone session hosts: use the Group Policy settings "Use the specified Remote Desktop license servers" and "Set the
Remote Desktop licensing mode" (Per Device or Per User). `Set-RDLicenseConfiguration -Mode` accepts PerDevice, PerUser
and NotConfigured.

## Grace period
There is a 120-day grace period during which no license server is required; afterwards clients need a valid RDS CAL
issued by a license server before they can sign in. Check the days remaining:
```powershell
$obj = Get-WmiObject -Namespace 'Root/CIMV2/TerminalServices' Win32_TerminalServiceSetting
$obj.GetGracePeriodDays()
```

## Diagnose
Open RD Licensing Diagnoser from Server Manager (Tools > Terminal Services > RD Licensing Diagnoser) on the session host:
it reports the licensing mode and license server problems. Track usage with RD Licensing Manager reports.

## Verify
- [ ] Licensing Diagnoser shows no problems; CAL usage report matches entitlement.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed: per device and per user CAL behaviour (not enforced, 60 and 90 day figures, 90 day temporary per device CALs), the 120-day grace period and the GetGracePeriodDays query, CAL and license server version compatibility table, activation methods and the Clearinghouse TCP 443 connection, the Terminal Server License Servers group, Set-RDLicenseConfiguration modes, the two Group Policy setting names, and the RD Licensing Diagnoser path. Removed as unconfirmed: the claim that the grace period starts at the first session host install, the Win32_TSLicenseReport class, lsdiag.msc and the CIM-method form of the grace query. The Add-RDServer RDS-LICENSING role is a documented value.

Method: documentation only; no commands were run.
