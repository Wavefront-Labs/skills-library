---
id: computing-software.systems-network-administration.powershell.get-ciminstance-queries
name: get-ciminstance-queries
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, cim, cimcmdlets, wmi-cmdlets, get-ciminstance, wql, get-cimclass, get-wmiobject-migration, inventory]
level: practitioner
status: verified
description: "Query Windows inventory with Get-CimInstance: WQL filters, -Property for speed, namespaces, associations, discovering classes, and migrating from Get-WmiObject."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-ciminstance
  - https://learn.microsoft.com/en-us/windows/win32/wmisdk/wql-sql-for-wmi
  - https://learn.microsoft.com/en-us/powershell/module/cimcmdlets/get-cimassociatedinstance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Get-CimInstance queries and filters

`Get-WmiObject` (DCOM) is not part of PowerShell 7 itself, but on Windows 7.6.7 still resolved it as a proxy function
from `Microsoft.PowerShell.Management` through the Windows PowerShell compatibility layer (it ran, returning deserialised
objects without methods; the same is true of `Get-EventLog`), so old scripts can appear to work. It does not exist on
Linux/macOS. Use CimCmdlets: they use WSMan by default for `-ComputerName` (the WinRM service that remoting uses; a
`-ComputerName localhost` call failed with a WS-Management error here because WinRM was not listening) and return
objects with real `[datetime]` values instead of DMTF strings.

## Filter at the source
```powershell
Get-CimInstance Win32_Service -Filter "StartMode='Auto' AND State<>'Running'" -Property Name, State, ExitCode
Get-CimInstance -Query "SELECT Name, ProcessId FROM Win32_Process WHERE Name LIKE 'w3wp%'"
Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' -ComputerName srv1, srv2
```
- `-Filter` is a WQL `WHERE` clause: strings in single quotes, `LIKE` with `%` and `_`, escape
  backslashes by doubling them (`"Name='<DRIVE>:\\Temp'"`).
- A WQL filter is evaluated by the provider, so only matches are returned (locally `Win32_Process` took 69 ms with `-Filter`
  against 93 ms with `Where-Object`; the saving should be larger for big classes and remote calls, not measured here).
- `-Property` limits returned properties (and work on the provider); unrequested ones are `$null`.
- Avoid `Win32_Product`: Microsoft's legacy WMI docs say enumerating it makes the MSI provider initiate a consistency
  check of installed packages, verifying and repairing the install (not run here). Read the Uninstall registry keys instead.

## Classes worth knowing
| Class | Gives |
|---|---|
| `Win32_OperatingSystem` | version, build, LastBootUpTime, free memory |
| `Win32_ComputerSystem` | model, domain, logged-on user, total RAM |
| `Win32_BIOS` | serial number |
| `Win32_QuickFixEngineering` | installed updates (only those from Component Based Servicing; MSI and Windows Update-site updates are not returned) |
| `Win32_Service` | services incl. `StartName` (service accounts) and `PathName` |
| `Win32_Volume`, `MSFT_Disk` (`root/Microsoft/Windows/Storage`) | storage |
| `MSFT_NetAdapter` (`root/StandardCimv2`) | modern network config |
| `Win32_ShadowCopy` | VSS snapshots |

## Namespaces and discovery
```powershell
Get-CimClass -Namespace root/cimv2 -ClassName *disk* | Select-Object CimClassName
(Get-CimClass Win32_Service).CimClassMethods        # methods and parameters
(Get-CimClass Win32_Service).CimClassProperties | Select-Object Name, CimType
Get-CimInstance -Namespace root -ClassName __NAMESPACE | Select-Object Name
Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct   # present on this Windows 11 client
```

## Associations
```powershell
$disk = Get-CimInstance Win32_DiskDrive -Filter "Index=0"
Get-CimAssociatedInstance -InputObject $disk -ResultClassName Win32_DiskPartition
```

## Migrating from Get-WmiObject
| Old | New |
|---|---|
| `Get-WmiObject -Class X -Filter ...` | `Get-CimInstance -ClassName X -Filter ...` |
| `$o.ConvertToDateTime($o.LastBootUpTime)` | already `[datetime]` |
| `$o.Method()` | `Invoke-CimMethod -InputObject $o -MethodName Method` |
| `-Credential` per call | `New-CimSession -Credential` then `-CimSession` (`Get-CimInstance` has no `-Credential` parameter) |
| DCOM to old hosts | `New-CimSessionOption -Protocol Dcom` (a DCOM session to this machine ran) |

## Verify
- [ ] Query returns the same rows as the GUI tool (services.msc, Disk Management).
- [ ] Remote queries use `-Filter` rather than client-side `Where-Object` on large classes.

## Checked
Ran on PowerShell 7.6.7 and Windows PowerShell 5.1.26100 (local machine): the Auto-service filter with `-Property`
(unrequested `StartMode` came back empty), LIKE query, `DriveType=3`, `Name='C:'`, the doubled-backslash rule
(`Win32_Directory -Filter "Name='C:" + two backslashes + "Windows'"` returned the folder; a single backslash gave
`Invalid query`), `[datetime]` LastBootUpTime, `Get-CimClass` listings (methods, properties), `root` namespace list,
`SecurityCenter2`, `Get-CimAssociatedInstance`, `MSFT_NetAdapter`, `MSFT_Disk`, `Win32_ShadowCopy`, the other class names,
DCOM session, parameter lists, and `Get-WmiObject` resolution in 7.6.7 (plus the fact that instance objects have no
`StopService()` method). Win32_QuickFixEngineering (CBS-only) and Win32_Product (consistency check) statements were read
on Microsoft Learn; remote queries and `Win32_Product` itself were not run.
