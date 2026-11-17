---
id: computing-software.systems-network-administration.virtualisation.hyper-v-linux-guests
name: hyper-v-linux-guests
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [linux-integration-services, hv-kvp, secure-boot-template, microsoft-uefi-ca, hyper-v-vm, generation-2, hyper-v]
level: practitioner
status: docs-checked
description: "Run Linux well on Hyper-V: Gen 2 with the Microsoft UEFI CA secure boot template, built-in hv drivers, KVP/VSS/fcopy daemons, disk and NIC settings, and common issues."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/best-practices-for-running-linux-on-hyper-v
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/supported-linux-and-freebsd-virtual-machines-for-hyper-v-on-windows
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/supported-ubuntu-virtual-machines-on-hyper-v
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/supported-centos-and-red-hat-enterprise-linux-virtual-machines-on-hyper-v
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/generation-2-virtual-machine-security-features
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmfirmware
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux guests on Hyper-V

## Create
```powershell
New-VM -Name web01 -Generation 2 -MemoryStartupBytes 4GB -SwitchName vSwitch1 -NewVHDPath "<VM_DIR>\web01.vhdx" -NewVHDSizeBytes 40GB
Set-VMProcessor -VMName web01 -Count 2
Add-VMDvdDrive -VMName web01 -Path "<ISO_DIR>\ubuntu-24.04-live-server-amd64.iso"
Set-VMFirmware -VMName web01 -FirstBootDevice (Get-VMDvdDrive -VMName web01)
```
## Secure Boot
Generation 2 VMs have Secure Boot enabled by default and some Linux VMs will not boot unless it is disabled or a suitable template is chosen. Microsoft's Generation 2 security page lists three templates: *Microsoft Windows* (Windows guests), *Microsoft UEFI Certificate Authority* (Linux distributions) and *Open Source Shielded VM* (Linux shielded VMs). `Set-VMFirmware -SecureBootTemplate` takes the template name. To turn Secure Boot off, as the Ubuntu support page documents:
```powershell
Set-VMFirmware -VMName web01 -EnableSecureBoot Off
```

## Integration services
Linux Integration Services (LIS) are part of the Linux kernel and updated with new releases; distributions on older kernels may lack enhancements, and Microsoft provides a LIS download for some of them. For distributions with built-in LIS, the user-space daemons come in a package: on RHEL and CentOS install `hyperv-daemons` (older releases: `hypervkvpd`) to enable key/value pair (KVP) exchange and the other daemon-based features. Check your distribution's support page for the package name and feature list.

## Best practices (Microsoft's list)
- Dynamic VHDX: create with `-BlockSizeBytes 1MB` instead of the 32 MB default, prefer ext4 to ext3, and create file systems with `mkfs.ext4 -G 4096`:
```powershell
New-VHD -Path "<VM_DIR>\data.vhdx" -SizeBytes 127GB -Dynamic -BlockSizeBytes 1MB
```
- Use a static MAC address on each virtual NIC for clustered Linux VMs (`Set-VMNetworkAdapter -StaticMacAddress`), because networking configuration can be lost after failover when the MAC changes.
- Use the Hyper-V-specific network adapter and remove legacy adapters; with both present, interface names can show random values.
- Use the `noop` I/O scheduler (blk subsystem) or `none` (blk-mq) so scheduling is left to the hypervisor; set it through `/sys/class/block/<disk>/queue/scheduler` and persist it in an init script.
- Kernels older than 2.6.37 (and RHEL kernels older than 2.6.32-504) do not support NUMA on Hyper-V with larger VM sizes and need `numa=off`.
- Generation 2 VMs: the grub menu timer can count down too quickly, and PXE boot has known limits (see the best practices page).

## Gotchas
- Without the KVP daemon the host cannot read guest data such as IP addresses.

## Verify
`Get-VMNetworkAdapter -VMName web01 | Select IPAddresses` shows guest IPs (this needs KVP in the guest).

## Checked

Checked 2026-10-26 against MicrosoftDocs/windowsserverdocs (Best practices for running Linux on Hyper-V, Supported Linux and FreeBSD VMs, Ubuntu and RHEL/CentOS support pages, Generation 2 security features; latest commit 2026-10-23) and the Windows Server 2025 `Set-VMFirmware` reference. Confirmed: 1 MB `BlockSizeBytes` versus 32 MB default, ext4 and `mkfs.ext4 -G 4096`, static MAC for clustering, legacy adapter naming issue, noop/none scheduler, NUMA kernel limit, Secure Boot default and the three template names, `Set-VMFirmware -EnableSecureBoot Off`, `hyperv-daemons`/`hypervkvpd` for KVP, LIS in kernel. Removed as undocumented: the `-SecureBootTemplate` token and quoted error message, the Ubuntu cloud-tools package names, hv_* daemon table, time synchronisation advice, 128 MB hot-add remark and the production checkpoint claim.

Method: documentation only; no commands were run.
