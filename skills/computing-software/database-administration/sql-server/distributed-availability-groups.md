---
id: computing-software.database-administration.sql-server.distributed-availability-groups
name: distributed-availability-groups
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, always-on, availability-group, distributed-availability-group, dag, forwarder, cross-cluster, migration, disaster-recovery, managed-instance-link]
level: sme
status: docs-checked
description: "Link two SQL Server availability groups in separate clusters with a distributed AG for cross-site DR or low-downtime migrations, including planned failover."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/distributed-availability-groups
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/configure-distributed-availability-groups
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/distributed-availability-groups
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/configure-distributed-availability-groups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed availability groups

**Goal:** replicate databases between two independent AGs (separate WSFCs, domains,
OSes or versions), with a single log stream across the WAN to a **forwarder**.

## When to use
- DR site with its own cluster/quorum: a WAN failure cannot take quorum from the primary site.
- Migrations: new hardware/OS/cluster or a newer SQL Server version (secondary AG may
  be higher version, one-way during migration), with seconds of cut-over downtime.
- Fan-out beyond replica limits (up to 18 replicas in one DAG). Read-only routing does not work through the secondary AG's listener.

## Build
Each AG exists first with its own listener; the global primary's AG has the databases.
```sql
-- on the primary replica of AG1 (global primary)
CREATE AVAILABILITY GROUP dag1 WITH (DISTRIBUTED)
AVAILABILITY GROUP ON
  'ag1' WITH (LISTENER_URL = 'tcp://ag1-listener.corp.local:5022',
              AVAILABILITY_MODE = ASYNCHRONOUS_COMMIT, FAILOVER_MODE = MANUAL,
              SEEDING_MODE = AUTOMATIC),
  'ag2' WITH (LISTENER_URL = 'tcp://ag2-listener.dr.local:5022',
              AVAILABILITY_MODE = ASYNCHRONOUS_COMMIT, FAILOVER_MODE = MANUAL,
              SEEDING_MODE = AUTOMATIC);
-- on the primary replica of AG2 (the forwarder)
ALTER AVAILABILITY GROUP dag1 JOIN AVAILABILITY GROUP ON
  'ag1' WITH (LISTENER_URL = 'tcp://ag1-listener.corp.local:5022',
              AVAILABILITY_MODE = ASYNCHRONOUS_COMMIT, FAILOVER_MODE = MANUAL, SEEDING_MODE = AUTOMATIC),
  'ag2' WITH (LISTENER_URL = 'tcp://ag2-listener.dr.local:5022',
              AVAILABILITY_MODE = ASYNCHRONOUS_COMMIT, FAILOVER_MODE = MANUAL, SEEDING_MODE = AUTOMATIC);
```
LISTENER_URL uses the **database mirroring endpoint port (5022 here)**, not the listener or SQL port. AG2 must be created
without databases (they arrive via seeding); grant `CREATE ANY DATABASE` on AG2 replicas.
Set every replica's mirroring endpoint to `LISTENER_IP = ALL`, use the same endpoint port on both AGs,
and keep both AGs in the same availability mode (both sync or both async). Each underlying AG needs a
listener (a DNN listener on Azure VMs is not supported). Higher-version target (SQL Server 2017+
can mix versions; the read/write side must be the same or lower version): seeding must be MANUAL
(back up full+log, restore WITH NORECOVERY, then `ALTER DATABASE ... SET HADR AVAILABILITY GROUP = [dag]`).

## Planned failover (no data loss)
Only manual `FORCE_FAILOVER_ALLOW_DATA_LOSS` exists for a DAG; sysadmin is required. Below is the
SQL Server 2019-and-earlier procedure; on 2022+ you may instead set
`ALTER AVAILABILITY GROUP dag1 SET (REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT = 1)` on the global primary
after the DAG is SYNCHRONIZED, do steps 3-4, then set it back to 0 on the new forwarder.
0. Stop writes on the global primary databases.
1. Set both AGs in the DAG to synchronous commit:
   `ALTER AVAILABILITY GROUP dag1 MODIFY AVAILABILITY GROUP ON 'ag1' WITH (AVAILABILITY_MODE = SYNCHRONOUS_COMMIT), 'ag2' WITH (AVAILABILITY_MODE = SYNCHRONOUS_COMMIT);`
2. Wait until every database shows SYNCHRONIZED and equal `last_hardened_lsn` on both sides
   (`sys.dm_hadr_database_replica_states` with `sys.availability_groups`; `is_distributed = 1` flags the DAG).
3. On the global primary: `ALTER AVAILABILITY GROUP dag1 SET (ROLE = SECONDARY);`
4. Re-check LSNs match (if not, fail back by running the failover command on the old global primary and restart), then on the forwarder: `ALTER AVAILABILITY GROUP dag1 FORCE_FAILOVER_ALLOW_DATA_LOSS;`
   (this is the only supported failover type for DAGs; with steps 0-3 done it loses nothing).
5. Repoint applications to AG2's listener; set back to async if it is a DR link.

## Operating notes
- Only manual failover between the AGs; the DAG has no listener of its own and nothing in the WSFC.
- A DAG has no delayed apply, so it does not protect against human error (unlike log shipping).
- Each AG keeps its own HA locally (sync replicas + automatic failover inside each).
- Monitor lag at the forwarder; the forwarder's secondaries get log from it, not the global primary.
- The SQL Managed Instance link feature is built on distributed AGs (SQL Server <-> Azure MI).

## Verify
- [ ] Both AGs show the DAG in `sys.availability_groups WHERE is_distributed = 1`.
- [ ] Databases on AG2 synchronizing; lag within RPO.
- [ ] Planned failover rehearsed with LSN comparison steps scripted.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for distributed availability groups and Configure a distributed availability group (2016-2025 gates noted).
Confirmed: T-SQL syntax including `LISTENER_URL` on the mirroring endpoint port, forwarder and seeding rules, version mixing and MANUAL seeding to a higher version, manual-only `FORCE_FAILOVER_ALLOW_DATA_LOSS` failover and both the 2019-and-earlier and 2022+ procedures, 18-replica limit, MI link relationship. Corrected the 2022 wording ("CU+") and the missing stop-writes step.
Method: documentation only; no commands were run.
