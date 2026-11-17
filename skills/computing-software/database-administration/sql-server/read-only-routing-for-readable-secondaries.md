---
id: computing-software.database-administration.sql-server.read-only-routing-for-readable-secondaries
name: read-only-routing-for-readable-secondaries
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, always-on, availability-group, read-only-routing, readable-secondary, applicationintent-readonly, read-scale, load-balanced-routing, listener]
level: advanced
status: docs-checked
description: "Configure SQL Server AG readable secondaries and read-only routing lists so ApplicationIntent=ReadOnly connections land on secondaries, with load balancing."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/configure-read-only-routing-for-an-availability-group-sql-server
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/active-secondaries-readable-secondary-replicas-always-on-availability-groups
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-availability-read-only-routing-lists-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read-only routing for readable secondaries

**Goal:** reporting and read-heavy app traffic goes to secondary replicas automatically
through the listener, and follows the topology after failover.

## Requirements
- SQL Server 2016 or later; the AG needs a listener; at least one readable secondary replica (check the editions page for what your edition allows).
- Only replicas on the same major build of SQL Server are readable.
- Clients must use TCP, set application intent to read-only, connect to the listener, **and** reference a database in that AG.

## Configure every replica (for both roles)
```sql
-- secondary role: allow read-intent connections and publish a routing URL
ALTER AVAILABILITY GROUP ag1 MODIFY REPLICA ON N'SQL1'
  WITH (SECONDARY_ROLE (ALLOW_CONNECTIONS = READ_ONLY,
                        READ_ONLY_ROUTING_URL = N'TCP://sql1.corp.local:1433'));
ALTER AVAILABILITY GROUP ag1 MODIFY REPLICA ON N'SQL2'
  WITH (SECONDARY_ROLE (ALLOW_CONNECTIONS = READ_ONLY,
                        READ_ONLY_ROUTING_URL = N'TCP://sql2.corp.local:1433'));
ALTER AVAILABILITY GROUP ag1 MODIFY REPLICA ON N'SQL3'
  WITH (SECONDARY_ROLE (ALLOW_CONNECTIONS = READ_ONLY,
                        READ_ONLY_ROUTING_URL = N'TCP://sql3.corp.local:1433'));
-- primary role: where to send read-intent connections when THIS replica is primary
ALTER AVAILABILITY GROUP ag1 MODIFY REPLICA ON N'SQL1'
  WITH (PRIMARY_ROLE (READ_ONLY_ROUTING_LIST = (('SQL2','SQL3'), 'SQL1')));
ALTER AVAILABILITY GROUP ag1 MODIFY REPLICA ON N'SQL2'
  WITH (PRIMARY_ROLE (READ_ONLY_ROUTING_LIST = (('SQL1','SQL3'), 'SQL2')));
ALTER AVAILABILITY GROUP ag1 MODIFY REPLICA ON N'SQL3'
  WITH (PRIMARY_ROLE (READ_ONLY_ROUTING_LIST = (('SQL1','SQL2'), 'SQL3')));
```
Inner parentheses `('SQL2','SQL3')` load-balance across that set (SQL Server 2016+; one nesting level only); if none of the set is available the next
entries are tried in order, and the list typically ends with the local replica. The routing URL is `TCP://<name or IP>:<port>` of that instance's Database Engine port,
not the listener's, and must be set before the routing list. Run these on the primary replica. SQL Server 2025 lets you set the URL to `NONE` to revert to default routing.

## Client side
`Server=tcp:ag1-listener,1433;Database=appdb;ApplicationIntent=ReadOnly;MultiSubnetFailover=True`.
The listener redirects; the client must be able to resolve and reach the replica
host names in the routing URLs. `sqlcmd` and `bcp` accept `-K ReadOnly`.

## Verify routing
```sql
SELECT ar.replica_server_name, rl.routing_priority, ar2.replica_server_name AS routes_to
FROM sys.availability_read_only_routing_lists rl
JOIN sys.availability_replicas ar  ON ar.replica_id  = rl.replica_id
JOIN sys.availability_replicas ar2 ON ar2.replica_id = rl.read_only_replica_id
ORDER BY ar.replica_server_name, rl.routing_priority;
-- from a client connected read-intent:
SELECT @@SERVERNAME;
```

## Gotchas of reading on secondaries
- Data lags the primary (usually seconds, more under I/O or network trouble or suspended data movement); apps must tolerate stale reads.
  Monitor with `sys.dm_hadr_database_replica_states` or the Always On dashboard. Anything intolerant of latency should run on the primary.
- Queries on secondaries are mapped to snapshot isolation and locking hints are ignored. The primary adds 14 bytes of row-version overhead to changed rows
  (page splits are possible) and tempdb holds row versions on the secondary. Long transactions, or a disconnected or suspended secondary,
  can block ghost-record cleanup and log truncation on the primary.
- Statistics on secondaries are temporary, stored in tempdb with the suffix `_readonly_database_statistic`; they disappear on restart or failover.
- Readers take Sch-S locks that can block redo of DDL; `sqlserver.lock_redo_blocked` fires when redo is blocked.
- Change tracking is disabled on secondary databases; CDC cannot be enabled only on a secondary.
- Read-intent connections are routed only when the primary and listener are online; if the listener is offline, clients must connect to the secondaries directly.
- `ALLOW_CONNECTIONS` for the secondary role accepts all connections (read-only) or read-intent connections only (`READ_ONLY` in the T-SQL above).

## Verify
- [ ] Routing list defined for every replica's primary role.
- [ ] A read-intent connection returns a secondary's @@SERVERNAME, and still works after failover.
- [ ] Redo lag monitored against what the readers can accept.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for Configure read-only routing, Offload workload to secondary replica (readable secondaries) and sys.availability_read_only_routing_lists (2016-2025).
Confirmed: routing URL and list syntax, load-balancing parentheses (2016+), set-URL-before-list rule, port semantics, client connection requirements, `-K ReadOnly`, view columns, snapshot isolation, 14-byte overhead, temporary statistics, latency and DDL/redo notes, 2025 `NONE`. Removed unconfirmed claims: Enterprise-only readable secondaries, licensing remark, `secondary_lag_seconds`, SSMS parameter instructions and the `read_only_routing_url` column in the sample query.
Method: documentation only; no commands were run.
