---
id: computing-software.systems-network-administration.windows-server.hyper-v-nested-virtualization
name: hyper-v-nested-virtualization
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, hyper-v-host, hyper-v-vm, nested-virtualization, exposevirtualizationextensions, mac-address-spoofing, lab, containers-hyper-v-isolation, amd-nested]
level: practitioner
status: docs-checked
description: "Run Hyper-V inside a Hyper-V VM for labs, containers with Hyper-V isolation or WSL: expose virtualization extensions, networking options and supported scenarios."
sources:
  - https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/user-guide/nested-virtualization
  - https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/user-guide/enable-nested-virtualization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested virtualization on Hyper-V

**Uses (from Learn):** running applications or emulators in a nested VM, testing software
releases, training environments, Hyper-V isolation for containers.

## Requirements
- Intel with VT-x and EPT: host Windows Server 2016 or later (or Windows 10 or later); VM configuration version 8.0 or higher.
- AMD EPYC / Ryzen or later: host Windows Server 2022 or later (or Windows 11 or later); VM configuration version 9.3 or higher.
- The VM must be in the Off state when you enable it.
- In an Azure VM, set Security Type to "Standard" to use nested virtualization.
- With Windows Server 2019 or earlier as the first-level VM, use 225 vCPUs or fewer.

## Enable
Run on the physical Hyper-V host, then start the VM and install Hyper-V inside it like on a physical server:
```powershell
Stop-VM <VMName>
Set-VMProcessor -VMName <VMName> -ExposeVirtualizationExtensions $true
Start-VM <VMName>
```
Disable on a stopped VM with `-ExposeVirtualizationExtensions $false`.

## Networking for nested guests
Two options: MAC address spoofing or NAT networking. For packets to route through two virtual
switches, MAC address spoofing must be on at the first (L1) level:
```powershell
Get-VMNetworkAdapter -VMName <VMName> | Set-VMNetworkAdapter -MacAddressSpoofing On
```
For NAT, follow the NAT networking section of the Learn enable page.

## Limits
- Dynamic Memory: a VM running Hyper-V cannot have its memory adjusted while running, so
  the memory does not fluctuate even if dynamic memory is enabled; enabling nested
  virtualization alone does not change dynamic memory.
- Non-Microsoft virtualization apps in Hyper-V VMs are not supported and likely fail;
  non-Microsoft hypervisors on Hyper-V, and Hyper-V on them, are not supported.
- Nested virtualization is not suitable for Windows Server Failover Clustering or
  performance-sensitive applications.
- Supported scenarios: Hyper-V VMs on Hyper-V VMs (production is supported if your services
  are supported), Hyper-V isolated containers (one nested level in production), WSL2 in a
  nested VM. Azure Local nested is evaluation only, not production.

## Verify
- [ ] `Get-VMProcessor <VMName>` shows `ExposeVirtualizationExtensions` True.
- [ ] An inner VM starts and gets network via spoofing or NAT.

## Checked
2026-10-28. Confirmed against the Learn pages "What is Nested Virtualization for Hyper-V?" and "Run Hyper-V in a Virtual Machine with Nested Virtualization" (requirements, config versions, Azure Security Type, 225 vCPU note, enable/disable command, MAC spoofing command, memory behaviour, supported and unsupported scenarios, failover clustering note). Fixed: the earlier "dynamic memory must be off" and "not for production" claims contradict the pages. Removed as unconfirmed: memory/CPU sizing example, `-Restart` install snippet, Azure VM size list and checkpoint/live-migration restrictions.
Method: documentation only; no commands were run.
