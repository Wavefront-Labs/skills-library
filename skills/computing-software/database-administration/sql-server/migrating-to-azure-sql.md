---
id: computing-software.database-administration.sql-server.migrating-to-azure-sql
name: migrating-to-azure-sql
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, azure-sql, azure-sql-database, azure-sql-managed-instance, azure-sql-migration, azure-database-migration-service, dms, bacpac, log-replay-service, managed-instance-link]
level: advanced
status: docs-checked
description: "Pick the Azure SQL target and migration method (DMS, LRS, MI link, native restore, replication), clear blockers, and run a controlled cut-over."
sources:
  - https://learn.microsoft.com/en-us/data-migration/sql-server/database/guide
  - https://learn.microsoft.com/en-us/data-migration/sql-server/managed-instance/guide
  - https://learn.microsoft.com/en-us/azure/dms/dms-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating SQL Server to Azure SQL

## 1. Choose the target
- **Azure SQL Managed Instance**: the optimal choice when you lift and shift the back end of applications that regularly use instance-level and cross-database functionality, without rearchitecting. Plan to move every database that must stay collocated, plus instance objects the app depends on (logins, credentials, SQL Server Agent jobs and operators, server-level triggers). Maintenance backup jobs and Always On configuration need not move: high availability is built in.
- **Azure SQL Database**: needs compatibility work; see "Transact-SQL differences between SQL Server and Azure SQL Database" and "Discontinued Database Engine functionality". Older source versions have more issues. Managed Instance migrates with minimal to no compatibility issues.

## 2. Methods
| Target | Method | Notes from the guides |
|---|---|---|
| MI | Azure DMS | near-zero downtime; cutover: stop incoming transactions, repoint the app, take tail log backups to the backup location, wait for status Restored, then Complete cutover |
| MI | Managed Instance link | create MI, prepare environment, configure link (SSMS or scripts), stop workload, validate data, fail over the link |
| MI | Log Replay Service (LRS) | storage account and blob container, SAS token or managed identity, upload backups (copy or `BACKUP TO URL`), choose autocomplete or continuous mode, start, monitor, complete (continuous mode) |
| MI | native `RESTORE DATABASE ... FROM URL` | requires some downtime; asynchronous, retried by the service |
| MI | SQL Server migration in Azure Arc | portal-driven; offers the link or LRS |
| SQL Database | Azure DMS (offline) | see the offline DMS tutorial |
| SQL Database | transactional replication | database in SQL Database is the subscriber; only push subscriptions are supported; use the latest SSMS; the snapshot locks tables until complete |

## 3. Native restore to MI
A credential with a shared access signature, then restore from the blob URL:
```sql
CREATE CREDENTIAL [https://<STORAGE_ACCOUNT>.blob.core.windows.net/<CONTAINER>]
WITH IDENTITY = 'SHARED ACCESS SIGNATURE', SECRET = '<SAS_TOKEN>';

RESTORE DATABASE [TargetDatabaseName]
FROM URL = 'https://<STORAGE_ACCOUNT>.blob.core.windows.net/<CONTAINER>/<FILE>.bak';
```
Restoring system databases is not supported: script out instance-level objects from `master` and `msdb` and run them on the target. Track a restore with `sys.dm_exec_requests` and `sys.dm_operation_status`. A TDE-protected database needs its certificate migrated to the target before restore.

## 4. Common blockers (MI guide)
Unsupported features (run an assessment), virtual network (MI needs a dedicated subnet; check subnet, service endpoints and NSG rules), logins and users (script and recreate; watch orphaned users from SID mismatches), Agent jobs/alerts/operators (not migrated), TDE certificate, database size and I/O limits of the chosen tier.

## 5. Speeding up a SQL Database migration
The guide names source data-file I/O, target log generation rate and network bandwidth as the contention points. It recommends the highest tier and compute your budget allows during the move (scale down afterwards), keeping BACPAC files close to the destination data centre, disabling auto update/create statistics during the migration, and dropping indexed views and recreating them afterwards.

## 6. After cut-over
- Update statistics with full scan.
- Remediate applications; write validation queries run against both source and target, in an isolated test environment, plus performance tests on both.
- Compare workload performance with the baseline taken on the source; some SQL Server features need the database compatibility level raised.

## Gotchas
- Azure DMS (portal) does not migrate logins, does not support TDE databases and does not assess or recommend SKUs (per its comparison table); handle those separately.
- Plan downtime for native restore of large databases: backup, upload and restore time grows with size.

## Verify
- [ ] Blockers resolved or accepted; rehearsal migration timed end to end.
- [ ] Validation queries match on source and target before cutover.

## Checked
2026-11-09. Read in full: the SQL Server to Azure SQL Database and to Managed Instance migration guides, and "What is Azure Database Migration Service". Removed as not stated there: the SQL Database "no cross-database/no Agent/no CLR" list, the Azure VM option, downtime classes per method, SqlPackage and `az sql midb` commands, MI link version requirements, the DMA retirement claim, the bandwidth example, collation and database-count limits.
Method: documentation only; no commands were run.
