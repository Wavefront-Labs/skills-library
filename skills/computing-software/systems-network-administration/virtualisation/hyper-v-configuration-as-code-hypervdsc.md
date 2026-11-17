---
id: computing-software.systems-network-administration.virtualisation.hyper-v-configuration-as-code-hypervdsc
name: hyper-v-configuration-as-code-hypervdsc
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hypervdsc, dsc, configuration-as-code, hyper-v, powershell]
level: advanced
status: docs-checked
description: "Manage Hyper-V hosts and VMs declaratively with the HyperVDsc PowerShell DSC module: switches, VHDs and VMs, applying configurations and drift checks."
sources:
  - https://github.com/dsccommunity/HyperVDsc
  - https://learn.microsoft.com/en-us/powershell/dsc/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V configuration as code with DSC

**Goal:** host and VM configuration described in code, applied repeatably and checked for drift.

## Module
`HyperVDsc` (DSC Community, published on the PowerShell Gallery). Resources include `VMSwitch`, `VMHost`, `Vhd`,
`VMHyperV`, `VMNetworkAdapter`, `VMDvdDrive`, `VMHardDiskDrive`, `VMScsiController`, `VMProcessor` and
`VhdFileDirectory`.
```powershell
Install-Module HyperVDsc -Scope AllUsers
```

## Example
```powershell
Configuration HvHost {
  Import-DscResource -ModuleName HyperVDsc, PSDesiredStateConfiguration
  Node 'hv01' {
    WindowsFeature HyperV { Name = 'Hyper-V'; Ensure = 'Present' }
    VMSwitch Ext {
      Name = 'vSwitch'; Type = 'External'; NetAdapterName = 'pNIC1','pNIC2'
      EnableEmbeddedTeaming = $true; AllowManagementOS = $true; Ensure = 'Present'
      DependsOn = '[WindowsFeature]HyperV'
    }
    Vhd App01Os {
      Name = 'app01-os'; Path = '<DRIVE>:\Hyper-V\app01'; Generation = 'Vhdx'
      MaximumSizeBytes = 80GB; Type = 'Dynamic'; Ensure = 'Present'
    }
    VMHyperV App01 {
      Name = 'app01'; VhdPath = '<DRIVE>:\Hyper-V\app01\app01-os.vhdx'; Generation = 2
      SwitchName = 'vSwitch'; StartupMemory = 4GB; ProcessorCount = 2; State = 'Running'
      Ensure = 'Present'; DependsOn = '[Vhd]App01Os','[VMSwitch]Ext'
    }
  }
}
HvHost -OutputPath .\mof
Start-DscConfiguration -Path .\mof -Wait -Verbose
Test-DscConfiguration -ComputerName hv01 -Detailed     # drift report
```
Resource properties used here (`Name`, `Type`, `NetAdapterName`, `EnableEmbeddedTeaming`, `AllowManagementOS`,
`Generation`, `MaximumSizeBytes`, `VhdPath`, `SwitchName`, `StartupMemory`, `ProcessorCount`, `State`, `Ensure`) come
from the module's resource schemas. `VMHyperV` defaults to Generation 1; setting `MinimumMemory` or `MaximumMemory`
enables dynamic memory; `RestartIfNeeded` lets DSC shut down and restart the VM for property changes.

## Delivery options
- Push with `Start-DscConfiguration` from a build server.
- DSC v3 (`dsc` CLI) does not depend on PowerShell but can use existing PowerShell DSC resources through its
  PowerShell and Windows PowerShell adapter resources.

## Gotchas
- Some properties cannot change on a running VM: use `RestartIfNeeded` deliberately.
- Clustered VMs: let the cluster own placement; avoid configurations that pin VMs to one node.

## Verify
`Test-DscConfiguration -Detailed` reports whether the node is in the desired state; manually changing a switch
setting shows up as drift.

## Checked

Date checked: 2026-10-27. Documentation: HyperVDsc repository (resource schemas and README, main branch), PowerShell DSC 3.0 overview and Test-DscConfiguration reference (PowerShell-Docs-DSC repository).
Confirmed: resource names and the properties and defaults used in the example (DSC_VMSwitch, DSC_Vhd and DSC_VMHyperV schemas); PowerShell Gallery publication; Test-DscConfiguration -ComputerName and -Detailed; DSC v3 PowerShell adapter resources.

Method: documentation only; no commands were run.
