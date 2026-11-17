---
id: computing-software.database-administration.mysql.group-replication-requirements-and-limitations
name: group-replication-requirements-and-limitations
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, group-replication-limitations, group-replication, innodb-cluster, primary-key-required, transaction-size-limit, gtid]
level: practitioner
status: docs-checked
description: "Check a MySQL schema and workload against Group Replication requirements (InnoDB, primary keys, GTIDs) and limits (transaction size, locks, multi-primary rules)."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/group-replication-requirements.html
  - https://dev.mysql.com/doc/refman/8.4/en/group-replication-limitations.html
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/check-instance-configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group Replication requirements and limitations

## Hard requirements
- InnoDB for all user tables (other engines cause errors in Group Replication); convert them, or block new ones with `disabled_storage_engines = "MyISAM,FEDERATED"`.
- **Primary key (or equivalent non-null unique key) on every table**: certification needs row identity; tables without one are not replicated safely.
- `gtid_mode = ON`, `enforce_gtid_consistency = ON`, `binlog_format = ROW` (default), `log_replica_updates = ON`, unique `server_id`.
- Low-latency reliable network between members (it is a Paxos-based group; WAN links hurt every commit).
- 3, 5 or 7 members for fault tolerance (max 9). With 3, one failure is tolerated.

Find blockers before migrating:
```sql
SELECT t.TABLE_SCHEMA, t.TABLE_NAME, t.ENGINE FROM information_schema.TABLES t
LEFT JOIN information_schema.TABLE_CONSTRAINTS c ON c.TABLE_SCHEMA = t.TABLE_SCHEMA AND c.TABLE_NAME = t.TABLE_NAME AND c.CONSTRAINT_TYPE = 'PRIMARY KEY'
WHERE t.TABLE_TYPE = 'BASE TABLE' AND t.TABLE_SCHEMA NOT IN ('mysql','sys','performance_schema','information_schema')
  AND (c.CONSTRAINT_NAME IS NULL OR t.ENGINE <> 'InnoDB');
```
```js
dba.checkInstanceConfiguration('admin@db1:3306');   // MySQL Shell reports config and schema issues
```
`sql_require_primary_key = ON` stops new PK-less tables. `sql_generate_invisible_primary_key = ON` adds a generated invisible primary key to InnoDB tables created without one.

## Limits that hit workloads
| Limit | Effect | Mitigation |
|---|---|---|
| Large transactions | message must fit `group_replication_transaction_size_limit` (~143 MB default); bigger ones roll back; big messages stall the group | batch bulk updates/deletes into chunks |
| Certification conflicts | in multi-primary, concurrent writes to the same row on different members: one aborts at commit | single-primary mode (default), or route writes for a row set to one member |
| `SELECT ... FOR UPDATE`, `LOCK TABLES`, `GET_LOCK` | locks are local to a member, not group-wide | do not rely on them across members in multi-primary |
| SERIALIZABLE isolation | not supported in multi-primary | — |
| Cascading foreign keys | unsupported in multi-primary (risk of undetected conflicts) | single-primary |
| Concurrent DDL and DML on the same object from different members | multi-primary hazard | run DDL on one member, pause writes to that object |
| Replication filters | global filters not allowed on GR channels | — |

## Flow control
Slow members make the group throttle writers (`group_replication_flow_control_mode`); one weak member drags the cluster. Size all members equally.

## Gotchas
- Members with lower versions in a mixed-version group force the group into compatibility rules; keep upgrades short.

## Checked

2026-10-31: confirmed InnoDB and primary-key requirements, gtid_mode/enforce_gtid_consistency/binlog_format=ROW/log_replica_updates settings, network requirements, the 9-member maximum and the n = 2f + 1 fault-tolerance table (groups of 3/5/7 tolerate 1/2/3 failures), disabled_storage_engines, sql_require_primary_key and sql_generate_invisible_primary_key (server system variables), transaction size limit default 150000000 bytes (~143 MB), and the multi-primary limitations (certification, SERIALIZABLE refusal, local locks, cascading foreign keys, global replication filters, concurrent DDL/DML) on dev.mysql.com 8.4 Group Replication pages. Removed the unquoted error text and the 8.0.30+ version note; corrected the disabled_storage_engines example to the documented one.
Method: documentation only; no commands were run.
