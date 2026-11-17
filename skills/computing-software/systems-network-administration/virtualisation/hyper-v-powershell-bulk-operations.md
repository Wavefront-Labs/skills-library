---
id: computing-software.systems-network-administration.virtualisation.hyper-v-powershell-bulk-operations
name: hyper-v-powershell-bulk-operations
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, hyper-v-module, get-vm-hyperv, powershell, powershell-direct, bulk-operations, cluster-wide-report, windows-server]
level: practitioner
status: docs-checked
description: "Manage many Hyper-V VMs at once with the Hyper-V PowerShell module: cluster-wide inventory, filtered bulk changes, remoting with CIM sessions and PowerShell Direct."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/powershell-direct
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/copy-vmfile
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bulk VM operations with the Hyper-V module

**Goal:** inventory and change hundreds of VMs reliably instead of clicking through Hyper-V Manager.

## Cluster-wide inventory
```powershell
$nodes = (Get-ClusterNode -Cluster hvclu01).Name
Get-VM -ComputerName $nodes |
  Select-Object ComputerName, Name, State, ProcessorCount,
    @{n='MemGB';e={[math]::Round($_.MemoryAssigned/1GB,1)}}, Version, Generation, Uptime |
  Export-Csv vm-inventory.csv -NoTypeInformation
```
Property names come from the object `Get-VM` returns; list them with `Get-VM | Get-Member` on your Windows Server
version before relying on them in a report.

## Safe bulk changes
```powershell
Get-VM -ComputerName $nodes | Where-Object Name -like 'web*' |
  Set-VM -AutomaticStartAction Start -AutomaticStartDelay 60 -WhatIf      # drop -WhatIf when happy
Get-VM -ComputerName $nodes | Get-VMIntegrationService -Name 'Guest Service Interface' |
  Where-Object { -not $_.Enabled } | Enable-VMIntegrationService
```
Always preview with `-WhatIf` and filter explicitly; `Get-VM | Stop-VM` with no filter stops everything.

## Remoting
Hyper-V cmdlets accept `-ComputerName` and `-CimSession`; reuse sessions for speed:
```powershell
$s = New-CimSession -ComputerName $nodes
Get-VM -CimSession $s | Measure-Object
```

## PowerShell Direct (no guest network needed)
From a Hyper-V host running Windows 10 or Windows Server 2016 or later, into a guest running Windows 10 or Windows
Server 2016 or later:
```powershell
Invoke-Command -VMName app01 -Credential $cred -ScriptBlock { Get-Service W32Time }
Copy-VMFile -Name app01 -SourcePath .\fix.ps1 -DestinationPath <GUEST_TEMP>\fix.ps1 -FileSource Host -CreateFullPath
```
`Copy-VMFile` needs the Guest Service Interface integration service enabled in the guest.

## Gotchas
- Clustered VMs: change high-availability settings with the Failover Clustering cmdlets (`Get-ClusterGroup`), not
  just the Hyper-V cmdlets.
- Managing a remote host needs membership of the Hyper-V Administrators or Administrators group on that host.

## Verify
Re-run the inventory export after changes and diff it against the previous CSV.

## Checked

Date checked: 2026-10-27. Documentation: Hyper-V PowerShell reference (Windows Server 2025 docset), PowerShell Direct page (windowsserverdocs main branch).
Confirmed: Set-VM -AutomaticStartAction and -AutomaticStartDelay; Copy-VMFile parameters; PowerShell Direct version requirements and Invoke-Command -VMName; Hyper-V Administrators or Administrators membership requirement for remote management. Property names on the VM object are not listed in the cmdlet reference, so the skill tells readers to confirm them with Get-Member.

Method: documentation only; no commands were run.
