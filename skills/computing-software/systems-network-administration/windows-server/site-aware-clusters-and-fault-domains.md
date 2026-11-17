---
id: computing-software.systems-network-administration.windows-server.site-aware-clusters-and-fault-domains
name: site-aware-clusters-and-fault-domains
category: computing-software
field: systems-network-administration
product: windows-server
tags: [failover-clustering, site-aware-cluster, fault-domains, stretch-cluster, cluster-quorum]
level: advanced
status: docs-checked
description: "Configure site and fault domain awareness: New-ClusterFaultDomain for sites, racks and chassis, preferred site and quorum."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/fault-domains
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/stretch-cluster-replication-using-shared-storage
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/new-clusterfaultdomain
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Site-aware clusters and fault domains

Fault domains tell the cluster which nodes share a failure point (site, rack, chassis) so Storage Spaces keeps data
copies in separate fault domains, the Health Service adds location metadata to alerts, and stretch clusters get storage
affinity. The four levels are site, rack, chassis and node; nodes are discovered automatically and the other levels are
optional.

## Define sites and assign nodes
```powershell
New-ClusterFaultDomain -Name London -Type Site -Description 'Primary DC' -Location 'LON1'
New-ClusterFaultDomain -Name Dublin -Type Site -Location 'DUB1'
Set-ClusterFaultDomain -Name N1,N2 -Parent London
Set-ClusterFaultDomain -Name N3,N4 -Parent Dublin
Get-ClusterFaultDomain
```
Racks and chassis: `-Type Rack` / `-Type Chassis` with nodes as children, racks inside sites. For Storage Spaces Direct,
specify rack/chassis fault domains **before** enabling it: data does not retroactively move when the topology changes.
Windows Server cannot verify that the fault domains you create match the physical world.

## Preferred site
```powershell
(Get-Cluster).PreferredSite = 'London'
```
The Storage Replica stretch cluster guide sets the preferred site this way for the primary site.

## Quorum
Use a witness in a **third** location (cloud witness is the usual choice) so either site can survive losing the other.

## Verify
- [ ] `Get-ClusterFaultDomain` shows the intended hierarchy.
- [ ] `(Get-Cluster).PreferredSite` is as designed.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (fault-domains and the Storage Replica stretch cluster article; repository last commit 2026-10-23) and the New-ClusterFaultDomain reference: four fault domain levels (site, rack, chassis, node), New-ClusterFaultDomain -Type Chassis/Rack/Site, Set-ClusterFaultDomain -Parent/-Location/-Description, specify fault domains before enabling Storage Spaces Direct, Windows Server cannot verify the topology matches reality, (Get-Cluster).PreferredSite. Removed unconfirmed failover affinity, per-group PreferredSite, CrossSiteDelay and CrossSiteThreshold claims and values.

Method: documentation only; no commands were run.
