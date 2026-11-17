---
id: computing-software.systems-network-administration.virtualisation.hyper-v-cluster-network-roles
name: hyper-v-cluster-network-roles
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, cluster-network-role, cluster-network-metric, failover-clustering, csv-traffic, heartbeat, windows-server]
level: advanced
status: gated
description: "Set failover cluster network roles and metrics for Hyper-V: cluster-only vs client, excluded storage networks, CSV preference, live migration networks, heartbeat thresholds."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/failover-cluster-network-recommendations
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/configure-live-migration-smb-bandwidth
  - https://techcommunity.microsoft.com/blog/failoverclustering/configuring-network-prioritization-on-a-failover-cluster/371683
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Cluster network roles and metrics

**Goal:** route heartbeat, CSV redirected I/O, live migration and client traffic over the intended networks.

## Traffic types
The Hyper-V cluster network recommendations describe separate networks for management, cluster (heartbeat and CSV redirection), live migration, storage (SMB or iSCSI) and VM access. Use a dedicated network or VLAN for live migration.

## Roles and metrics
Cluster network role values are commonly written as 0 (not used by the cluster), 1 (cluster communication only) and 3 (cluster and client) (gated: unconfirmed, source is paywalled or blocked), and the lowest metric is preferred for cluster and CSV traffic (gated: unconfirmed, source is paywalled or blocked).
```powershell
Get-ClusterNetwork | Format-Table Name, Role, Metric, AutoMetric, Address
(Get-ClusterNetwork 'Cluster Network 2').Name = 'iSCSI-A'
(Get-ClusterNetwork 'iSCSI-A').Role = 0
```
The reason for the marker is that the source for the role numbers, the metric rule and the heartbeat defaults (a Tech Community blog) could not be retrieved; confirm them in the current Failover Clustering documentation before changing a production cluster.

## Live migration networks
The documented method is the `MigrationExcludeNetworks` parameter on the Virtual Machine resource type:
```powershell
Get-ClusterResourceType -Name 'Virtual Machine' | Get-ClusterParameter -Name MigrationNetworkOrder, MigrationExcludeNetworks
Get-ClusterResourceType -Name 'Virtual Machine' | Set-ClusterParameter -Name MigrationExcludeNetworks -Value ((Get-ClusterNetwork 'Management').Id)
```
Multiple IDs are joined with `;`. The recommendations page shows the same cmdlet used to allow migration only on a network named `Migration_Network`.

## Heartbeat tolerance
```powershell
Get-Cluster | Format-List SameSubnetDelay, SameSubnetThreshold, CrossSubnetDelay, CrossSubnetThreshold
```
The `CrossSubnetDelay` property is shown in the Get-Cluster reference; default values are not confirmed (gated: unconfirmed, source is paywalled or blocked). Raise thresholds only for known transient links; it slows real failure detection.

## Verify
`Get-ClusterNetworkInterface` shows all interfaces Up, and a test migration uses the intended network.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed in the Hyper-V cluster network recommendations page: cluster traffic covers heartbeat and CSV redirection, storage networks carry SMB or iSCSI, live migration should use a dedicated network, and the MigrationExcludeNetworks cluster parameter on the Virtual Machine resource type is the documented way to restrict live migration networks. Role numbers, metric behaviour and heartbeat defaults come from a Tech Community blog whose body could not be retrieved, so they carry the gated marker. Removed as unconfirmed: single-point-of-failure and subnet-merging remarks.

Method: documentation only; no commands were run.
