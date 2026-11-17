---
id: computing-software.systems-network-administration.virtualisation.hyper-v-live-migration-networks
name: hyper-v-live-migration-networks
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmmigrationnetwork, live-migration-network, simultaneous-live-migrations, hyper-v-live-migration, failover-clustering, hyper-v]
level: practitioner
status: docs-checked
description: "Choose which networks Hyper-V live migration uses on standalone hosts and in clusters, set simultaneous migration limits, and keep migration off the management network."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/set-up-hosts-for-live-migration-without-failover-clustering
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/failover-cluster-network-recommendations
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/configure-live-migration-smb-bandwidth
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/add-vmmigrationnetwork
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/get-cluster
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/set-smbbandwidthlimit
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live migration networks and limits

## Standalone hosts (Hyper-V settings)
```powershell
Enable-VMMigration
Set-VMHost -UseAnyNetworkForMigration $false
Add-VMMigrationNetwork 10.10.50.0/24 -Priority 1
Add-VMMigrationNetwork 10.10.51.0/24 -Priority 2
Get-VMMigrationNetwork
Set-VMHost -MaximumVirtualMachineMigrations 2 -MaximumStorageMigrations 2
```
`Add-VMMigrationNetwork` takes a subnet in CIDR form and an optional `-Priority`. Live migration authentication is Kerberos (needs constrained delegation) or CredSSP (needs a sign-in to the source server), set with `Set-VMHost -VirtualMachineMigrationAuthenticationType`.

## Failover clusters (cluster settings win)
In clusters, the **cluster** decides: Failover Cluster Manager → Networks → Live Migration
Settings → tick and order networks. PowerShell:
```powershell
Get-ClusterNetwork | Select Name, Role, Address, Metric
# exclude networks by ID from migration (cluster parameter on the VM resource type)
$exclude = (Get-ClusterNetwork | ? Name -in 'Management','Storage1').Id -join ';'
Get-ClusterResourceType -Name "Virtual Machine" | Set-ClusterParameter -Name MigrationExcludeNetworks -Value $exclude
Get-ClusterResourceType -Name "Virtual Machine" | Get-ClusterParameter MigrationNetworkOrder, MigrationExcludeNetworks
```
The simultaneous migration count can be set per node with `Set-VMHost`; from the 2022-09 cumulative update on Windows Server 2022 (KB5017381) the cluster property `(Get-Cluster).MaximumParallelMigrations` can be set instead, and it overrides the `Set-VMHost` values on all nodes.

## Sizing simultaneous migrations
- The default number of simultaneous live migrations is 2. Compression is the default performance option; SMB is the alternative.
- Node drain moves all VMs, queued by this limit; higher values shorten drain time only
  if bandwidth allows.

## SMB-based migration bandwidth cap
When using `-VirtualMachineMigrationPerformanceOption SMB`, cap migration so it doesn't
starve S2D storage traffic on shared NICs:
```powershell
Set-SmbBandwidthLimit -Category LiveMigration -BytesPerSecond 750MB
```
(requires the `FS-SMBBW` feature).

## Gotchas
- `Set-VMHost -UseAnyNetworkForMigration $true` lets migration use any available network, including the management NIC: keep it `$false` and list the intended networks.
- Use a dedicated network or VLAN for live migration so it does not raise latency for other traffic.

## Verify
During a test migration, `Get-NetTCPConnection` or performance counters show
traffic on the intended NIC/subnet; drain completes in the expected time.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: Enable-VMMigration, Add-VMMigrationNetwork with a subnet and -Priority, Set-VMHost -UseAnyNetworkForMigration, -MaximumVirtualMachineMigrations, -MaximumStorageMigrations, default of 2 simultaneous migrations, compression as the default performance option, Kerberos and CredSSP choices, MigrationExcludeNetworks on the Virtual Machine resource type, Set-SmbBandwidthLimit -Category LiveMigration (FS-SMBBW feature), and the cluster MaximumParallelMigrations property. Removed as unconfirmed: TCP port 6600, throughput-based sizing figures, and the role None remark.

Method: documentation only; no commands were run.
