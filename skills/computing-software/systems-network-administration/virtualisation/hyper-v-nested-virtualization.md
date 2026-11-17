---
id: computing-software.systems-network-administration.virtualisation.hyper-v-nested-virtualization
name: hyper-v-nested-virtualization
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, nested-virtualization, exposevirtualizationextensions, mac-address-spoofing, labs, windows-server]
level: practitioner
status: docs-checked
description: "Run Hyper-V (or other hypervisors) inside a Hyper-V VM: expose virtualization extensions, configure networking via MAC spoofing or NAT, and know the unsupported features."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/enable-nested-virtualization
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/nested-virtualization
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmprocessor
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested virtualization on Hyper-V

**Goal:** build a virtual Hyper-V or cluster lab, or run containers with Hyper-V isolation inside a VM.

## Requirements
- Intel VT-x with EPT: host Windows Server 2016 or later (or Windows 10 or later), VM configuration version 8.0 or higher.
- AMD EPYC / Ryzen: host Windows Server 2022 or later (or Windows 11 or later), VM configuration version 9.3 or higher.
- With Windows Server 2019 or earlier as the first-level VM, use 225 vCPUs or fewer.

## Enable
```powershell
Stop-VM -Name nestedhv
Set-VMProcessor -VMName nestedhv -ExposeVirtualizationExtensions $true
Start-VM -Name nestedhv
# then inside the guest:  Install-WindowsFeature Hyper-V -IncludeManagementTools -Restart
```

## Networking for nested VMs
Option 1, MAC spoofing (nested VMs reach the outer network directly):
```powershell
Get-VMNetworkAdapter -VMName nestedhv | Set-VMNetworkAdapter -MacAddressSpoofing On
```
Option 2, NAT inside the middle VM (an internal switch plus `New-NetNat`, then an IP address on the vEthernet adapter and gateway and DNS on each nested VM) when MAC spoofing is not possible, as in a public cloud.

## Not supported / degraded
- While Hyper-V runs inside the VM, its memory cannot be adjusted while running (even with dynamic memory enabled the amount does not fluctuate); the VM must be turned off to change memory.
- Virtualization applications other than Hyper-V are not supported in Hyper-V VMs and are likely to fail.
- Nested virtualization is not suitable for Windows Server Failover Clustering or performance-sensitive applications.
- Production use of nested Hyper-V VMs is supported (on Azure and on-premises), including Hyper-V isolated containers at one nesting level, but evaluate your services and applications first; Azure Local nested in a VM is for evaluation only.

## Verify
Install Hyper-V in the guest (`Install-WindowsFeature Hyper-V -IncludeManagementTools -Restart`); a nested VM then boots and reaches the network.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: Intel and AMD host, OS and VM configuration version prerequisites, the 225-vCPU note, Set-VMProcessor -ExposeVirtualizationExtensions, MAC address spoofing and NAT options, dynamic memory and runtime memory resize behaviour, and the production-support statements. Removed because no documentation page confirmed them: the reduced-performance and checkpoint/live-migration restriction claims (the page says production is supported) and the Get-ComputerInfo verify step.
Method: documentation only; no commands were run.
