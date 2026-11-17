---
id: computing-software.cybersecurity-defensive.endpoint-security.print-spooler-hardening
name: print-spooler-hardening
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [print-spooler-hardening, printnightmare, point-and-print, spooler-service, printer-driver-installation, windows-endpoint-protections]
level: practitioner
status: docs-checked
description: "Harden Windows Print Spooler: disable where not needed, Point and Print restrictions, driver install limits, RPC over named pipes settings and monitoring after PrintNightmare."
sources: ["https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34527", "https://support.microsoft.com/en-us/topic/kb5005010-restricting-installation-of-new-printer-drivers-after-applying-the-july-6-2021-updates-31b91c02-05bc-4ada-a7ea-183b129578a7", "https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-printers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Print spooler hardening

The Print Spooler runs as SYSTEM and accepts remote RPC calls; it has produced many critical bugs
(PrintNightmare CVE-2021-34527, SpoolFool) and is used for authentication coercion (PrinterBug).

## Disable where not needed
Servers that do not print (DCs especially, most application servers):
```
Stop-Service -Name Spooler -Force
Set-Service -Name Spooler -StartupType Disabled
```
GPO: System Services -> Print Spooler -> Disabled. Verify with `Get-Service Spooler`.

## Workstations and print servers (spooler needed)
- `RestrictDriverInstallationToAdministrators` = 1 (`HKLM\Software\Policies\Microsoft\Windows NT\Printers\PointAndPrint`) - per KB5005652, a value of 1 (or no value) requires administrator privileges to install drivers; ensure it is not set to 0.
- Point and Print Restrictions policy: Users can only point and print to approved servers (list), "Show warning and elevation prompt" for new connections and driver updates.
- Package Point and Print - Approved servers.
- **Disallow inbound remote printing** on workstations that are not print servers (see the Printers Policy CSP page for the setting).
- RPC settings: "Configure RPC connection settings" - RPC over TCP, authentication required; "Configure RPC listener settings".
- Patch monthly - print servers are a high-value target.

## Monitoring
- Monitor the PrintService Admin and Operational event logs for driver installs and failures.
- New driver files written under the spooler driver store by non-admin processes.
- Sysmon/EDR: spoolsv.exe spawning unusual children.

## Checked
2026-10-28. Confirmed in KB5005652 and the Printers Policy CSP page: `RestrictDriverInstallationToAdministrators` registry name and behaviour, RPC over TCP default with authentication, `Set-Service -StartupType`. Removed: event IDs 316/808/811, the exact spooler driver path, the August 2021 default date, the policy display name for inbound connections and the Windows 11 22H2 version gate.
Method: documentation only; no commands were run.

## Verify
- [ ] Spooler disabled on all DCs and non-print servers.
- [ ] Policy check: `RestrictDriverInstallationToAdministrators` = 1 fleet-wide.
- [ ] Workstations do not accept client connections.
