---
id: computing-software.database-administration.sql-server.basic-availability-groups-standard-edition
name: basic-availability-groups-standard-edition
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, basic-availability-group, standard-edition, availability-groups, database-mirroring-replacement, two-replica]
level: practitioner
status: docs-checked
description: "Build basic availability groups on SQL Server Standard edition (one database, two replicas), know their limits, and plan listeners, backups and upgrades around them."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/basic-availability-groups-always-on-availability-groups
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/configure-basic-availability-groups
  - https://docs.dbatools.io/New-DbaAvailabilityGroup.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-functions/sys-fn-hadr-backup-is-preferred-replica-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic availability groups (Standard edition)

The Standard-edition replacement for database mirroring (SQL 2016+).

## Limits
- At most **two replicas** (primary + one secondary; Basic AGs on Linux from SQL Server 2017 allow an extra configuration-only replica) and one **database** per AG; create one AG per database (several basic AGs can share an instance).
- Secondary is **not readable**, no backups on the secondary, no integrity checks there.
- Cannot take part in a distributed availability group (an Enterprise feature).
- Sync or async commit; automatic failover with sync commit.
- Supported only on Standard edition servers running SQL Server 2016 or later.

## Create
```sql
CREATE AVAILABILITY GROUP [BAG_appdb]
WITH (BASIC, AUTOMATED_BACKUP_PREFERENCE = PRIMARY, DB_FAILOVER = ON)
FOR DATABASE appdb
REPLICA ON
  N'sql01' WITH (ENDPOINT_URL = N'TCP://sql01.corp.example.com:5022', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
                 FAILOVER_MODE = AUTOMATIC, SEEDING_MODE = AUTOMATIC),
  N'sql02' WITH (ENDPOINT_URL = N'TCP://sql02.corp.example.com:5022', AVAILABILITY_MODE = SYNCHRONOUS_COMMIT,
                 FAILOVER_MODE = AUTOMATIC, SEEDING_MODE = AUTOMATIC);
-- on sql02
ALTER AVAILABILITY GROUP [BAG_appdb] JOIN;
ALTER AVAILABILITY GROUP [BAG_appdb] GRANT CREATE ANY DATABASE;
```
dbatools: `New-DbaAvailabilityGroup -Primary sql01 -Secondary sql02 -Name BAG_appdb -Database appdb -Basic -SeedingMode Automatic -ClusterType Wsfc`.

## Operating many basic AGs
- One listener per AG (and one IP each): applications with several databases need several
  listeners, or one listener plus connection strings that tolerate databases on different nodes.
  Keep all AGs on the same primary with a job that fails back stragglers, or the app breaks when only one database fails over.
- Backups must run on the primary: set jobs to check `sys.fn_hadr_backup_is_preferred_replica`.
- CHECKDB only on the primary (secondary not readable). Schedule accordingly.
- Logins/jobs must be synchronised to the secondary (`Copy-DbaLogin`).

## Upgrade to Enterprise
A basic AG cannot be upgraded in place to a regular (advanced) AG: drop it and create a new AG on Enterprise edition servers.

## Gotchas
- Quorum: see the WSFC quorum article for witness guidance on two-node clusters.
- Not available in a basic AG: readable secondary, backups or integrity checks on the secondary, distributed AG membership.

## Verify
Planned failover of each basic AG works and all of an app's databases end up on the same node; backups and CHECKDB run against the current primary.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: basic availability groups article for SQL Server 2025 (Standard edition, SQL Server 2016 and later, limits: two replicas plus Linux configuration-only replica, one database, no read access, backups or integrity checks on the secondary, no distributed AG, cannot be upgraded to an advanced AG, multiple basic AGs per instance, WITH BASIC syntax), sys.fn_hadr_backup_is_preferred_replica, dbatools New-DbaAvailabilityGroup (-Basic, -ClusterType, -SeedingMode in examples), dbatools Copy-DbaLogin. Removed as unconfirmed: the listener claim, the WSFC/Pacemaker requirement sentence, 'databases stay' after dropping, the two-node witness rule and the contained-AG Enterprise claim.
Method: documentation only; no commands were run.
