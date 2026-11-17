---
id: computing-software.systems-network-administration.windows-server.storage-replica-stretch-cluster
name: storage-replica-stretch-cluster
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-replica, stretch-cluster, failover-clustering, sites, site-awareness, asymmetric-storage, multi-site-cluster]
level: advanced
status: docs-checked
description: "Build a stretch failover cluster with Storage Replica between two sites: site fault domains, asymmetric storage, replicating cluster disks and witness placement."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/stretch-cluster-replication-using-shared-storage
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/fault-domains
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/storage-replica-frequently-asked-questions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stretch cluster with Storage Replica

One failover cluster spanning two sites, each site with its own shared storage (SAN,
JBOD or iSCSI), Storage Replica copying the disks between sites. Workloads fail over
automatically between sites.

## Design
- Each site: same number of nodes (or at least one), storage visible only to that site's
  nodes (asymmetric storage).
- Configure a file share witness or cloud witness so quorum survives the loss of a site (the docs cite Cloud (Azure) witness as an option).
- Synchronous replication needs an average of about 5 ms RTT or less between sites; asynchronous has no latency recommendation.
- Windows Server 2016 Datacenter or later (Standard from 2019 for a single volume up to 2 TB); storage must support Persistent Reservation.
- Expect storage errors from cluster validation because of the asymmetric storage.
- Data and log disks per replication group, same sizes in both sites.

## Configure sites
```powershell
New-ClusterFaultDomain -Name Seattle -Type Site -Location 'Seattle DC1'
New-ClusterFaultDomain -Name Redmond -Type Site -Location 'Redmond DC2'
Set-ClusterFaultDomain -Name NODE1 -Parent Seattle; Set-ClusterFaultDomain -Name NODE2 -Parent Seattle
Set-ClusterFaultDomain -Name NODE3 -Parent Redmond; Set-ClusterFaultDomain -Name NODE4 -Parent Redmond
(Get-Cluster).PreferredSite = 'Seattle'
```

## Replicate cluster disks
Test with `Test-SRTopology` against nodes in each site, then add only the source data disk as a CSV (the destination disk stays as available storage):
```powershell
Add-ClusterSharedVolume -Name 'Cluster Disk 1'     # source data disk as CSV for Hyper-V workloads
New-SRPartnership -SourceComputerName NODE1 -SourceRGName RG01 -SourceVolumeName '<SystemDrive>\ClusterStorage\Volume1' `
  -SourceLogVolumeName L: -DestinationComputerName NODE3 -DestinationRGName RG02 `
  -DestinationVolumeName F: -DestinationLogVolumeName L:
```
Or use Failover Cluster Manager: right-click the disk, Replication, Enable.

## Behaviour
- Move the source CSV to a node in the other site (Move Storage in Failover Cluster Manager, or `Move-ClusterSharedVolume`) for a planned site move; the replication direction follows.
- A full site loss: the surviving site keeps quorum through the witness. Automatic failover can be prevented only with PowerShell (NodeWeight and forced quorum), which the docs advise against.

## Verify
- [ ] `Get-ClusterFaultDomain` shows sites with correct nodes.
- [ ] `(Get-SRGroup).Replicas.ReplicationStatus` ContinuouslyReplicating.
- [ ] Planned role move to the other site succeeds and replication reverses.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs StorageReplica cmdlet pages. Confirmed New-ClusterFaultDomain/Set-ClusterFaultDomain site setup and (Get-Cluster).PreferredSite, asymmetric storage, file share or cloud witness, the 5 ms synchronous guidance, adding only the source disk as a CSV, New-SRPartnership with a ClusterStorage source path, the Failover Cluster Manager Replication > Enable route, and planned site moves through Move-ClusterSharedVolume. Removed the unconfirmed third-site witness and automatic-reversal wording.

Method: documentation only; no commands were run.
