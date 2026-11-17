---
id: computing-software.systems-network-administration.virtualisation.hyper-v-role-install-and-host-settings
name: hyper-v-role-install-and-host-settings
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v-install, hyper-v-host, install-windowsfeature-hyper-v, numa-spanning, hyper-v-settings, server-core, enhanced-session, hyper-v, windows-server, slat, hyper-v-requirements]
level: practitioner
status: docs-checked
description: "Build a Hyper-V host: role install with PowerShell, hardware prerequisites, default VM/VHD paths, NUMA spanning, live migration limits and nested virtualization."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/get-started/install-hyper-v
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/host-hardware-requirements
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/non-uniform-memory-access
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmhost
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hyper-V role install and host settings

**Goal:** a Hyper-V host installed the same way every time, with defaults that keep VM
files off the system drive and memory placement predictable.

## Prerequisites
- A 64-bit processor with second-level address translation (SLAT), hardware-assisted virtualisation (Intel VT or
  AMD-V) and hardware-enforced DEP (XD/NX) available and enabled. SLAT is required to install the hypervisor but
  not the management tools. The requirements page explains how to check a machine with `systeminfo`.
- Hyper-V requirements exceed the general Windows Server minimums; check the Windows Server catalogue.
- Server Core is a supported host installation: installing with `-IncludeManagementTools` on Server Core adds only
  the Hyper-V PowerShell module, and Hyper-V Manager runs on another computer.
- Do not run other server roles in the root partition: they can hurt performance and widen the attack surface.
- Licensing: Datacenter allows unlimited Windows Server VMs; Standard includes 2 VMs.

## Install
```powershell
Install-WindowsFeature -Name Hyper-V -IncludeManagementTools -Restart
# Remote: Install-WindowsFeature -Name Hyper-V -ComputerName hv01 -IncludeManagementTools -Restart
Get-WindowsFeature Hyper-V
```
Third-party hypervisor apps (VMware Workstation, VirtualBox) can fail or run unreliably while the Hyper-V
hypervisor is running.

## Host defaults
```powershell
Set-VMHost -VirtualHardDiskPath '<DATA_VOL>\Hyper-V\Virtual Hard Disks' -VirtualMachinePath '<DATA_VOL>\Hyper-V'
Set-VMHost -NumaSpanningEnabled $false          # see below
Set-VMHost -EnableEnhancedSessionMode $true
Set-VMHost -MaximumVirtualMachineMigrations 2 -MaximumStorageMigrations 2
Get-VMHost | Format-List *
```
(Use your data volume path; on clusters VM paths live on CSVs instead. The default for simultaneous live
migrations is 2.)
- **NUMA spanning:** by default, if one physical NUMA node cannot satisfy a VM's memory, Hyper-V allocates memory
  from another node. That lets more VMs run but can reduce performance; constraining VMs to one node gives more
  predictable performance but you may not be able to use all host memory. Starting with Windows Server 2025 (and
  Windows 11 24H2), a VM that needs more virtual cores than a NUMA node has must have NUMA spanning configured on
  both the host and the VM. Benchmark before changing it.
- **Dynamic Memory** and virtual NUMA cannot be used together: a VM with Dynamic Memory effectively has one virtual
  NUMA node.

## Gotchas
- Antivirus on the host must follow Microsoft's exclusion list (see the antivirus exclusions skill), or VMs can
  fail to start.
- Nested virtualisation (the Hyper-V host itself running as a VM) needs
  `Set-VMProcessor -VMName <vm> -ExposeVirtualizationExtensions $true` on the outer VM.

## Verify
`Get-WindowsFeature Hyper-V` shows Installed; `Get-VMHost` shows the intended paths and NUMA setting; a test VM
creates its files on the data volume.

## Checked

Date checked: 2026-10-27. Documentation: Install Hyper-V, Hyper-V host hardware requirements, NUMA in Hyper-V, nested virtualisation and Hyper-V performance configuration pages (windowsserverdocs main branch, Windows Server 2025); Set-VMHost reference (Windows Server 2025 docset).
Confirmed: Install-WindowsFeature syntax and Server Core note; SLAT, VT/AMD-V and DEP requirements; Set-VMHost parameter names including -NumaSpanningEnabled, -EnableEnhancedSessionMode, -MaximumVirtualMachineMigrations and -MaximumStorageMigrations; default of two simultaneous live migrations; NUMA spanning default and the Windows Server 2025 change; Dynamic Memory versus virtual NUMA; -ExposeVirtualizationExtensions; Standard 2 VMs versus Datacenter unlimited.

Method: documentation only; no commands were run.
