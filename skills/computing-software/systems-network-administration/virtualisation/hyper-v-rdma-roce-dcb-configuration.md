---
id: computing-software.systems-network-administration.virtualisation.hyper-v-rdma-roce-dcb-configuration
name: hyper-v-rdma-roce-dcb-configuration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [roce-dcb-pfc, rdma, smb-direct, dcb, hyper-v]
level: advanced
status: docs-checked
description: "Configure RDMA (RoCE v2 or iWARP) with DCB, PFC and ETS for SMB Direct storage and live migration traffic on Hyper-V hosts, matching switch settings."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-local/concepts/host-network-requirements
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-direct
  - https://learn.microsoft.com/en-us/powershell/module/dcbqos/new-netqostrafficclass
  - https://learn.microsoft.com/en-us/powershell/module/dcbqos/enable-netqosflowcontrol
  - https://learn.microsoft.com/en-us/powershell/module/dcbqos/set-netqosdcbxsetting
  - https://learn.microsoft.com/en-us/powershell/module/netqos/new-netqospolicy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDMA, RoCE and DCB for storage traffic

**Goal:** lossless, low-latency SMB Direct for S2D, SOFS and live migration.

## RoCE v2 needs DCB end to end
```powershell
Install-WindowsFeature Data-Center-Bridging
# Tag traffic
New-NetQosPolicy 'SMB'     -NetDirectPortMatchCondition 445 -PriorityValue8021Action 3
New-NetQosPolicy 'Cluster' -Cluster -PriorityValue8021Action 7
New-NetQosPolicy 'Default' -Default -PriorityValue8021Action 0
# Lossless only for SMB
Enable-NetQosFlowControl  -Priority 3
Disable-NetQosFlowControl -Priority 0,1,2,4,5,6,7
# Bandwidth reservations (ETS)
New-NetQosTrafficClass 'SMB'     -Priority 3 -BandwidthPercentage 50 -Algorithm ETS   # 50 percent is Microsoft's example reservation
New-NetQosTrafficClass 'Cluster' -Priority 7 -BandwidthPercentage 1  -Algorithm ETS   # system class: 1 percent on 25 GbE+, 2 percent on 10 GbE or lower
# Host decides, ignore switch DCBX
Set-NetQosDcbxSetting -Willing $false
Enable-NetAdapterQos -Name 'pNIC1','pNIC2'
```
PFC and ETS must be configured consistently on every network port, including the switches. Microsoft's Azure Local guidance for RoCE is three traffic classes: system/heartbeat on priority 7 (not PFC-enabled), RDMA on priority 3 or 4 (PFC-enabled, 50 percent example) and the default class (priority 0, no host configuration). Use the same priority on hosts and switches.

## iWARP
Runs over TCP; PFC and ETS are optional for iWARP but required for RoCE. RDMA adapters only interoperate with adapters that use the same protocol (iWARP or RoCE).

## RDMA on SET vNICs
```powershell
Add-VMNetworkAdapter -ManagementOS -SwitchName SETswitch -Name SMB1
Add-VMNetworkAdapter -ManagementOS -SwitchName SETswitch -Name SMB2
Enable-NetAdapterRdma -Name 'vEthernet (SMB1)','vEthernet (SMB2)'
Set-VMNetworkAdapterTeamMapping -ManagementOS -VMNetworkAdapterName SMB1 -PhysicalNetAdapterName pNIC1
Set-VMNetworkAdapterTeamMapping -ManagementOS -VMNetworkAdapterName SMB2 -PhysicalNetAdapterName pNIC2
```
For live migration, Microsoft's guidance is SMB (`Set-VMHost -VirtualMachineMigrationPerformanceOption SMB`) when at least 5 Gbps is available for it and the adapters are RDMA-capable, otherwise Compression; cap it with `Set-SMBBandwidthLimit -Category LiveMigration -BytesPerSecond 750MB` so it cannot take the whole RDMA class (the cmdlet takes bytes per second).

## Verify
```powershell
Get-NetAdapterRdma | Where Enabled
Get-SmbClientNetworkInterface | Where RdmaCapable
Get-SmbMultichannelConnection
Get-NetQosFlowControl; Get-NetAdapterQos
```
During a large file copy the Performance Monitor counters *SMB Direct Connection > Bytes RDMA Read/sec* and *Bytes RDMA Written/sec* should rise; compare copy time with RDMA disabled and enabled.

## Checked

Checked 2026-10-26 against the Azure Local host network requirements page (MicrosoftDocs/azure-stack-docs, latest commit 2026-10-23), the SMB Direct page in windowsserverdocs, and the Windows Server 2016 and later cmdlet references for `New-NetQosTrafficClass`, `Enable/Disable-NetQosFlowControl`, `Set-NetQosDcbxSetting`, `New-NetQosPolicy` (`-NetDirectPortMatchCondition`, `-Cluster`, `-Default`), `Enable-NetAdapterQos` and `Set-VMNetworkAdapterTeamMapping`. Corrected: the system traffic class share depends on link speed (1 or 2 percent) and is not PFC-enabled; iWARP does not need DCB (the earlier "recommended at scale" claim was not in the source); the RDMA counters named in the Verify section were not documented, so the documented SMB Direct Connection counters replace them; the `Client RDMA Capable` output claim was removed. Switch-side configuration is vendor specific and not covered here.

Method: documentation only; no commands were run.
