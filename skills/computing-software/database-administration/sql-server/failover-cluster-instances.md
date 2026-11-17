---
id: computing-software.database-administration.sql-server.failover-cluster-instances
name: failover-cluster-instances
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, failover-cluster-instance, fci, wsfc, shared-storage, storage-spaces-direct, always-on, quorum]
level: advanced
status: docs-checked
description: "Design and operate SQL Server failover cluster instances on WSFC with shared storage: what fails over, storage, quorum, failover sequence and FCI vs AG."
sources:
  - https://learn.microsoft.com/en-us/sql/sql-server/failover-clusters/windows/always-on-failover-cluster-instances-sql-server
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Failover cluster instances (FCI)

**Goal:** instance-level HA: one SQL Server instance that moves between Windows Server Failover Clustering (WSFC)
nodes, with one copy of the data on shared storage.

## What an FCI is
An FCI is a single SQL Server instance installed across WSFC nodes (possibly across subnets). Clients see one
instance on one computer. Only the node that owns the WSFC resource group runs the SQL Server services; the group
holds the network name, IP address, shared disks, the Database Engine and SQL Server Agent services, Analysis Services
if installed, and a file share resource if FILESTREAM is installed. Binaries are installed locally on every node, and
the services are started and stopped by WSFC, not automatically.

## FCI vs availability group
- An FCI protects the whole instance. It must use shared storage, so the storage is a potential single point of
  failure and the FCI depends on the storage layer for data protection. An availability group does not need shared
  storage.
- An FCI can host databases that are in an availability group for database-level disaster recovery.
- Automatic failover from an FCI to other nodes inside an availability group is not supported, so do not couple FCIs
  and standalone nodes in one AG if automatic failover matters; that coupling is fine for DR.

## Storage
Supported: WSFC cluster disks (iSCSI, Fibre Channel, SAN), SMB file shares, Storage Spaces Direct (introduced in Windows Server 2016
Datacenter) and Cluster Shared Volumes. Mounted drives are not supported on clusters that include a SQL
Server installation.

## Requirements and rules
- Nodes need the same hardware class and identical software: OS version and patch level, SQL Server version, patch
  level, components and instance name.
- Each FCI needs a dedicated cluster group with uniquely assigned drive letters, at least one unique IP address, and
  unique virtual server and instance names in the domain.
- Production: use static IP addresses with the FCI virtual IP; do not use DHCP (a lease expiry delays DNS
  re-registration).
- FCI nodes must not be domain controllers.
- Clients connect to the virtual network name, never a node name. In a multi-subnet FCI each subnet gets a virtual IP
  and DNS is updated at failover.

## Failover sequence
1. Unless a hardware or system failure occurs, dirty pages in the buffer cache are written to disk.
2. SQL Server services in the resource group stop on the active node.
3. Resource group ownership moves to another node.
4. The new owner starts its SQL Server services.
5. Connections to the virtual network name are directed to the new active node.

Failover lasts as long as it takes to write remaining dirty pages, so it can be long and unpredictable; indirect
checkpoints throttle dirty pages and make it more predictable and configurable (useful for an RTO).

## Health monitoring
WSFC polls the instance over a dedicated connection for detailed component diagnostics from a system stored
procedure, which distinguishes a heavily loaded system from a failing one (fewer false failovers). The failover
policy is configurable, and diagnostic logs are stored beside the SQL Server error logs and can be opened in the Log
File Viewer to see what led to an automatic failover. See "Failover policy for failover cluster instances".

## Quorum
The FCI stays online only while the WSFC cluster has quorum (a majority of quorum nodes available). If quorum is lost
the whole cluster and the FCI go offline and need manual intervention. See "WSFC quorum modes and voting
configuration".

## Verify
- [ ] Quorum and voting configuration reviewed and documented.
- [ ] Test failover to every node; measure recovery time against the RTO.
- [ ] Applications use the virtual network name; no node names in connection strings.

## Checked
Date: 2026-11-09. Confirmed against "Always On failover cluster instances (SQL Server)" (Microsoft Learn): resource
group contents, failover sequence, storage options, mounted-drive and domain-controller restrictions, requirements,
static IP advice, indirect checkpoints, health monitoring, quorum. Removed (not on the cited pages): the install
walkthrough, `FailureConditionLevel` / `HealthCheckTimeout` details, `sys.dm_os_cluster_nodes` query, rolling-patch
steps, Linux/Pacemaker notes, a cluster-validation checklist.
Method: documentation only; no commands were run.
