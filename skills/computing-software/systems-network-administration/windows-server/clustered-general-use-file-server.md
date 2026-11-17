---
id: computing-software.systems-network-administration.windows-server.clustered-general-use-file-server
name: clustered-general-use-file-server
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, scale-out-file-server, sofs, clustered-file-server, add-clusterfileserverrole, failover-clustering, file-server, high-availability]
level: practitioner
status: docs-checked
description: "Create a highly available general-use clustered file server for user data: Add-ClusterFileServerRole, scoped shares, ABE, why to avoid continuous availability, and failover."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/sofs-overview
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/deploy-two-node-clustered-file-server
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/add-clusterfileserverrole
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# General-use clustered file server

For user home folders, department shares and other information-worker data. A general-use clustered file server is
online on one node at a time (active-passive); run several roles to spread load.

## Create
```powershell
Install-WindowsFeature FS-FileServer   # all nodes
Add-ClusterFileServerRole -Name FS01 -Storage 'Cluster Disk 3' -StaticAddress 10.0.0.45 -Cluster CLUSTER01
New-SmbShare -Name Finance -Path '<vol>:\Shares\Finance' -ScopeName FS01 -FolderEnumerationMode AccessBased `
  -ChangeAccess 'CORP\Finance-RW' -ReadAccess 'CORP\Finance-RO' -ContinuouslyAvailable $false
```
- `-ScopeName` is the New-SmbShare parameter for shares on a failover cluster file server resource; use the clustered
  role name.
- The role's VCO is created by the CNO in AD, so the CNO needs Create Computer objects rights (see the CNO skill).

## CA or not
Leave continuous availability **off** for this workload. With CA shares, home directories, Folder Redirection, Offline
Files and Roaming User Profiles generate many writes that must be committed immediately, which reduces performance,
and CA shares are incompatible with File Server Resource Manager.

## Companions
General-use clusters support features Scale-Out File Server does not: BranchCache, Data Deduplication, DFS Replication,
DFS Namespaces as a root server, and Dynamic Access Control.

## Failover test
```powershell
Move-ClusterGroup FS01 -Node NODE2
Get-SmbShare -ScopeName FS01
```

## Verify
- [ ] Shares listed with `Get-SmbShare -ScopeName FS01` after moving to each node.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (sofs-overview and the two-node clustered file server article; repository last commit 2026-10-23) and the PowerShell reference for Add-ClusterFileServerRole (Name, Storage, StaticAddress, Cluster) and New-SmbShare (ScopeName, FolderEnumerationMode, ContinuouslyAvailable): general-use file servers are active-passive, continuous availability is a poor fit for home directories and incompatible with FSRM, and the feature table (BranchCache, Data Deduplication, DFS Replication and DFS namespace roots work on general-use clusters, not on Scale-Out File Server). Removed unconfirmed claims about Available Storage, Office reconnect behaviour, FSRM and shadow copy placement.

Method: documentation only; no commands were run.
