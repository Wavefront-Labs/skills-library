---
id: computing-software.database-administration.sql-server.wsfc-quorum-and-witness
name: wsfc-quorum-and-witness
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, always-on, availability-group, wsfc-quorum, cloud-witness, file-share-witness, node-weight]
level: advanced
status: docs-checked
description: "Configure Windows Server Failover Cluster quorum for SQL Server AGs and FCIs: witness choice, dynamic quorum, node votes across sites, and forcing quorum after a disaster."
sources:
  - https://learn.microsoft.com/en-us/sql/sql-server/failover-clusters/windows/wsfc-quorum-modes-and-voting-configuration-sql-server
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/manage-cluster-quorum
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/deploy-cloud-witness
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WSFC quorum and witness configuration

Availability groups and FCIs depend on the Windows cluster staying in quorum: if the cluster
loses quorum, AG replicas go to RESOLVING and the databases become unavailable, even on
healthy nodes.

## Witness choice
Microsoft recommends always configuring a witness on Windows Server 2012 R2 and later; the cluster then manages the witness vote with Dynamic Quorum.
| Witness | Use |
|---|---|
| Cloud Witness (Azure blob) | needs an Azure Standard general purpose v2 storage account and outbound HTTPS (port 443) from every node to the Azure blob endpoint |
| File Share Witness | an SMB share on a third site/server (not on a cluster node) |
| Disk Witness | shared-storage clusters (FCI) in one site |
```powershell
Set-ClusterQuorum -CloudWitness -AccountName "stwitnessprod" -AccessKey "<key>"
Set-ClusterQuorum -FileShareWitness "\\witness01\clusterwitness"
Get-ClusterQuorum
```

## Votes in multi-site setups
DR-site nodes that should never cause or block failover decisions can have their vote removed:
```powershell
(Get-ClusterNode -Name "SQLDR01").NodeWeight = 0
Get-ClusterNode | Format-Table Name, State, NodeWeight, DynamicWeight
```
Keep the majority of votes (plus witness) in the primary site, or place the witness in a
third location so either site can win.
**Dynamic quorum** adjusts node votes as nodes fail sequentially and manages the witness vote.

## Forcing quorum after a disaster
If the primary site is lost and the DR nodes have no majority, quorum must be forced and the AG
failed over with possible data loss. Follow the current Microsoft procedure for forcing quorum
and for `FORCE_FAILOVER_ALLOW_DATA_LOSS`, and expect to resume and reseed replicas when the old
site returns.

## Health settings that cause false failovers
Cluster heartbeat thresholds and AG health-check settings that are too tight cause failovers on
transient network blips; check the current Microsoft guidance for your platform before changing them.

## Gotchas
- Witness share must be reachable from all nodes and not hosted on a node in the cluster.
- Losing the witness is not an outage by itself but reduces tolerance; alert on it.

## Checked
2026-11-01. Confirmed on Learn: witness recommendation and Dynamic Quorum (Windows Server 2012 R2 and later), Cloud Witness requirements (Standard general purpose v2 account, HTTPS port 443), NodeWeight setting in the SQL Server quorum page. Removed: forced-quorum commands, heartbeat threshold names and values, CNO permission, Linux Pacemaker claim, default-since-2012-R2 and third-site claims (not stated in these pages).
Method: documentation only; no commands were run.

## Verify
`Get-ClusterQuorum` shows the witness; in a test, stop nodes one by one and confirm the cluster
stays up as designed; validation report (`Test-Cluster`) has no quorum warnings.
