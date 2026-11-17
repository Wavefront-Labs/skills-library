---
id: computing-software.systems-network-administration.virtualisation.hyper-v-converged-host-vnics-on-set
name: hyper-v-converged-host-vnics-on-set
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [host-vnic, converged-networking, switch-embedded-teaming, hyper-v-switch, smb-direct, hyper-v]
level: advanced
status: docs-checked
description: "Build converged Hyper-V host networking on a SET switch: management, live migration and SMB host vNICs, VLANs, team mapping for RDMA, and bandwidth weights."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/virtual-switch
  - https://learn.microsoft.com/en-us/azure/azure-local/concepts/host-network-requirements
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/new-vmswitch
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmnetworkadapterteammapping
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converged host vNICs on a SET switch

Two (or more) fast NICs carry everything: VM traffic plus host vNICs for management,
live migration, cluster and SMB storage, separated by VLAN and QoS.

## Build
```powershell
New-VMSwitch -Name ConvergedSwitch -NetAdapterName "NIC1","NIC2" `
  -EnableEmbeddedTeaming $true -AllowManagementOS $false -MinimumBandwidthMode Weight
Set-VMSwitchTeam -Name ConvergedSwitch -LoadBalancingAlgorithm HyperVPort

Add-VMNetworkAdapter -ManagementOS -SwitchName ConvergedSwitch -Name Mgmt
Add-VMNetworkAdapter -ManagementOS -SwitchName ConvergedSwitch -Name LiveMigration
Add-VMNetworkAdapter -ManagementOS -SwitchName ConvergedSwitch -Name SMB1
Add-VMNetworkAdapter -ManagementOS -SwitchName ConvergedSwitch -Name SMB2

Set-VMNetworkAdapterVlan -ManagementOS -VMNetworkAdapterName Mgmt -Access -VlanId 10
Set-VMNetworkAdapterVlan -ManagementOS -VMNetworkAdapterName LiveMigration -Access -VlanId 50
Set-VMNetworkAdapterVlan -ManagementOS -VMNetworkAdapterName SMB1 -Access -VlanId 711
Set-VMNetworkAdapterVlan -ManagementOS -VMNetworkAdapterName SMB2 -Access -VlanId 712

# pin each SMB vNIC to one physical NIC so RDMA paths are deterministic
Set-VMNetworkAdapterTeamMapping -ManagementOS -VMNetworkAdapterName SMB1 -PhysicalNetAdapterName NIC1
Set-VMNetworkAdapterTeamMapping -ManagementOS -VMNetworkAdapterName SMB2 -PhysicalNetAdapterName NIC2
Enable-NetAdapterRdma -Name "vEthernet (SMB1)","vEthernet (SMB2)"

# QoS weights (switch created in Weight mode)
Set-VMNetworkAdapter -ManagementOS -Name Mgmt -MinimumBandwidthWeight 5
Set-VMNetworkAdapter -ManagementOS -Name LiveMigration -MinimumBandwidthWeight 20
Set-VMSwitch ConvergedSwitch -DefaultFlowMinimumBandwidthWeight 40
```
Then assign IPs to the `vEthernet (...)` adapters with `New-NetIPAddress`.

## RDMA notes
RDMA adapters only work with adapters that use the same RDMA protocol (iWARP or RoCE). iWARP uses TCP and can optionally be enhanced with PFC and ETS. For RoCE and DCB design, follow the current Azure Local host network requirements and your switch vendor's guidance.

## Gotchas
- `-MinimumBandwidthMode` is a `New-VMSwitch` parameter (Weight mode takes values 1 to 100); `Set-VMSwitch` has no such parameter, so choose it when creating the switch.
- SET supports only switch-independent teaming with Dynamic or Hyper-V Port load balancing (Hyper-V Port recommended at 10 Gbps and above); no LACP.
- Build remotely only with out-of-band access: `-AllowManagementOS $false` creates the switch without a management vNIC until you add one.
- SET requires symmetric adapters: same make, model, speed and configuration.

## Verify
`Get-VMNetworkAdapter -ManagementOS`, `Get-VMNetworkAdapterVlan -ManagementOS`,
`Get-VMNetworkAdapterTeamMapping -ManagementOS`, `Get-NetAdapterRdma` (Enabled True),
`Get-SmbClientNetworkInterface` shows RDMA capable; `Test-Cluster` network tests pass.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: New-VMSwitch -EnableEmbeddedTeaming, -AllowManagementOS and -MinimumBandwidthMode (Weight is 1 to 100) and that Set-VMSwitch has no -MinimumBandwidthMode parameter; Set-VMSwitchTeam -LoadBalancingAlgorithm; Set-VMNetworkAdapterTeamMapping -ManagementOS -PhysicalNetAdapterName; Set-VMNetworkAdapter -MinimumBandwidthWeight and Set-VMSwitch -DefaultFlowMinimumBandwidthWeight; SET symmetric adapter rule, switch-independent only, Dynamic or Hyper-V Port algorithms (Azure Local host network requirements). Removed as unconfirmed: the RoCE DCB/PFC rules, the DNS registration advice and the claim that the host loses its IP.

Method: documentation only; no commands were run.
