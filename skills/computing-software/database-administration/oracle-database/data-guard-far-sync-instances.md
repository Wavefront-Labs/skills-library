---
id: computing-software.database-administration.oracle-database.data-guard-far-sync-instances
name: data-guard-far-sync-instances
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, far-sync, data-guard, zero-data-loss, redo-routes, maximum-availability, active-data-guard, dgmgrl]
level: sme
status: docs-checked
description: "Get zero data loss to a distant Oracle standby with a Far Sync instance: create it, configure broker RedoRoutes, alternate paths, and failover behaviour."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sbydb/creating-oracle-data-guard-far-sync-instance.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dgbkr/oracle-data-guard-broker-properties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data Guard Far Sync instances

SYNC redo transport to a standby 1000 km away adds round-trip latency to every commit. A Far Sync
instance close to the primary receives redo SYNC, then forwards ASYNC to the
remote standby. If the primary fails and the far sync was synchronized, the far sync and the terminal standby coordinate a final redo shipment and a zero-data-loss failover. Far Sync is part of the Oracle Active Data Guard Far Sync feature and requires an Active Data Guard licence. There is no architectural distance limit; the practical limit is the application's tolerance of the network latency. A direct network connection between primary and remote standby is still required.

A Far Sync instance has a control file and standby redo logs but **no datafiles**. It is supported in Maximum Performance or Maximum Availability mode.

## Create
On the primary:
```sql
ALTER DATABASE CREATE FAR SYNC INSTANCE CONTROLFILE AS '/u01/fs/control01.ctl';   -- primary at least mounted
```
On the far sync host: copy the control file and a server parameter file (recommended; without one `SHOW CONFIGURATION` warns) with its own `db_unique_name = 'orcl_fs'`, `control_files` for the copied control file, and the `*_FILE_NAME_CONVERT` parameters; copy the primary's password file unless you use OS authentication with SSL transport authentication; then:
```sql
STARTUP MOUNT;
-- standby redo logs as for a regular standby (see Managing Standby Redo Logs); they cannot be shared with other databases
ALTER DATABASE ADD STANDBY LOGFILE THREAD 1 GROUP 11 SIZE 2G;  -- repeat; sizes must match the primary's online redo
```
Listener/tnsnames entries both ways (primary, far sync, remote standby).

## Broker configuration
```
DGMGRL> ADD FAR_SYNC orcl_fs AS CONNECT IDENTIFIER IS orcl_fs;   -- clear any remote redo destinations on it first; it is added disabled
DGMGRL> ENABLE FAR_SYNC orcl_fs;
DGMGRL> EDIT DATABASE orcl SET PROPERTY RedoRoutes = '(LOCAL : orcl_fs SYNC)';
DGMGRL> EDIT FAR_SYNC orcl_fs SET PROPERTY RedoRoutes = '(orcl : orcl_dr ASYNC)';
DGMGRL> EDIT CONFIGURATION SET PROTECTION MODE AS MaxAvailability;
DGMGRL> SHOW CONFIGURATION VERBOSE;
```
For role reversal, define the mirror path (a far sync near the DR site, `orcl_fs2`) and include it in
the DR database's RedoRoutes, so after switchover the new primary also has a nearby SYNC target.

## High availability of the far sync itself
Alternate paths: with `PRIORITY` (1 to 8, lower = higher priority) the primary ships to the far sync while it is available and falls back to the standby, returning when the far sync recovers:
```
DGMGRL> EDIT DATABASE orcl SET PROPERTY RedoRoutes = '(LOCAL : (orcl_fs SYNC PRIORITY=1, orcl_dr ASYNC PRIORITY=2))';
```
Or two far sync instances with the same priority (the primary keeps using the one it chose). `PRIORITY=8` destinations are all shipped to together. `LOCAL` cannot be used as a source at a far sync instance.

## Monitor
```sql
DGMGRL> SHOW CONFIGURATION;
DGMGRL> SHOW DATABASE orcl_dr;      -- transport/apply lag
DGMGRL> VALIDATE FAR_SYNC orcl_fs;  -- comprehensive far sync checks
```

## Gotchas
- Keep the far sync's password file current (recopy after privilege or password changes unless propagated).

## Verify
`SHOW CONFIGURATION` shows SUCCESS in MaxAvailability, and a tested failover to `orcl_dr` (`FAILOVER TO orcl_dr`) loses no data.

## Checked
Date 2026-10-22. Oracle Database 19c Data Guard Concepts and Administration (creating a far sync instance) and Data Guard
Broker (properties, DGMGRL commands). Confirmed: `ALTER DATABASE CREATE FAR SYNC INSTANCE CONTROLFILE AS`, ADD/ENABLE/EDIT
FAR_SYNC syntax, RedoRoutes grammar and PRIORITY semantics, licence, protection modes, zero-data-loss failover behaviour,
SPFILE/password-file/SRL notes. Removed (not documented in the pages read): the "< ~5 ms" latency rule, one-more-SRL-group
sizing, "cannot be opened or become primary", patch-level and archive-log fallback gotchas, the v$archive_dest_status
and v$managed_standby monitoring queries. The `VALIDATE FAR_SYNC` and `FAILOVER TO` commands were confirmed only as entries
in the DGMGRL command summary table, not by their syntax sections.
Method: documentation only; no commands were run.
