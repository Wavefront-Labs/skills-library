---
id: computing-software.systems-network-administration.windows-server.scale-out-file-server-role
name: scale-out-file-server-role
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, scale-out-file-server, sofs, add-clusterscaleoutfileserverrole, cluster-shared-volumes, failover-clustering, smb3]
level: advanced
status: docs-checked
description: "Create a Scale-Out File Server role on CSV for application data: prerequisites, Add-ClusterScaleOutFileServerRole, share creation and SMB client checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/sofs-overview
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/add-clusterscaleoutfileserverrole
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/set-smbpathacl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a Scale-Out File Server role

SOFS is an active-active clustered file server: every node serves the same shares from
CSVs. For application data only (Hyper-V VHDX, SQL databases, VDI user disks), not for
user home folders and office documents (metadata-heavy workloads perform badly).

## Prerequisites
- Failover cluster with CSVs (S2D or shared SAN). File Server role service on all nodes:
  `Install-WindowsFeature FS-FileServer`.
- CNO with Create Computer objects rights so the cluster can create the network name.

## Create
```powershell
Add-ClusterScaleOutFileServerRole -Name SOFS01 -Cluster CLUSTER01
New-Item -Path "$env:SystemDrive\ClusterStorage\Volume1\Shares\VMs" -ItemType Directory
New-SmbShare -Name VMs -Path "$env:SystemDrive\ClusterStorage\Volume1\Shares\VMs" -ScopeName SOFS01 `
  -FullAccess 'CORP\HV-Hosts','CORP\HV-Admins' -ContinuouslyAvailable $true
Set-SmbPathAcl -ShareName VMs -ScopeName SOFS01   # copy the share ACL to the folder
```
- SOFS uses a Distributed Network Name (DNN) so clients can connect to all nodes.
- Hyper-V hosts' computer accounts need access on the share and the folder ACL.

## Hyper-V hosts using SOFS
- `Set-VMHost -VirtualHardDiskPath \\SOFS01\VMs -VirtualMachinePath \\SOFS01\VMs`.

## Verify
```powershell
Get-SmbShare -ScopeName SOFS01 | Select Name,ContinuouslyAvailable,Path
Get-SmbConnection   # on clients
Get-SmbMultichannelConnection
```
- [ ] Clients are registered in `Get-SmbWitnessClient` and spread across nodes.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (sofs-overview, repository last commit 2026-10-23) and the Windows Server 2025 PowerShell reference: Scale-Out File Server is for application data (Hyper-V, SQL Server), not information-worker workloads with many metadata operations; Distributed Network Name; Add-ClusterScaleOutFileServerRole parameters; New-SmbShare -ScopeName and -ContinuouslyAvailable; Set-SmbPathAcl -ScopeName/-ShareName; ReFS recommended with Storage Spaces Direct. Removed unconfirmed claims about -CachingMode None, SMB dialect, DNS record layout, Kerberos delegation and the Hyper-V host permission specifics.

Method: documentation only; no commands were run.
