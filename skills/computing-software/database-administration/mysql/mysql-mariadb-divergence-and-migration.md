---
id: computing-software.database-administration.mysql.mysql-mariadb-divergence-and-migration
name: mysql-mariadb-divergence-and-migration
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, mysql-upgrade, mariadb-migration, compatibility, gtid-differences, json-type, sys-versioning, logical-migration]
level: advanced
status: draft
description: "Know where MySQL 8 and MariaDB 10.x/11.x diverge (GTIDs, JSON, auth, system tables, replication) and migrate between them with a logical dump rather than in place."
sources:
  - https://mariadb.com/kb/en/mariadb-vs-mysql-compatibility/
  - https://mariadb.com/kb/en/moving-from-mysql-to-mariadb/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MySQL vs MariaDB divergence

**Goal:** treat MySQL 8 and MariaDB as different products: choose consciously, and
move between them without corrupting data or replication.

## Key differences (MySQL 8.x vs MariaDB 10.6+/11.x)
| Area | MySQL 8 | MariaDB |
|---|---|---|
| Data dictionary | Transactional DD in InnoDB, no .frm | .frm files |
| GTID | `server_uuid:N` | `domain-server-seq` (gtid_domain_id); incompatible |
| JSON | Native binary type | Alias for LONGTEXT + CHECK(JSON_VALID) |
| Auth default | caching_sha2_password | mysql_native_password / ed25519 / unix_socket for root |
| Features unique | Group Replication, InnoDB Cluster, histograms auto-update, invisible indexes | Galera built in, system-versioned tables, sequences, Aria/ColumnStore/Spider engines, `RETURNING` |
| Default collation | utf8mb4_0900_ai_ci | utf8mb4_general_ci (11.x: uca1400) |
| Tools | MySQL Shell utilities, mysqldump | mariadb-dump, mariabackup (fork of XtraBackup) |

## Migration rules
- **In-place binary swap is not supported** from MySQL 8.0 to MariaDB (or back):
  different DD and redo formats. MySQL 5.7 → MariaDB 10.x in place worked
  historically; do not rely on it now.
- Use a logical migration: `mysqldump --single-transaction --routines --triggers --events`
  (or mydumper/myloader), load into the target, then replicate to catch up.
- Cross-vendor replication: MariaDB can replicate **from** MySQL (file/position,
  not GTID-auto-positioning) for cutover; MySQL 8 replicating from MariaDB is
  not supported.
- Rewrite collations: `utf8mb4_0900_ai_ci` does not exist in MariaDB < 11.4; sed
  it to a supported collation in the dump.
- Users and grants: dump with `SHOW CREATE USER` / pt-show-grants and translate
  auth plugins.

## Gotchas
- Client libraries and connectors usually work on both, but SQL features
  (window functions behaviour, JSON functions, CTE limits, optimizer hints) differ: run the app test suite against the target.
- Monitoring queries using `performance_schema`/`sys` differ in detail.
- Managed services: Aurora MySQL and RDS MariaDB are separate engines; switching is a migration.

## Verify
Row counts and checksums per table (e.g. `CHECKSUM TABLE` is engine-dependent;
compare `SELECT COUNT(*)` plus sampled hashes), and the app test suite passes on the target.
