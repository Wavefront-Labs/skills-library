---
id: computing-software.it-support-helpdesk.desktop-support.services-console-and-service-recovery
name: services-console-and-service-recovery
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-admin-tools, services-msc, windows-services, sc-exe, startup-type, service-recovery-options, service-dependencies, delayed-start, comptia-a-plus]
level: practitioner
status: docs-checked
description: "Manage Windows services: services.msc, sc.exe and PowerShell, startup types incl. delayed start, dependencies, recovery actions, and services that will not start."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/sc-config"
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-service"
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-service"
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/restart-service"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# services-console-and-service-recovery

Goal: start, configure and fix Windows services without breaking
dependencies.

## Look
```powershell
Get-Service -Name spooler, wuauserv, bits | Select Name, Status, StartType
```

## Change
```powershell
Restart-Service spooler -Force
Set-Service -Name bits -StartupType Manual
```
```cmd
sc.exe config wsearch start= delayed-auto      :: a space is required after "start="
```
`sc.exe config` accepts `start=` values boot, system, auto, demand (manual,
the default if omitted), disabled and delayed-auto (starts automatically a
short time after the other auto services). If the space after `start=` is
omitted, the command fails.

## Won't start
- Check the System log for Service Control Manager errors for the service,
  and the service's own logs.
- Dependencies: if a dependency failed to start, start it first (Dependencies
  tab in services.msc).
- Logon failure: the service account's password changed or expired, or lacks
  the "Log on as a service" right.
- Executable missing or corrupt: repair or reinstall the application.
- Disabled by policy (Group Policy or Intune): a local change may revert.

## Gotchas
- Do not disable services on the strength of "tweak" guides; they can break
  updates, printing and search.
- `Restart-Service -Force` also restarts dependent services.

## Verify
The service is Running with the expected start type after a reboot, and no
new Service Control Manager errors appear in the System log.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn sc config, Get-Service, Set-Service and Restart-Service pages, as published October 2026. Confirmed: sc config start= values including delayed-auto and the space requirement, Get-Service and Set-Service -StartupType parameters, Restart-Service -Force. Removed: event IDs 7000-7038, sc failure and recovery-tab details, startup-delay timing, Win32_Service query, sc qc/queryex, trigger-start and tamper-protection notes, which no readable page covers.

Method: documentation only; no commands were run.
