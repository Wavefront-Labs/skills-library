---
id: computing-software.systems-network-administration.windows-server.rdma-rss-vmq-offloads
name: rdma-rss-vmq-offloads
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, netadapter, server-networking, rdma, rss-vmq, rss, vmq, vrss, smb-direct, roce, iwarp, dcb, enable-netadapterrdma, get-smbclientnetworkinterface]
level: advanced
status: docs-checked
description: "Tune NIC offloads on Windows Server: RSS for host traffic, VMQ/vRSS for Hyper-V, RDMA (iWARP vs RoCE with DCB/PFC) for SMB Direct, and how to verify each."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/network-subsystem/net-sub-performance-tuning-nics
  - https://learn.microsoft.com/en-us/azure/azure-local/concepts/host-network-requirements
  - https://learn.microsoft.com/en-us/powershell/module/netadapter/set-netadapterrss
  - https://learn.microsoft.com/en-us/powershell/module/netadapter/enable-netadapterrdma
  - https://learn.microsoft.com/en-us/powershell/module/dcbqos/new-netqostrafficclass
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDMA, RSS and VMQ

## RSS (Receive Side Scaling)
Spreads inbound host traffic across CPU cores. The default RSS profile is `NUMAStatic` and the default queue count is
two (the driver may allow more); if cores look underused for receive traffic, raising the queue count is the documented
tuning step. Check the current settings:
```powershell
Get-NetAdapterRss -Name NIC1 | Select Name,Enabled,BaseProcessorNumber,MaxProcessors,Profile
Set-NetAdapterRss -Name NIC1 -BaseProcessorNumber 2 -MaxProcessors 8
```
Microsoft's tuning guidance is to handle NIC interrupts and DPCs on a core that shares cache with the core running the
consuming thread. Avoid mixing RSS-capable and non-RSS adapters on a web server.

## VMQ and vRSS (Hyper-V)
VMQ gives each vNIC its own hardware queue; vRSS spreads a VM's traffic across virtual processors. **Dynamic VMMQ**
builds on both, tunes processing to cores automatically, requires Switch Embedded Teaming and is supported by adapters
with the Compute (Premium) qualification.
```powershell
Get-NetAdapterVmq ; Get-NetAdapterVmqQueue
Get-VMNetworkAdapter -VMName app01 | Select Name,VmqWeight,VrssEnabled
```

## RDMA for SMB Direct (S2D, live migration, SOFS)
- RDMA adapters only interoperate with adapters using the same protocol (iWARP or RoCE); both are supported on
  Azure Local.
- **DCB** is required for RoCE and optional for iWARP. Where DCB is used, PFC and ETS must be configured on every host
  and switch port. The Azure Local guidance for RoCE is three traffic classes: system (priority 7, not PFC,
  1 to 2 percent), RDMA/SMB Direct (priority 3 or 4, PFC enabled, 50 percent) and default (priority 0).
  The values below are the Azure Local recommendations, not universal defaults.
```powershell
Enable-NetAdapterRdma -Name 'NIC1','NIC2'
Get-NetAdapterRdma | ? Enabled
Get-SmbClientNetworkInterface | Select FriendlyName,RdmaCapable,RssCapable,Speed
Get-SmbMultichannelConnection        # RDMA used if ClientRdmaCapable/ServerRdmaCapable True
# DCB host sketch (cmdlets from the DcbQoS module; install the Data-Center-Bridging feature first):
New-NetQosPolicy 'SMB' -NetDirectPortMatchCondition 445 -PriorityValue8021Action 3
Enable-NetQosFlowControl -Priority 3 ; Disable-NetQosFlowControl -Priority 0,1,2,4,5,6,7
New-NetQosTrafficClass 'SMB' -Priority 3 -BandwidthPercentage 50 -Algorithm ETS
Enable-NetAdapterQos -Name 'NIC1','NIC2'
```
Microsoft points to the RDMA deployment document in the SDN GitHub repository for manual deployment, and recommends
Network ATC where available.

## Verify
- [ ] `Get-SmbMultichannelConnection` shows RDMA-capable client and server interfaces in use during a file copy or live migration.
- [ ] `Get-NetAdapterRss` shows the intended queues and processors, and Task Manager shows receive load spread across cores.

## Checked

2026-10-27. Documentation release: Azure Local host network requirements, Windows Server networking performance tuning for NICs, and Storage/NetAdapter/DcbQoS/SmbShare cmdlet references (Windows Server 2022 docset). Confirmed: RSS default profile and queue count, Dynamic VMMQ requirements, RDMA protocol interoperability, DCB required for RoCE and optional for iWARP, recommended priorities and bandwidth reservations, and the parameter names used in the examples. Removed the core-0 advice, the Broadcom VMQ pitfall, the Test-RDMA and Validate-DCB tool names, the perfmon counter names and the '2019+' statement as unconfirmed. Confirmed the Get-NetAdapterRdma, Get-NetAdapterVmqQueue, Set-NetAdapterRss (-BaseProcessorNumber, -MaxProcessors) and Set-VMNetworkAdapter (-VmqWeight, -VrssEnabled) cmdlets and parameters.

Method: documentation only; no commands were run.
