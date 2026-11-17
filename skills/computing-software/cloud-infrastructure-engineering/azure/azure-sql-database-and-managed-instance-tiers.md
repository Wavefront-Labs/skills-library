---
id: computing-software.cloud-infrastructure-engineering.azure.azure-sql-database-and-managed-instance-tiers
name: azure-sql-database-and-managed-instance-tiers
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-sql, sql-database, sql-managed-instance, sql-server-on-vm, vcore, dtu, general-purpose, business-critical, hyperscale, serverless, elastic-pools, instance-pools, zone-redundant, max-size, log-rate, tempdb, maintenance-window, sql-auditing, point-in-time-restore, ltr, long-term-retention, geo-restore, sql-ledger, sql-pricing, azure-hybrid-benefit]
level: practitioner
status: docs-checked
description: "Choose and size Azure SQL: SQL DB vs Managed Instance vs SQL on VM, vCore tiers (GP/BC/Hyperscale/serverless), elastic pools, zone redundancy, maintenance windows, PITR/LTR."
sources: ["https://learn.microsoft.com/en-us/azure/azure-sql/database/service-tiers-sql-database-vcore", "https://learn.microsoft.com/en-us/azure/azure-sql/database/serverless-tier-overview", "https://learn.microsoft.com/en-us/azure/azure-sql/database/automated-backups-overview", "https://learn.microsoft.com/en-us/azure/azure-sql/database/maintenance-window", "https://learn.microsoft.com/en-us/azure/azure-sql/database/connectivity-architecture", "https://learn.microsoft.com/en-us/cli/azure/sql/db"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure SQL — pick the deployment and tier that fits, not the one on the first page

**Goal:** a database platform choice you can defend (DB vs MI vs VM), a tier sized on
log rate and IOPS from the limits tables, not just vCores, backups you did not have to
configure, and no surprise resource-governance throttling in production.

## 1. Deployment option
| | **SQL Database** | **SQL Managed Instance** | **SQL Server on VM** |
|---|---|---|---|
| Scope | single DB (or elastic pool) | near-full instance surface: cross-database queries, SQL Agent, linked servers | everything, including OS access |
| Network | public endpoint + firewall, or private endpoint | VNet-injected (delegated subnet) | your VNet |
| HA | built in | built in | you build AG/FCI |
| Lift-and-shift from on-prem | app changes likely | native backup/restore (.bak) | as-is |
Rule: SQL DB for new cloud apps and SaaS; MI for migrating instance-dependent estates; VM only when a feature or licensing demands it. Read the feature-comparison page for the current gaps.

## 2. Tiers (vCore model)
| Tier | Storage | Pick for |
|---|---|---|
| **General Purpose** | remote storage, read IO latency 5-10 ms; SQL DB data size 1 GB to 4 TB | most workloads |
| **Business Critical** | local SSD, read IO latency 1-2 ms; 1 GB to 4 TB; built-in Read Scale-Out gives one free read-only replica | IO-latency-sensitive OLTP |
| **Hyperscale** | data size 10 GB to 128 TB, grows automatically (you do not set max size); up to 30 named replicas | large DBs, rapid scale, read scale-out |
| **Serverless** (General Purpose and Hyperscale compute tier) | autoscaling between min and max vCores, billed per second, auto-pause when inactive | dev/test, spiky |
```bash
az sql server create -g rg -n sql-prod-uks -l uksouth --enable-ad-only-auth --external-admin-principal-type Group --external-admin-name sg-sql-admins --external-admin-sid <group-object-id>
az sql db create -g rg -s sql-prod-uks -n orders --edition GeneralPurpose --family Gen5 --capacity 8 --compute-model Provisioned --zone-redundant true --backup-storage-redundancy Zone --max-size 1024GB --license-type BasePrice
az sql elastic-pool create -g rg -s sql-prod-uks -n pool-saas --edition GeneralPurpose --family Gen5 --capacity 16 --db-max-capacity 4 --db-min-capacity 0 --max-size 2048GB
az sql mi create -g rg -n sqlmi-prod --subnet <delegated-subnet-id> --tier GeneralPurpose --family Gen5 --capacity 8 --storage 512GB --admin-user <admin> --zone-redundant true
```
- **Elastic pools** when many DBs have uncorrelated peaks (SaaS per-tenant DBs): size the pool for the combined load and cap per database with `--db-max-capacity`.
- **Sizing by limits, not vCores**: the resource-limits tables per tier and size give max log rate, data IOPS, tempdb size and max workers/sessions. General Purpose is listed at 320 IOPS per vCore (16,000 maximum). Bulk loads and index rebuilds hit log rate first, so read the log-rate row for your size.
- Zone redundancy (`--zone-redundant true`) is available in regions with availability zones; check the high-availability page for which tiers and the SLA.

## 3. Backups you get for free
- Automated full, differential (every 12 or 24 hours) and transaction-log backups; backup storage redundancy is chosen with `--backup-storage-redundancy` (geo-redundant is the default, zone or local optional). Hyperscale does not use full/differential/log backups (snapshot-based).
- **PITR** retention is 7 days by default and configurable from 1 to 35 days (Basic: 1 to 7). `az sql db restore --dest-name orders-pitr --time "2026-10-14T03:00:00Z"` restores to a new database.
- **Long-term retention** keeps weekly, monthly and yearly full backups up to 10 years: `az sql db ltr-policy set --weekly-retention P12W --monthly-retention P12M --yearly-retention P7Y --week-of-year 1`; restore with `az sql db ltr-backup restore`.
- **Geo-restore** needs geo-redundant or geo-zone-redundant backup storage and is disabled once a database moves to local or zone-redundant backup storage. For a real RTO use failover groups.
- MI: native backup to and restore from URL (`.bak`) is how migrations land.

## 4. Operations that matter
- **Maintenance window**: choose a preset with `--maint-config-id` (weekday window 10:00 PM to 6:00 AM Monday to Thursday, weekend window 10:00 PM to 6:00 AM Friday to Sunday, local time; the listed day is the start day). Without one, planned maintenance uses the default policy.
- Connection policy: Redirect (recommended) connects straight to the node hosting the database and needs outbound ports 11000-11999 to Azure SQL IPs; Proxy goes through the gateways on port 1433; Default is Redirect for clients inside Azure and Proxy for clients outside. Use retry logic for transient errors.
- Compute scale: `az sql db update --capacity 16`.
- Automatic tuning defaults: `FORCE_LAST_GOOD_PLAN` enabled, `CREATE_INDEX` and `DROP_INDEX` disabled.
- Serverless auto-pause delay: General Purpose minimum 15 minutes up to 10,080 minutes (`-1` disables auto-pause); Hyperscale minimum 60 minutes and auto-pause there is in preview per the page. A paused database resumes on the next login, so the first connection is delayed: use retry logic.
- Cost: see the Azure SQL pricing pages for reservations and Hybrid Benefit (`--license-type BasePrice`).

## Gotchas
- General Purpose remote-storage latency (5-10 ms read IO) makes chatty OLTP feel slow versus local SSD; Business Critical or Hyperscale fix it, or batch the app.
- Log rate and IOPS scale with vCores, not with storage size: a small database loading large volumes nightly is log-throttled.
- Serverless databases need connection retry logic because auto-resume delays the first connection.
- MI subnet sizing and route/NSG requirements: see the Managed Instance subnet-size article before creating the subnet.
- Elastic pool databases share pool resources; one runaway tenant affects the rest, so set per-database max.

## Verify
- [ ] `az sql db show` shows the intended SKU, zone redundancy, backup storage redundancy and maintenance configuration; Entra-only auth is enabled on the server.
- [ ] Peak-hour resource usage (the `sys.dm_db_resource_stats` view or Azure Monitor metrics) leaves headroom on CPU, data IO and log write.
- [ ] A PITR restore into a new database succeeds and the LTR policy lists the expected backups.

## Checked
2026-10-27. Confirmed against Learn: vCore service tiers, Hyperscale and serverless overviews, automated backups, maintenance window, connectivity architecture, automatic tuning overview, and the az sql server/db/elastic-pool/mi CLI references (every flag in the commands above was matched to the command's flag list).
Corrected: `--maintenance-configuration-id` is `--maint-config-id`; `--connection-policy` is not a db flag.
Removed (unconfirmed or price-related): SLA percentages, tempdb and log-rate figures, MI size limits and provisioning times, hardware family list, error numbers, diagnostic category list, LTR-with-server-deletion claim, reservation discount claims.
Method: documentation only; no commands were run.
