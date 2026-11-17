---
id: computing-software.systems-network-administration.windows-server.continuously-available-smb-shares
name: continuously-available-smb-shares
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, scale-out-file-server, sofs, continuous-availability, smb-transparent-failover, persistent-handles, hyper-v-over-smb, sql-over-smb]
level: advanced
status: docs-checked
description: "Configure continuously available SMB 3 shares for Hyper-V and SQL Server: persistent handles, transparent failover, permissions, multichannel and SMB Direct."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-feature-descriptions.md
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/file-server-smb-overview.md
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/new-smbshare
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/set-smbpathacl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Continuously available shares for Hyper-V and SQL

Continuous availability (CA) gives persistent handles: if the node serving a client
fails, the handle is reclaimed on another node within seconds and the app (Hyper-V,
SQL) sees a pause, not an error.

## Create
```powershell
New-SmbShare -Name SQLData -Path "$env:SystemDrive\ClusterStorage\Volume2\SQLData" -ScopeName SOFS01 `
  -ContinuouslyAvailable $true -FullAccess 'CORP\sqlsvc-gmsa$','CORP\SQL-Admins' -FolderEnumerationMode Unrestricted
Set-SmbPathAcl -ShareName SQLData
Get-SmbShare SQLData | Select ContinuouslyAvailable,CachingMode
```
Shares on a clustered file server are created with the Continuous Availability property by default; shares on CSV volume paths also get SMB Scale-Out. Down-level clients (before Windows 8 / Server 2012) can connect but do not get transparent failover.

## SQL Server
- Service account (gMSA) Full Control on share and NTFS.
- Database files: `CREATE DATABASE ... ON (FILENAME = '\\SOFS01\SQLData\db.mdf')`.
- Use an SMB 3.0+ client (Windows 8 / Windows Server 2012 or later).

## Hyper-V
- Host computer accounts plus Hyper-V admins Full Control.
- Live migration between hosts keeps VMs on the share (no storage move).

## Performance
- SMB Multichannel automatically uses multiple NICs; check
  `Get-SmbMultichannelConnection`.
- SMB Direct (RDMA) for low latency: `Get-NetAdapterRdma`, `Get-SmbClientNetworkInterface | ? RdmaCapable`.
- SMB encryption costs CPU; enable it only where required. SMB Direct supports encryption from Windows Server 2022, and AES-128-GCM is the default cipher for SMB 3.1.1.

## Test failover
Move the share owner / drain a node while a VM runs IO: expect a short pause, no
crash. `Get-SmbOpenFile | Select ClientComputerName,Path,ContinuouslyAvailable` shows
persistent handles.

## Verify
- [ ] Handles show ContinuouslyAvailable True; planned node drain caused no VM/SQL errors.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- SMB Transparent Failover (smb-feature-descriptions): needs a cluster of 2+ nodes passing validation, shares created with the CA property (the default), CSV paths for Scale-Out, Windows 8 / Server 2012 or later clients; down-level clients connect without transparent failover.
- New-SmbShare parameters -ContinuouslyAvailable, -ScopeName, -FullAccess, -FolderEnumerationMode (Unrestricted is the default) and Set-SmbPathAcl (copies the share ACL to the folder) confirmed in the cmdlet references.
- AES-128-GCM default for 3.1.1 and SMB Direct encryption from 2022 confirmed. Removed unconfirmed details: the general-file-server performance warning, the SQL trace-flag remark and the AES-GCM acceleration claim.

Method: documentation only; no commands were run.
