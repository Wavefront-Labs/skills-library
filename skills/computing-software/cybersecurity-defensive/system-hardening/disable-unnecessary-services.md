---
id: computing-software.cybersecurity-defensive.system-hardening.disable-unnecessary-services
name: disable-unnecessary-services
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [service-hardening, attack-surface, systemd, windows-services, least-functionality, config-management, service-minimisation]
level: practitioner
status: docs-checked
description: "Minimise running services on Linux and Windows: inventory with systemctl and Get-Service, map each to a need, disable or mask the rest, and enforce via config management."
sources: ["https://man7.org/linux/man-pages/man1/systemctl.1.html", "https://learn.microsoft.com/en-us/windows-server/security/windows-services/security-guidelines-for-disabling-system-services-in-windows-server", "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-service"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Disable unnecessary services

**Goal:** every running service on a host has a documented reason; everything else is removed, disabled or masked.

## Linux (systemd)
1. Inventory enabled and running units: `systemctl list-unit-files --type=service --state=enabled`, `systemctl list-units --type=service --state=running`. `--type` takes a comma-separated list of unit types (such as `service` and `socket`); socket and timer units can also activate services, so list them too (`systemctl list-sockets`, `systemctl list-timers`).
2. Map each unit to a role or owner. Anything without one is a removal candidate.
3. Remove the package where possible (use your distribution's package manager). Otherwise `systemctl disable --now <unit>`: `disable` does not stop a running unit unless combined with `--now`.
4. `systemctl mask <unit>` is a stronger form of disable: it prohibits all kinds of activation, including enablement and manual activation.

## Windows Server
1. Inventory: `Get-Service` and filter on `StartType`.
2. Microsoft publishes security guidelines for system services on Windows Server 2016 with Desktop Experience. They list services to disable (for example the Xbox Live services) and say that from Windows Server 2019 those configurations are the OS defaults. The page notes some services exist only with Desktop Experience and not on Server Core.
3. Disable via Security Templates in Group Policy or with PowerShell: `Set-Service -Name <service> -StartupType Disabled` (the `Disabled` value means the service cannot be started by a user or application), then `Stop-Service <service>`.

## Enforce
- Encode the allowed service list per role in your configuration management and alert on drift.
- Re-check after OS upgrades and agent installs.

## Gotchas
- Disable without mask can leave the unit startable by other activation paths; mask when a unit must never run.
- Scope Windows changes by server role and test first; do not copy a guideline written for one OS release to another without reading it.

## Verify
- [ ] Each enabled service is in the role's allow list.
- [ ] Re-run the inventory commands and compare with the allow list.

## Checked
2026-11-01. Confirmed: systemctl `list-unit-files`, `list-units`, `--type`, `--state`, `disable --now`, `mask`, `list-sockets`, `list-timers` (systemctl man page, first 100,000 characters); Windows Server 2016 service guidance (Xbox services, 2019 defaults, Server Core note, Security Templates or PowerShell) and `Set-Service -StartupType Disabled` (Microsoft Learn).
Removed: lists of Linux services to remove, package-manager commands, `Get-WindowsFeature`/`Uninstall-WindowsFeature`, the Group Policy console path, Print Spooler and PrintNightmare advice, and CIS/OpenSCAP/NIST claims (those documents were not read).
Method: documentation only; no commands were run.
