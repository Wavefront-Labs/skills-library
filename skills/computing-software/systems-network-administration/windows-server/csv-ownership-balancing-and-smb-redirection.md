---
id: computing-software.systems-network-administration.windows-server.csv-ownership-balancing-and-smb-redirection
name: csv-ownership-balancing-and-smb-redirection
category: computing-software
field: systems-network-administration
product: windows-server
tags: [scale-out-file-server, csv-ownership-balancing, cluster-shared-volumes, smb-witness, sofs]
level: advanced
status: docs-checked
description: "Keep Scale-Out File Server and CSV ownership balanced: automatic CSV balancer, Move-ClusterSharedVolume, SMB client redirection and diagnosing redirected I/O."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/failover-cluster-csvs
  - https://learn.microsoft.com/en-us/powershell/module/smbwitness/get-smbwitnessclient
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# CSV ownership balancing and SMB client redirection

Each CSV has a **coordinator node** (owner) handling metadata. SOFS clients connect to any node; the SMB witness
service helps clients reach the node that owns the CSV holding their share, avoiding extra hops.

## Check balance
```powershell
Get-ClusterSharedVolume | Select Name,OwnerNode,State
Get-ClusterSharedVolumeState | Select Name,Node,StateInfo,FileSystemRedirectedIOReason,BlockRedirectedIOReason
```
Healthy: owners spread across nodes; `StateInfo` = Direct on all nodes.

## Automatic balancing
Since Windows Server 2012 R2, CSV ownership is distributed across the nodes by the number of CSVs each owns, and is
rebalanced automatically on events such as CSV failover.

Manual move during maintenance or after imbalance, ideally in a quiet period:
```powershell
Move-ClusterSharedVolume -Name 'Cluster Virtual Disk (Vol1)' -Node N2
```

## SMB client redirection
```powershell
Get-SmbWitnessClient | Select ClientName,FileServerNodeName,WitnessNodeName,NetworkName,ShareName
```
Shows which node each client is connected to and which node hosts its witness registration.

## Redirected I/O
`FileSystemRedirected` or `BlockRedirected` means a node sends I/O over the cluster network to the owner instead of
direct to storage: a large performance hit. File system redirection is per volume (for example while a backup
application takes CSV snapshots); block redirection happens at block level (for example lost storage connectivity).
CSVs formatted with ReFS on a SAN always run redirected. The state output shows the reason.

## Verify
- [ ] Owners balanced, StateInfo Direct everywhere, witness clients connected to owners.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (failover-cluster-csvs, repository last commit 2026-10-23) and the SmbWitness PowerShell reference: CSV ownership is distributed by the number of CSVs per node and rebalanced automatically since Windows Server 2012 R2, Get-ClusterSharedVolumeState reports per-node state and redirection reason, redirected I/O modes, ReFS on SAN always redirected, Get-SmbWitnessClient fields. Removed the unconfirmed CsvBalancer property, the pause-duration claim and the extra redirection reasons.

Method: documentation only; no commands were run.
