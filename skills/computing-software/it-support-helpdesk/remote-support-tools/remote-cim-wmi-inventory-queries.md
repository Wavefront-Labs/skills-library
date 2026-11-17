---
id: computing-software.it-support-helpdesk.remote-support-tools.remote-cim-wmi-inventory-queries
name: remote-cim-wmi-inventory-queries
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, cim-wmi-queries, get-ciminstance, wmi, cim-session, remote-inventory, powershell-remoting]
level: practitioner
status: draft
description: "Query hardware and OS facts remotely with CIM/WMI: Get-CimInstance classes support uses, CIM sessions over WinRM or DCOM, multi-machine output, and WMI repository errors."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance"
  - "https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/new-cimsessionoption"
  - "https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/computer-system-hardware-classes"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# remote-cim-wmi-inventory-queries

Before visiting a desk, answer "what model, how much RAM, disk free, when did it last
boot, what serial?" remotely. CIM cmdlets (`Get-CimInstance`) replace the old
`Get-WmiObject` (gone in PowerShell 7).

## Classes support uses
| Need | Class | Properties |
|---|---|---|
| Model, maker, RAM, logged-on user | `Win32_ComputerSystem` | Manufacturer, Model, TotalPhysicalMemory, UserName |
| Serial, BIOS version | `Win32_BIOS` | SerialNumber, SMBIOSBIOSVersion, ReleaseDate |
| OS build, last boot, free RAM | `Win32_OperatingSystem` | Caption, BuildNumber, LastBootUpTime, FreePhysicalMemory |
| Disks | `Win32_LogicalDisk` (DriveType=3) | DeviceID, Size, FreeSpace |
| Physical disks / SSD health | `MSFT_PhysicalDisk` (ns `root/Microsoft/Windows/Storage`) | MediaType, HealthStatus |
| Battery | `Win32_Battery`; `BatteryFullChargedCapacity` (ns `root/wmi`) | EstimatedChargeRemaining |
| Monitors | `WmiMonitorID` (ns `root/wmi`) | UserFriendlyName (byte array) |
| Installed updates | `Win32_QuickFixEngineering` | HotFixID, InstalledOn |
| Services | `Win32_Service` | Name, State, StartMode, StartName |

## One machine
```powershell
Get-CimInstance Win32_OperatingSystem -ComputerName PC123 |
  Select-Object CSName, Caption, BuildNumber, LastBootUpTime
Get-CimInstance Win32_LogicalDisk -ComputerName PC123 -Filter "DriveType=3" |
  Select-Object DeviceID, @{n='FreeGB';e={[math]::Round($_.FreeSpace/1GB,1)}}
```

## Many machines, one connection each
```powershell
$s = New-CimSession -ComputerName (Get-Content .\pcs.txt) -ErrorAction SilentlyContinue
Get-CimInstance Win32_ComputerSystem -CimSession $s |
  Select-Object PSComputerName, Model, UserName | Export-Csv .\inventory.csv -NoTypeInformation
$s | Remove-CimSession
```
CIM sessions use WinRM by default. For machines without WinRM, use DCOM:
`New-CimSession -ComputerName PC123 -SessionOption (New-CimSessionOption -Protocol Dcom)`
(needs RPC 135 + dynamic ports through the firewall).

## Errors
- "WinRM cannot complete the operation": WinRM off; use DCOM option or enable WinRM.
- "Access denied": need local admin (or WMI namespace permissions).
- "Invalid class" / "Provider load failure" on one machine: WMI repository problem.
  Check `winmgmt /verifyrepository`; if inconsistent, `winmgmt /salvagerepository`.
  Don't delete the repository folder as a first step.

## Gotchas
- `Win32_Product` triggers MSI consistency checks/repairs on every package: never use it
  for software inventory; read the Uninstall registry keys instead.
- `UserName` is empty for RDP users and over some sessions; use `quser /server:PC123`.

## Verify
The query returns expected values matching what the user sees (Settings > About), and the
multi-machine export lists every reachable host with failures captured separately.
