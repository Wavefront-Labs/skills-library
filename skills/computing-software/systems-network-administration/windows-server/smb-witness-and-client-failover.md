---
id: computing-software.systems-network-administration.windows-server.smb-witness-and-client-failover
name: smb-witness-and-client-failover
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, scale-out-file-server, sofs, smb-witness, get-smbwitnessclient, move-smbwitnessclient, transparent-failover, smb-scale-out]
level: advanced
status: docs-checked
description: "Understand and manage the SMB Witness service for clustered file servers: fast client failover notification, Get-SmbWitnessClient, Move-SmbWitnessClient rebalancing."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/smbwitness/get-smbwitnessclient
  - https://learn.microsoft.com/en-us/powershell/module/smbwitness/move-smbwitnessclient
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/sofs-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMB Witness and client failover

When a client connects to a clustered file server (SOFS or general use), it registers with the SMB witness service on a
different node. If the serving node fails, the witness notifies the client so it can reconnect to a surviving node
without waiting for a network time-out.

## Inspect
```powershell
Get-SmbWitnessClient | Select ClientName,FileServerNodeName,WitnessNodeName,NetworkName,ShareName
```
Each row is a witness registration; a client can have several (one per resource). Empty output for a clustered share
means clients are not registered, for example because they connect by node name or IP instead of the clustered name.

## Move a SOFS client
```powershell
Move-SmbWitnessClient -ClientName HV05 -DestinationNode NODE3
```
Only SMB connections to a Distributed Network Name can be moved, which is why SOFS clients should always use the SOFS name.

## Gotchas
- Connect clients to the clustered name, not a node name or IP.
- Always test failover with a node drain while a client runs I/O.

## Verify
- [ ] Every Hyper-V/SQL client appears in `Get-SmbWitnessClient` with a witness on a different node than the file server node.
- [ ] Node drain test: client I/O resumes without errors.

## Checked

Confirmed 2026-10-25 against the SmbWitness PowerShell reference (Windows Server 2025 set): Get-SmbWitnessClient retrieves SMB witness client registrations with witness servers in a failover cluster and shows Client Computer Name, Witness Node Name, File Server Node Name, Network Name and Share Name; Move-SmbWitnessClient requires -ClientName and -DestinationNode and only connections to a Distributed Network Name can be moved. Removed the unconfirmed TCP timeout figures, State values, RPC firewall ports, service name and OS requirement details.

Method: documentation only; no commands were run.
