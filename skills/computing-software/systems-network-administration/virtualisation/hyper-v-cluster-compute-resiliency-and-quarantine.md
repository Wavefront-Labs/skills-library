---
id: computing-software.systems-network-administration.virtualisation.hyper-v-cluster-compute-resiliency-and-quarantine
name: hyper-v-cluster-compute-resiliency-and-quarantine
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [compute-resiliency, vm-resiliency, node-quarantine, failover-cluster, hyper-v]
level: advanced
status: gated
description: "Tune Hyper-V cluster VM compute resiliency and node quarantine: isolation and unmonitored VMs, resiliency periods, quarantine thresholds and clearing quarantine."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/get-cluster
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/start-clusternode
  - https://techcommunity.microsoft.com/blog/failoverclustering/virtual-machine-compute-resiliency-in-windows-server-2016/372027
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# VM compute resiliency and node quarantine

**Goal:** short network blips do not trigger mass VM failovers, while flapping nodes are taken out of service.

## Isolation
When a node briefly loses cluster communication it can enter an **Isolated** state and keep its VMs running as unmonitored for a resiliency period instead of failing them over (gated: unconfirmed, source is paywalled or blocked). Property names and values for tuning it, as commonly written, are listed below and must be confirmed against the Windows Server 2016 compute resiliency blog before use (gated: unconfirmed, source is paywalled or blocked).
```powershell
Get-Cluster | Select ResiliencyLevel, ResiliencyDefaultPeriod
(Get-Cluster).ResiliencyDefaultPeriod = 240      # seconds
(Get-ClusterGroup app01).ResiliencyPeriod = 60   # per-VM override
```
The reason is that the blog page body could not be read here, so the defaults, the meaning of level values, and the -1 per-VM convention are not confirmed.

## Quarantine
The Get-Cluster reference documents the quarantine settings: `QuarantineThreshold` is the number of times a node can become isolated in an hour before the node is quarantined (default 3), and `QuarantineDuration` is how long it stays quarantined (default 7200 seconds, 2 hours).
```powershell
Get-Cluster | Format-List -Property Quarantine*
Get-ClusterNode | Select Name, State, StatusInformation
Start-ClusterNode -Name hv03 -ClearQuarantine      # after fixing the cause
```
`Start-ClusterNode -ClearQuarantine` is a documented switch.

## Tuning
- Fix flapping networks rather than masking them with longer periods.
- Heartbeat thresholds (`SameSubnetThreshold`, `CrossSubnetThreshold`) interact with isolation; change them together and sparingly.

## Verify
Cluster events show node isolation and quarantine transitions; after a planned NIC pull the VMs behave as intended.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed in the Get-Cluster and Start-ClusterNode references: QuarantineThreshold (default 3, counted per hour) and QuarantineDuration (default 7200 seconds) exist, and Start-ClusterNode has -ClearQuarantine. The isolation, unmonitored and resiliency property names, values and defaults come from a Microsoft Tech Community blog whose page body could not be retrieved, so they carry the gated marker.

Method: documentation only; no commands were run.
