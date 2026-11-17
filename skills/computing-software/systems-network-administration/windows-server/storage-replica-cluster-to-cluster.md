---
id: computing-software.systems-network-administration.windows-server.storage-replica-cluster-to-cluster
name: storage-replica-cluster-to-cluster
category: computing-software
field: systems-network-administration
product: windows-server
tags: [storage-replica, cluster-to-cluster-replication, new-srpartnership, failover-clustering, grant-sraccess]
level: advanced
status: docs-checked
description: "Replicate between two failover clusters with Storage Replica: Grant-SRAccess both ways, Test-SRTopology, partnership creation on CSV or role disks, and failover."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/cluster-to-cluster-storage-replication
  - https://learn.microsoft.com/en-us/powershell/module/storagereplica/grant-sraccess
  - https://learn.microsoft.com/en-us/powershell/module/storagereplica/set-srpartnership
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Replica cluster-to-cluster

Two independent clusters (often S2D), one per site; Storage Replica copies volumes between them. Failover is
manual: you reverse direction and bring roles online at the DR cluster.

## Prepare
- Same size data volumes and log volumes (log on SSD; the log defaults to 8 GB and the log volume should be at least 10 GB; size it to absorb outages) on both clusters.
- Both clusters Windows Server Datacenter; Windows Server 2019 or later Standard works only for a single volume up to 2 TB.
- Firewall: ICMP, SMB 445 (plus 5445 for SMB Direct) and WS-Man 5985 in both directions between all nodes.
- Network between sites with enough bandwidth for the write workload; synchronous replication needs an average round trip of 5 ms or less, asynchronous has no latency recommendation.

## Grant access both ways
```powershell
Grant-SRAccess -ComputerName CL1-N1 -Cluster CL2
Grant-SRAccess -ComputerName CL2-N1 -Cluster CL1
```

## Test (on a node of each side, with workload running)
```powershell
Test-SRTopology -SourceComputerName CL1 -SourceVolumeName $env:SystemDrive\ClusterStorage\Vol1 -SourceLogVolumeName L: `
  -DestinationComputerName CL2 -DestinationVolumeName $env:SystemDrive\ClusterStorage\Vol1 -DestinationLogVolumeName L: `
  -DurationInMinutes 30 -ResultPath <REPORT_DIR>
```
The HTML report (TestSrTopologyReport) checks the requirements and reports measured latency and write I/O; with no write load it is not useful.

## Create the partnership
```powershell
New-SRPartnership -SourceComputerName CL1 -SourceRGName RG-CL1 -SourceVolumeName $env:SystemDrive\ClusterStorage\Vol1 -SourceLogVolumeName L: `
  -DestinationComputerName CL2 -DestinationRGName RG-CL2 -DestinationVolumeName $env:SystemDrive\ClusterStorage\Vol1 -DestinationLogVolumeName L: `
  -ReplicationMode Asynchronous
```
The destination volume goes offline to users (it's a replica). Watch `Get-SRGroup` and the StorageReplica Admin events (1237 shows progress, 1215 block copy completed).

## Failover
```powershell
Set-SRPartnership -NewSourceComputerName CL2 -SourceRGName RG-CL2 -DestinationComputerName CL1 -DestinationRGName RG-CL1
```
Cluster-to-cluster failover needs manual intervention: bring VMs/roles online on CL2 yourself.

## Verify
- [ ] Partnership healthy; failover and failback rehearsed with timings documented.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs StorageReplica cmdlet pages. Confirmed Grant-SRAccess in both directions, Test-SRTopology report, 8 GB default log with 10 GB minimum volume, Standard limits, ports, 5 ms synchronous guidance, Set-SRPartnership -NewSourceComputerName reversal and manual failover. Corrected the initial-sync event: 1215 is block copy completed, 1237 is progress.

Method: documentation only; no commands were run.
