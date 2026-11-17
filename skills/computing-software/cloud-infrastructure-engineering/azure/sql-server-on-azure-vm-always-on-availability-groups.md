---
id: computing-software.cloud-infrastructure-engineering.azure.sql-server-on-azure-vm-always-on-availability-groups
name: sql-server-on-azure-vm-always-on-availability-groups
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, sql-high-availability, sql-vm-availability-group, always-on-ag, wsfc, distributed-network-name]
level: sme
status: docs-checked
description: "Design SQL Server Always On availability groups on Azure VMs: multi-subnet vs load balancer vs DNN listener, quorum, relaxed cluster heartbeat settings."
sources: ["https://learn.microsoft.com/azure/azure-sql/virtual-machines/windows/availability-group-overview", "https://learn.microsoft.com/azure/azure-sql/virtual-machines/windows/availability-group-manually-configure-multi-subnet-multiple-regions", "https://learn.microsoft.com/azure/azure-sql/virtual-machines/windows/availability-group-distributed-network-name-dnn-listener-configure", "https://learn.microsoft.com/azure/azure-sql/virtual-machines/windows/hadr-cluster-best-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server AGs on Azure VMs

**Goal:** highly available SQL Server on IaaS with fast, reliable listener failover.

## Design
- **VM redundancy**: put replicas in the same availability set or in different availability zones; a VM cannot be in both. Zones protect against a whole-datacenter failure but add network latency between replicas, which can delay the primary and raise the chance of data loss on an unplanned failover. Test under load.
- **Multi-subnet** (VMs in several subnets of one virtual network): preferred. The listener gets an IP in each subnet and needs no Azure Load Balancer or DNN. Azure does not support ARP/GARP, which is why a single subnet needs one of the options below.
- **Single subnet**: use a virtual network name (VNN) listener with an Azure Load Balancer (frontend IP for the listener, a probe port, Direct Server Return enabled, internal or external type), or a **distributed network name (DNN)** listener. DNN needs SQL Server 2019 CU8 or later, 2017 CU25 or later, or 2016 SP3 or later, on Windows Server 2016 or later. DNN fails over faster because no load balancer has to detect the failure.
- With a DNN, open transactions against a failing-over database roll back and need a manual reconnect; connections to a failing-over database close but others on the primary stay open.
- Each AG or FCI on the same cluster needs its own connection point.
- Use a single NIC per cluster node; ignore the cluster validation warning about one network.
- **Quorum**: use a cloud witness whenever possible (Windows Server 2016+); disk witness needs Azure Shared Disks; file share witness when the others are unavailable. Use three or more odd votes and do not give DR regions votes.
- A Basic AG has one secondary and no read access, so a database-mirroring style connection string (`Failover Partner`) can replace the listener.

## Clients
- Put `MultiSubnetFailover=True` in the connection string (also for VNN and single-subnet clusters); a DNN connection string also needs the DNN port number, for example `DataSource=DNN_Listener,6789;MultiSubnetFailover=True`.
- If a client cannot use MultiSubnetFailover, you may need `RegisterAllProvidersIP = 0` and `HostRecordTTL = 300`, at the cost of more DNS queries.

## Relaxed cluster settings (Windows Server 2012 and later)
Defaults assume tuned on-premises networks; the heartbeat uses UDP 3343. Microsoft recommends: `SameSubnetDelay` 1 second, `SameSubnetThreshold` 40 heartbeats, `CrossSubnetDelay` 1 second, `CrossSubnetThreshold` 40 heartbeats.
```powershell
(get-cluster).SameSubnetThreshold = 40
(get-cluster).CrossSubnetThreshold = 40
```
- Lease timeout must be below 2 x SameSubnetThreshold x SameSubnetDelay: start at 40 seconds and do not exceed 80 with the relaxed values. Set max failures in a specified period to 6.
- If a health-probe or listener port is in the dynamic range 49,152-65,536, add an exclusion, for example `netsh int ipv4 add excludedportrange tcp startport=59999 numberofports=1 store=persistent`.

## Gotchas
- Without `MultiSubnetFailover=True`, clients may not reconnect promptly after failover.
- The database mirroring endpoint can use any available port; examples often use 5022.

## Verify
- [ ] The AG shows healthy synchronization on every replica and a test failover reconnects clients.

## Checked

Method: docs-checked 2026-11-09 against the Learn pages availability-group-overview and hadr-cluster-best-practices (read in the relevant sections), the DNN listener page and the multi-subnet multiple-regions page (keyword checks). Corrected the cluster threshold values (the draft's 15/20/1000 are not in Microsoft's table). Removed unconfirmed: probe port 59999 as the LB default, New-Cluster and CREATE LISTENER samples, `az sql vm group`, licensing note, dbatools advice and the 30 second failover target.
