---
id: computing-software.cloud-infrastructure-engineering.azure.sql-managed-instance-failover-groups
name: sql-managed-instance-failover-groups
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, sql-high-availability, mi-failover-group, managed-instance, geo-replication, failover-group-listener]
level: sme
status: docs-checked
description: "Set up failover groups for Azure SQL Managed Instance: network prerequisites, DNS zone, listener endpoints, failover policy, planned and forced failover."
sources: ["https://learn.microsoft.com/azure/azure-sql/managed-instance/failover-group-sql-mi", "https://learn.microsoft.com/azure/azure-sql/managed-instance/failover-group-configure-sql-mi", "https://learn.microsoft.com/azure/azure-sql/managed-instance/failover-group-standby-replica-how-to-configure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Managed Instance failover groups

**Goal:** geo-replicate all user databases of a Managed Instance and fail over with one connection string.

## Prerequisites
- Secondary MI in another region with the same service tier, compute tier and compute size as the primary, created with **DNS zone partner** = primary (`az sql mi create --dns-zone-partner`) so both share the DNS zone.
- Connectivity between the two VNets (global VNet peering or VPN gateways), with the ports in the configure article allowed in the NSGs: TCP **5022** and the **11000-11999** range.
- Same service tier, compute tier and size apply to both replicas of the group.

## Create
```bash
az sql instance-failover-group create -g rg -n fog-mi --mi mi-weu --partner-mi mi-neu \
  --partner-resource-group rg-dr --failover-policy Manual --secondary-type Standby
```
- **Listener endpoints**: read-write `<fog-name>.<dnszone>.database.windows.net` and read-only `<fog-name>.secondary.<dnszone>.database.windows.net`. Apps use these, never the instance names.
- `--secondary-type Standby` marks the secondary as a passive replica for disaster recovery only (the default is `Geo`).
- Failover policy: Microsoft-managed automatic failover (the grace period can't be set below one hour) or **Manual** (customer-managed).

## Failover
```bash
az sql instance-failover-group set-primary -g rg-dr -n fog-mi --location northeurope            # planned, no data loss
az sql instance-failover-group set-primary -g rg-dr -n fog-mi --location northeurope --allow-data-loss   # forced
```
Planned failover synchronises first; forced failover (`--allow-data-loss`) may lose recent transactions because replication is asynchronous.

## Gotchas
- Instance-level objects (logins in `master`, SQL Agent jobs in `msdb`) are not replicated: create them on both instances.
- All user databases on the instance are included in the group; check the overview article for the one-group-per-instance-pair rule.
- Initial seeding of large databases takes time; wait for replication to be healthy before a drill.

## Verify
- [ ] `az sql instance-failover-group show ... --query "{role:replicationRole, state:replicationState}"`.
- [ ] App connects through the listener before and after a planned failover drill.

## Checked
2026-10-27. Confirmed on Microsoft Learn: failover-group-sql-mi (same service tier, compute tier and size, one failover group, grace period not below one hour, Microsoft-managed vs customer-managed policy),
failover-group-configure-sql-mi (ports 5022 and 11000-11999, set-primary), CLI reference for `az sql instance-failover-group` (--mi, --partner-mi, --partner-resource-group, --failover-policy,
--secondary-type Standby/Geo default Geo, --grace-period, --allow-data-loss, set-primary --location) and `az sql mi` (--dns-zone-partner).
Removed: same collation and time zone requirement, licence-free claim, `sys.dm_hadr_physical_seeding_stats` monitoring tip, old-primary-rejoins claim, "run against the secondary region" claim.

Method: documentation only; no commands were run.
