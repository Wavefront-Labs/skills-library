---
id: computing-software.systems-network-administration.windows-server.printmanagement-cmdlets
name: printmanagement-cmdlets
category: computing-software
field: systems-network-administration
product: windows-server
tags: [print-server, printmanagement-module, add-printer, printer-drivers, print-services]
level: practitioner
status: gated
description: "Manage print queues with PrintManagement cmdlets: add drivers, ports and printers, set sharing and default settings, manage jobs and script bulk queue creation."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/printmanagement/
  - https://learn.microsoft.com/en-us/powershell/module/printmanagement/add-printer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PrintManagement cmdlets

## Drivers, ports, queues
```powershell
# The driver package must already be available on the server
Add-PrinterDriver -Name 'HP Universal Printing PCL 6' -ComputerName PRINT01
Add-PrinterPort -Name 'IP_10.20.5.31' -PrinterHostAddress 10.20.5.31 -ComputerName PRINT01
Add-Printer -Name 'FIN-2F-MFP01' -DriverName 'HP Universal Printing PCL 6' -PortName 'IP_10.20.5.31' `
  -Shared -ShareName 'FIN-2F-MFP01' -Location 'Finance 2nd floor' -Published -ComputerName PRINT01
```
`-Published` is the Add-Printer parameter for publishing the printer in Active Directory.

## Bulk from CSV
```powershell
Import-Csv queues.csv | ForEach-Object {
  if (-not (Get-PrinterPort -Name "IP_$($_.IP)" -ComputerName PRINT01 -ErrorAction SilentlyContinue)) {
    Add-PrinterPort -Name "IP_$($_.IP)" -PrinterHostAddress $_.IP -ComputerName PRINT01 }
  Add-Printer -Name $_.Name -DriverName $_.Driver -PortName "IP_$($_.IP)" -Shared -ShareName $_.Name -Location $_.Location -ComputerName PRINT01 }
```

## Defaults
```powershell
Set-PrintConfiguration -PrinterName 'FIN-2F-MFP01' -DuplexingMode TwoSidedLongEdge -Color $false -ComputerName PRINT01
```

## Jobs
```powershell
Get-PrintJob -PrinterName 'FIN-2F-MFP01' -ComputerName PRINT01
Get-PrintJob -PrinterName 'FIN-2F-MFP01' -ComputerName PRINT01 | Where-Object JobStatus -match 'Error' | Remove-PrintJob
```
Stuck queue that will not clear: restart the Spooler service and re-check with `Get-PrintJob`.

## Inventory
```powershell
Get-Printer -ComputerName PRINT01 | Select Name,DriverName,PortName,Shared,Location,PrinterStatus | Export-Csv printers.csv -NoTypeInformation
```

## Verify
- [ ] Queues appear in AD search and on clients via GPO deployment; test page prints.

## Checked
2026-10-28. Confirmed on the Learn PrintManagement module index and Add-Printer page: Add-Printer, Add-PrinterDriver, Add-PrinterPort,
Get-PrintJob, Set-PrintConfiguration exist; `-Published` is an Add-Printer parameter. Removed as unconfirmed: the pnputil
step and the spool-folder deletion advice. The remaining parameter names (-PrinterHostAddress, -DuplexingMode, -Color,
Remove-PrintJob usage, Get-Printer properties) were not checked on their cmdlet pages
(gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
