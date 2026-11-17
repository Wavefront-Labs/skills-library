---
id: computing-software.database-administration.mysql.group-replication-single-vs-multi-primary
name: group-replication-single-vs-multi-primary
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, group-replication, single-primary-mode, multi-primary-mode, innodb-cluster, primary-election, group-replication-consistency, switch-to-multi-primary]
level: practitioner
status: docs-checked
description: "Choose and switch MySQL Group Replication between single-primary and multi-primary mode, with their conflict, consistency and DDL constraints."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/group-replication-deploying-in-single-primary-mode.html
  - https://dev.mysql.com/doc/refman/8.4/en/group-replication-deploying-in-multi-primary-mode.html
  - https://dev.mysql.com/doc/refman/8.4/en/group-replication-changing-group-mode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group Replication: single-primary vs multi-primary

**Goal:** run the mode that matches the workload, and know what each one forbids.

## Single-primary (default, recommended)
One writable member; others `super_read_only`. On primary failure a new primary is elected: lowest MySQL version first, then `group_replication_member_weight` (default 50), then lowest `server_uuid`.
```sql
SELECT MEMBER_HOST, MEMBER_STATE, MEMBER_ROLE, MEMBER_VERSION FROM performance_schema.replication_group_members;
SELECT group_replication_set_as_primary('<member_uuid>');   -- planned switchover
```
Shell: `cluster.setPrimaryInstance('db2:3306')`.

## Multi-primary
All members accept writes; conflicts are detected at certification: one transaction commits, the other is rolled back. Restrictions enforced by `group_replication_enforce_update_everywhere_checks = ON`:
- No `SERIALIZABLE` isolation.
- No cascading foreign keys.
- Concurrent DDL and DML on the same object on different members is unsafe; route DDL to one member.
Apps must retry rolled-back transactions; hot rows written from several members thrash.

## Switching online
```sql
SELECT group_replication_switch_to_multi_primary_mode();
SELECT group_replication_switch_to_single_primary_mode('<member_uuid>');
```
Shell: `cluster.switchToMultiPrimaryMode()` / `switchToSinglePrimaryMode()`.

## Consistency on reads after failover/writes
`group_replication_consistency`: `BEFORE_ON_PRIMARY_FAILOVER` (the MySQL 8.4 default; a new primary holds reads and writes until its backlog is applied), `EVENTUAL`, `BEFORE`, `AFTER`, `BEFORE_AND_AFTER` (read-your-writes across members at latency cost).

## Gotchas
- Minimum 3 members for fault tolerance; up to 9.
- Every table needs a primary key (or non-null unique key) and InnoDB.
- Multi-primary is not a write-scaling feature: every write is applied on every member.

## Checked

2026-10-31: confirmed single-primary fencing (super_read_only), the primary election factors in order (lowest MySQL version, then member weight, then lowest server_uuid; member weight range 0-100 default 50), group_replication_switch_to_multi_primary_mode()/switch_to_single_primary_mode() and enforce_update_everywhere_checks, the multi-primary strict checks (SERIALIZABLE commit fails, cascading foreign keys fail), group_replication_consistency values with BEFORE_ON_PRIMARY_FAILOVER as the 8.4 default, and the 9-member maximum on dev.mysql.com 8.4 Group Replication pages. Corrected the election order and the consistency default; removed the unconfirmed error number and version notes.
Method: documentation only; no commands were run.

## Verify
`replication_group_members` shows the expected roles; in multi-primary, two concurrent updates of the same row from different members: one commits, one is rolled back.
