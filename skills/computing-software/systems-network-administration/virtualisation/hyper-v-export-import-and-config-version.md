---
id: computing-software.systems-network-administration.virtualisation.hyper-v-export-import-and-config-version
name: hyper-v-export-import-and-config-version
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, export-vm, import-vm, vm-configuration-version, update-vmversion, compare-vm, vm-migration, windows-server]
level: practitioner
status: docs-checked
description: "Move Hyper-V VMs with Export-VM and Import-VM (copy, register, new ID), fix import incompatibilities with Compare-VM, and manage VM configuration versions safely."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/export-and-import-virtual-machines
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/upgrade-virtual-machine-version-in-hyper-v-on-windows-or-windows-server
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/import-vm
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/compare-vm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V export, import and VM configuration versions

**Goal:** move or clone a VM between non-clustered hosts, and keep its config version compatible with every host it must run on.

## Export
```powershell
Export-VM -Name app01 -Path '<EXPORT_DIR>'          # the VM can be running or stopped
```
An export gathers the virtual hard disks, the VM configuration files and any checkpoint files into one unit.

## Import modes
```powershell
$vmcx = Get-ChildItem '<EXPORT_DIR>\app01\Virtual Machines\*.vmcx'
Import-VM -Path $vmcx.FullName                               # register in place, same ID
Import-VM -Path $vmcx.FullName -Copy -GenerateNewId `
  -VirtualMachinePath '<VM_DIR>' -VhdDestinationPath '<VM_DIR>\Disks'   # clone
```
Register in place keeps the VM's ID, so it conflicts if the original still exists on that host; a copy import with `-GenerateNewId` gets a new unique ID and can be imported on the same host.

## Fix incompatibilities before import
```powershell
$report = Compare-VM -Path $vmcx.FullName
$report.Incompatibilities | Format-Table Message, MessageId
$report.Incompatibilities[0].Source | Disconnect-VMNetworkAdapter   # e.g. missing switch
Import-VM -CompatibilityReport $report
```

## Configuration versions
```powershell
Get-VMHostSupportedVersion
Get-VM | Format-Table Name, Version
New-VM -Name legacy01 -Version 9.0 -Generation 2      # an older version for compatibility with older hosts
Update-VMVersion -Name app01                           # one-way, VM must be off
```
- A VM can be imported only if the host supports its configuration version: newer hosts import older versions, not the reverse.
- Do not update the version until every host the VM may run on (including DR targets) supports it; the upgrade guidance is to update only if you will not need to move the VM back to an older host.

## Verify
The imported VM starts, network adapters connect to the intended switches, and `Get-VM` shows a unique `VMId` and expected `Version`.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: Export-VM on started or stopped VMs; Import-VM register in place, restore (-Copy with -VhdDestinationPath and -VirtualMachinePath) and copy (-Copy -GenerateNewId); Import-VM -CompatibilityReport and Compare-VM report with Incompatibilities; Get-VMHostSupportedVersion, New-VM -Version and Update-VMVersion; import only if the host supports the configuration version. Removed as unconfirmed: file extension list, the feature list unlocked by newer versions and the hard no-downgrade statement.

Method: documentation only; no commands were run.
