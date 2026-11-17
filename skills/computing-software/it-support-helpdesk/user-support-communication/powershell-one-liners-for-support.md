---
id: computing-software.it-support-helpdesk.user-support-communication.powershell-one-liners-for-support
name: powershell-one-liners-for-support
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, scripting, powershell, powershell-for-support, ps1, execution-policy, get-help, pipeline, comptia-a-plus, support-automation]
level: intro
status: draft
description: "PowerShell for helpdesk work: discovering commands, the pipeline and Select/Where, a kit of support one-liners, execution policy, running .ps1 safely, and logging."
sources:
  - "https://learn.microsoft.com/en-us/powershell/scripting/overview"
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# powershell-one-liners-for-support

Goal: answer common support questions in one line instead of five GUI
windows (A+ 220-1202 4.8: .ps1 use cases).

## Discover
```powershell
Get-Command *printer*            # find cmdlets
Get-Help Get-Printer -Examples   # usage examples (Update-Help once)
Get-Printer | Get-Member         # what properties an object has
```
Pipeline pattern: **get → filter (Where-Object) → shape (Select-Object) →
output (Format-Table / Export-Csv)**.

## Support kit
```powershell
# uptime / last boot
(Get-CimInstance Win32_OperatingSystem).LastBootUpTime
# free space
Get-Volume | Where DriveLetter | Select DriveLetter, @{n='FreeGB';e={[math]::Round($_.SizeRemaining/1GB,1)}}
# installed app version
Get-CimInstance Win32_InstalledWin32Program | Where Name -like '*Zoom*' | Select Name, Version
# top memory processes
Get-Process | Sort WS -Descending | Select -First 10 Name, @{n='MB';e={[int]($_.WS/1MB)}}
# who is signed in
(Get-CimInstance Win32_ComputerSystem).UserName
# connectivity to a service
Test-NetConnection outlook.office365.com -Port 443
# recent errors
Get-WinEvent -FilterHashtable @{LogName='System';Level=2;StartTime=(Get-Date).AddHours(-24)} | Select -First 20 TimeCreated, Id, ProviderName
# serial number for warranty lookup
(Get-CimInstance Win32_BIOS).SerialNumber
# export a report
Get-Printer | Select Name, DriverName, PortName | Export-Csv "$env:TEMP\printers.csv" -NoTypeInformation
```

## Running scripts
- Execution policy (`Get-ExecutionPolicy -List`) is a safety guard, not a
  security boundary; managed devices usually **AllSigned/RemoteSigned** via
  policy. Don't set `Unrestricted` machine-wide; for a one-off:
  `powershell.exe -ExecutionPolicy Bypass -File .\fix.ps1` (only for
  trusted, reviewed scripts).
- Log with `Start-Transcript -Path "$env:TEMP\fix.log"`.
- Use `-WhatIf` on cmdlets that support it before destructive actions.
- PowerShell 5.1 (built-in) vs 7 (pwsh) — scripts for the fleet should
  target 5.1 unless 7 is deployed.

## Gotchas
- Aliases (`gci`, `%`, `?`) are fine interactively, write full names in
  scripts.
- Avoid `Win32_Product` — triggers MSI repairs.
- Running elevated changes context (HKCU, mapped drives).

## Verify
The one-liner returns the expected data on a test machine; scripts produce a
transcript and correct exit code.
