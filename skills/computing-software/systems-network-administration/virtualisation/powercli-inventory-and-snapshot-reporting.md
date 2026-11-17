---
id: computing-software.systems-network-administration.virtualisation.powercli-inventory-and-snapshot-reporting
name: powercli-inventory-and-snapshot-reporting
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [powercli, powercli-reporting, get-vm, get-view, inventory-report, snapshot-report, rvtools, vmware, vsphere, powershell]
level: practitioner
status: draft
description: "Build fast vSphere inventory reports in PowerCLI: Get-VM vs Get-View performance, calculated properties, snapshot/tools/hardware reports, CSV/Excel export and scheduling."
sources:
  - https://developer.broadcom.com/powercli
  - https://developer.broadcom.com/xapis/vsphere-web-services-api/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PowerCLI inventory and snapshot reporting

**Goal:** answer "what do we have and what is wrong with it" across thousands of VMs in
seconds, on a schedule.

## Connect safely
```powershell
Install-Module VCF.PowerCLI -Scope CurrentUser     # module name in current releases; older: VMware.PowerCLI
Set-PowerCLIConfiguration -InvalidCertificateAction Fail -Scope User   # trust your CA instead of ignoring
$cred = Get-Secret vcenter-ro                      # SecretManagement vault, read-only account
Connect-VIServer vc01.<domain> -Credential $cred
```

## Get-VM vs Get-View
`Get-VM` builds rich objects (slow at scale, several API calls per VM). `Get-View` returns
raw managed objects; with `-Property` it fetches only what you ask for and is 10-50x faster.
```powershell
Get-View -ViewType VirtualMachine -Property Name, Config.Hardware, Guest.ToolsVersionStatus2,
  Runtime.PowerState, Summary.Storage.Committed, Snapshot |
 Select Name,
  @{n='vCPU';e={$_.Config.Hardware.NumCPU}},
  @{n='MemGB';e={$_.Config.Hardware.MemoryMB/1024}},
  @{n='Tools';e={$_.Guest.ToolsVersionStatus2}},
  @{n='Power';e={$_.Runtime.PowerState}},
  @{n='UsedGB';e={[math]::Round($_.Summary.Storage.Committed/1GB,1)}},
  @{n='HasSnap';e={[bool]$_.Snapshot}} |
 Export-Csv vm-inventory.csv -NoTypeInformation
```

## Typical reports
```powershell
# Snapshots older than 3 days with size
Get-VM | Get-Snapshot | Where Created -lt (Get-Date).AddDays(-3) | Select VM,Name,Created,SizeGB
# VMs with mounted ISOs, limits, or outdated hardware
Get-VM | Get-CDDrive | Where IsoPath | Select Parent, IsoPath
Get-VM | Get-VMResourceConfiguration | Where {$_.MemLimitMB -ne -1 -or $_.CpuLimitMhz -ne -1}
# Datastore usage
Get-Datastore | Select Name, @{n='FreePct';e={[math]::Round($_.FreeSpaceGB/$_.CapacityGB*100,1)}} | Sort FreePct
```
`ImportExcel` module's `Export-Excel` gives formatted multi-sheet workbooks. RVTools is
the off-the-shelf alternative for ad-hoc full exports.

## Scheduling
Run from a management server with Task Scheduler or a CI runner, read-only service
account, credentials from a vault, email or post results; keep scripts in Git.

## Verify
Report row count equals `(Get-View -ViewType VirtualMachine -Property Name).Count`;
spot-check three VMs against the client.
