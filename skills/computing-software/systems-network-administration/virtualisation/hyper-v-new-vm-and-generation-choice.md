---
id: computing-software.systems-network-administration.virtualisation.hyper-v-new-vm-and-generation-choice
name: hyper-v-new-vm-and-generation-choice
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [new-vm-hyperv, hyper-v, vm-generation, powershell]
level: intro
status: docs-checked
description: "Create Hyper-V VMs with New-VM and companion cmdlets, choose Generation 1 or 2 correctly, and set secure boot, CPU, memory, disks and boot order."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/new-vm
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/should-i-create-a-generation-1-or-2-virtual-machine-in-hyper-v
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/dynamic-memory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating VMs with New-VM and choosing generation

**Goal:** VMs created consistently with the right generation, because it cannot be changed later.

## Generation 1 vs 2
| | Gen 1 | Gen 2 |
|---|---|---|
| Firmware | BIOS | UEFI, Secure Boot, vTPM |
| Boot from | IDE disk/DVD, legacy NIC PXE | SCSI disk/DVD, standard (synthetic) NIC PXE |
| OS | Most guest operating systems, including 32-bit | Most 64-bit Windows versions and current Linux and FreeBSD |
| Boot disk | VHD (up to 2040 GB) or VHDX (up to 2 TB) | VHDX (up to 64 TB) |
A generation cannot be changed after the VM is created. Microsoft recommends generation 2 unless the OS or a prebuilt VHD is not UEFI-compatible.

## Create
```powershell
$root = '<DRIVE>:\Hyper-V'
New-VM -Name app01 -Generation 2 -MemoryStartupBytes 4GB -Path $root `
  -NewVHDPath "$root\app01\app01-os.vhdx" -NewVHDSizeBytes 80GB -SwitchName vSwitch
Set-VMProcessor -VMName app01 -Count 4
Set-VMMemory -VMName app01 -DynamicMemoryEnabled $true -MinimumBytes 2GB -MaximumBytes 8GB
Add-VMDvdDrive -VMName app01 -Path "$root\iso\WinServer2025.iso"
Set-VMFirmware -VMName app01 -FirstBootDevice (Get-VMDvdDrive -VMName app01)
Set-VMNetworkAdapterVlan -VMName app01 -Access -VlanId 20
Enable-VMIntegrationService -VMName app01 -Name 'Guest Service Interface'
Set-VM -VMName app01 -AutomaticStartAction Start -AutomaticStopAction ShutDown -CheckpointType Production
Start-VM app01
```

## Linux on Gen 2
To Secure Boot a generation 2 Linux VM, choose the UEFI CA Secure Boot template when creating it (`Set-VMFirmware -SecureBootTemplate`, `-EnableSecureBoot`); check the exact template name with the Hyper-V Manager list.

## Clustered VMs
Create on a CSV path, then `Add-ClusterVirtualMachineRole -VMName app01` so the cluster manages it.

## Gotchas
- `-Version` sets the configuration version for compatibility with older hosts during mixed-version periods.
- A vTPM is enabled with a key protector: `Set-VMKeyProtector -VMName app01 -NewLocalKeyProtector; Enable-VMTPM -VMName app01`.
- With Dynamic Memory the VM needs its startup memory to boot and during OS installation or upgrade, even if the minimum is lower.

## Verify
`Get-VM app01 | Select Name, Generation, Version, State`; the OS installer boots from DVD and sees the SCSI disk.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: New-VM -Generation, -MemoryStartupBytes, -NewVHDPath, -NewVHDSizeBytes, -SwitchName and -Version; generation differences (boot methods, boot volume limits, PXE, SCSI/IDE) and that generation cannot be changed; the UEFI CA Secure Boot template for Linux; Set-VMMemory -DynamicMemoryEnabled/-MinimumBytes/-MaximumBytes; Set-VMKeyProtector -NewLocalKeyProtector; startup memory is what a VM gets during OS installation. Removed as unconfirmed: the exact Linux template string, the Credential Guard claim and the Exchange or database dynamic memory remark.

Method: documentation only; no commands were run.
