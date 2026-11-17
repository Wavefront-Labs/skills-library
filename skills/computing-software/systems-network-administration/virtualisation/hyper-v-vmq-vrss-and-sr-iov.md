---
id: computing-software.systems-network-administration.virtualisation.hyper-v-vmq-vrss-and-sr-iov
name: hyper-v-vmq-vrss-and-sr-iov
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, vmq, vrss, sr-iov, netadapter-vmq, iovweight, network-offload, windows-server]
level: advanced
status: docs-checked
description: "Tune Hyper-V network offloads: VMQ processor assignment, vRSS for high-throughput VMs, and SR-IOV enablement with its live-migration and switch-feature trade-offs."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/hpn/hpn-software-hardware-features
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/hpn/hpn-software-only-features
  - https://learn.microsoft.com/en-us/powershell/module/netadapter/set-netadaptervmq
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmnetworkadapter
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/new-vmswitch
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VMQ, vRSS and SR-IOV on Hyper-V

**Goal:** spread VM network processing over CPU cores and, where justified, bypass the vSwitch with SR-IOV.

## VMQ / VMMQ
VMQ gives each vNIC its own hardware queue, processed on a chosen core.
```powershell
Get-NetAdapterVmq | Format-Table Name, Enabled, BaseProcessorNumber, MaxProcessors, NumberOfReceiveQueues
Set-NetAdapterVmq -Name 'NIC1' -BaseProcessorNumber 2 -MaxProcessors 8
```
- `Set-NetAdapterVmq` has `-BaseProcessorNumber`, `-MaxProcessors`, `-MaxProcessorNumber` and `-NumaNode` for placing queues on processors.
- Microsoft's guidance is that whenever Hyper-V is enabled, VMQ must also be enabled; VMMQ spreads one VM's traffic over multiple queues, each processed by a different processor.

## vRSS
Software vRSS spreads incoming traffic for a VM across multiple logical processors of the VM, so the VM can handle more network traffic than one LP could. Check RSS in the guest with `Get-NetAdapterRss`.

## SR-IOV
A virtual function of the physical NIC is mapped directly into the VM.
```powershell
New-VMSwitch -Name 'SRIOV' -NetAdapterName 'NIC3' -EnableIov $true   # only at creation
Set-VMNetworkAdapter -VMName db01 -IovWeight 100
Get-VMNetworkAdapter -VMName db01 | Format-List Status, VirtualFunction
```
`-IovWeight` ranges from 0 to 100; 0 disables SR-IOV on the vNIC. With `-MinimumBandwidthMode Default`, a switch that is IOV-enabled gets mode None, so weight-based minimum bandwidth is not available on it.

### Trade-offs
- SR-IOV traffic bypasses the Hyper-V switch: policies such as ACLs and bandwidth management are not applied, and it cannot go through network virtualization encapsulation (NV-GRE, VXLAN). Microsoft advises using it only for workloads where the extra performance is needed.
- `-EnableIov` is a `New-VMSwitch` parameter (it is not in `Set-VMSwitch`), so choose it when creating the switch.

## Verify
`Get-NetAdapterVmq` shows the intended processor assignment, and for SR-IOV `Get-VMNetworkAdapter` shows the virtual function status.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: VMQ allocates a queue per VM and should be enabled with Hyper-V, VMMQ, software vRSS description, SR-IOV bypasses the switch (ACLs, bandwidth management, NV-GRE and VXLAN not applied), Set-NetAdapterVmq processor parameters, Set-VMNetworkAdapter -IovWeight range 0 to 100, New-VMSwitch -EnableIov and the Default minimum bandwidth mode behaviour on IOV switches. Removed as unconfirmed: core 0 and starting-core advice, 1 GbE driver remark, vCPU and bandwidth thresholds for vRSS, IOMMU and firmware requirements, and live migration failover behaviour.

Method: documentation only; no commands were run.
