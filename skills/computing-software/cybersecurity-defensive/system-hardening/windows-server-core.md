---
id: computing-software.cybersecurity-defensive.system-hardening.windows-server-core
name: windows-server-core
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [server-core, windows-server, attack-surface-reduction, windows-admin-center, sconfig, windows-hardening]
level: practitioner
status: docs-checked
description: "Use Windows Server Core to cut attack surface and patching: role suitability, sconfig and PowerShell setup, remote management with Windows Admin Center, and app checks."
sources: ["https://learn.microsoft.com/en-us/windows-server/administration/server-core/what-is-server-core", "https://learn.microsoft.com/en-us/windows-server/administration/server-core/server-core-sconfig", "https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Server Core minimisation

Server Core is the installation option without the desktop shell, Explorer, browser and most GUI components.
Fewer components means a smaller attack surface and no local browsing by admins; see the Microsoft Server Core overview for the documented benefits.

## Role suitability
Check the supported roles list in the Server Core overview and vendor support for third-party apps and agents; some installers need the GUI.

## Initial configuration
- `sconfig` starts automatically at logon on Windows Server 2022 and later; use it for basic configuration (see the SConfig article for the menu).

## Manage remotely, not locally
- Windows Admin Center (browser-based gateway), RSAT/MMC from a privileged access workstation, PowerShell
  remoting (WinRM, restricted to admin subnets), Server Manager from another server.
- Disable RDP where not required, or limit it to jump hosts and enable NLA.
- Remote management tools concentrate risk: harden the Windows Admin Center gateway (HTTPS, restricted
  access, MFA via the identity provider).

## Hardening on top
Same baselines apply (Microsoft security baseline, CIS Server Core profile where available, STIG), plus remove
unused roles and features, Defender and EDR agents, and application control.

## Gotchas
- Some troubleshooting needs remote tools prepared in advance (event viewer remote access, firewall rules for
  remote MMC).
- Do not install a browser on the server; that removes much of the benefit.

## Verify
The host is fully manageable from
Windows Admin Center or remoting; local logon is limited to break-glass use.

## Checked

2026-10-28. Confirmed against: Microsoft Learn What is Server Core, SConfig article (automatic start from Windows Server 2022), Windows Admin Center overview.

Removed as unconfirmed: role suitability list, App Compatibility FOD detail, PowerShell setup cmdlets, Core/Desktop conversion claim, Microsoft default-recommendation claim, Get-ComputerInfo verify.

Method: documentation only; no commands were run.
