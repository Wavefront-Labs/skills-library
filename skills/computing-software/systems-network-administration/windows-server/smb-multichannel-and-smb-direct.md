---
id: computing-software.systems-network-administration.windows-server.smb-multichannel-and-smb-direct
name: smb-multichannel-and-smb-direct
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, file-server, smb-multichannel, smb-direct, rdma, smb-performance]
level: advanced
status: docs-checked
description: "Get the most from SMB Multichannel and SMB Direct: requirements, constraining interfaces, verifying connections, and why throughput may not scale."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-direct.md
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/smb-multichannel
  - https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-feature-descriptions.md
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/new-smbmultichannelconstraint
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SMB Multichannel and SMB Direct

**Multichannel** (SMB 3.0+, on by default) opens several TCP connections over multiple NICs or one RSS NIC, giving
bandwidth aggregation and NIC failover. **SMB Direct** runs SMB over RDMA capable network adapters for low
latency and low CPU.

## Requirements for multichannel to kick in
- Both ends SMB 3.0+ (Windows 8/2012+).
- Multiple NICs, or one NIC with RSS, or RDMA-capable NICs.
- On failover clusters (Windows Server 2016 and later), multiple NICs on the same subnet are recognised automatically and SMB Multichannel is enabled with no extra configuration.

## Check
```powershell
Get-SmbMultichannelConnection                 # on the client: client/server IPs, RSS/RDMA capable
Get-SmbClientNetworkInterface | ft FriendlyName,LinkSpeed,RssCapable,RdmaCapable
Get-SmbServerNetworkInterface -CimSession FS01
Get-SmbConnection | ft ServerName,ShareName,Dialect
```
No rows in `Get-SmbMultichannelConnection` = single connection.

## Constrain which NICs are used
```powershell
New-SmbMultichannelConstraint -ServerName FS01 -InterfaceAlias 'SMB1','SMB2'    # client side
Set-SmbClientConfiguration -EnableMultiChannel $true
```
Use for clusters/Hyper-V hosts so SMB avoids the management NIC.

## Why it does not scale
- RSS disabled or only one queue on the NIC; check `Get-NetAdapterRss`.
- SMB encryption costs CPU. From Windows Server 2022 and Windows 11, SMB Direct supports encryption (data is encrypted before direct placement); earlier versions lost direct data placement when encryption was on.

## Verify
- [ ] Multichannel connections show expected interfaces; a large copy uses all NICs
      and disconnecting one cable or disabling one adapter mid-copy does not stop the transfer.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- Multichannel is SMB 3.0, on by default with nothing to install; SMB Direct supports encryption from Windows Server 2022 and Windows 11 (smb-direct and smb-feature-descriptions pages).
- New-SmbMultichannelConstraint takes -ServerName with -InterfaceAlias or -InterfaceIndex; Get-SmbClientNetworkInterface exposes RssCapable, RdmaCapable and LinkSpeed; the Get-SmbServerNetworkInterface, Get-SmbMultichannelConnection and Get-NetAdapterRss cmdlet pages exist.
- Cluster simplified multichannel (same-subnet NICs recognised automatically) from the failover-clustering smb-multichannel page; the cable-pull failover test comes from the smb-direct verification steps.
- Removed unconfirmed details: the RDMA transport list, same-speed NIC rule, NIC team counting, copy-tool and diskspd advice, mixed-speed behaviour and Task Manager check.

Method: documentation only; no commands were run.
