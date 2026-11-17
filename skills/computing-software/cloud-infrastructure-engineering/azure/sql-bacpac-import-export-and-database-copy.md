---
id: computing-software.cloud-infrastructure-engineering.azure.sql-bacpac-import-export-and-database-copy
name: sql-bacpac-import-export-and-database-copy
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-sql, sql-import-export, bacpac, database-copy, sqlpackage, transactionally-consistent-copy, dev-refresh, cross-server-copy, private-link-import-export]
level: practitioner
status: docs-checked
description: "Move or clone Azure SQL databases: transactionally consistent database copy across servers, BACPAC export/import with SqlPackage or the service, and when each fits."
sources: ["https://learn.microsoft.com/en-us/azure/azure-sql/database/database-copy", "https://learn.microsoft.com/en-us/azure/azure-sql/database/database-export", "https://learn.microsoft.com/en-us/azure/azure-sql/database/database-import", "https://learn.microsoft.com/en-us/sql/tools/sqlpackage/sqlpackage-export"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BACPAC import/export and database copy

**Goal:** clone or move an Azure SQL database (prod → test refresh, cross-subscription move,
archive, on-prem hand-off) with the right tool for size and consistency.

## 1. Pick the tool
| Need | Tool |
|---|---|
| Consistent clone in Azure (same or other server/subscription in the same tenant) | **Database copy** — transactionally consistent, fast, no app downtime |
| Portable file (on-prem, other tenant, archive), small–medium DBs | **BACPAC** (schema + data) via SqlPackage |
| Schema only | DACPAC (SqlPackage extract) |
| Large DBs / near-zero downtime moves | geo-replica + failover; BACPAC of a large database is slow and is not transactionally consistent unless exported from a copy |
| Point-in-time copy | PITR restore to new DB (`az sql db restore --time`) |

## 2. Database copy
```bash
az sql db copy -g rg-prod -s sql-prod -n orders --dest-resource-group rg-test --dest-server sql-test --dest-name orders-refresh \
  --service-objective GP_Gen5_2 --backup-storage-redundancy Local
# or T-SQL on the destination server's master:
# CREATE DATABASE orders_refresh AS COPY OF sql-prod.orders ( SERVICE_OBJECTIVE = 'GP_Gen5_2' );
# SELECT state_desc FROM sys.databases WHERE name = 'orders_refresh'; SELECT * FROM sys.dm_database_copies;
```
- Logins: a copy to another server does not bring server-level logins with it — use contained users or Entra auth (see the copy article's login and SID section).
- After a prod → test copy, run a **masking/scrub script** before anyone else gets access.

## 3. BACPAC export/import
```bash
# Export from a reachable client (preferred: control, retry, Entra auth)
SqlPackage /a:Export /ssn:tcp:sql-prod.database.windows.net /sdn:orders /ua:True /tid:<tenant-id> /tf:orders.bacpac /p:VerifyFullTextDocumentTypesSupported=false
SqlPackage /a:Import /tsn:tcp:sql-test.database.windows.net /tdn:orders /ua:True /sf:orders.bacpac /p:DatabaseServiceObjective=GP_Gen5_4
# Service-side to blob (no client needed)
az sql db export -g rg-prod -s sql-prod -n orders --storage-key-type StorageAccessKey --storage-key <key> \
  --storage-uri https://stbackup.blob.core.windows.net/bacpac/orders.bacpac --admin-user <user> --admin-password <pwd>
```
- **Consistency**: export reads tables while writes continue, so the BACPAC can be inconsistent — export from a **database copy**, not the live DB.
- Exporting to blob storage is limited to a 200 GB BACPAC; export larger databases to local storage with SqlPackage.
- Import creates a new database, or loads into an existing empty database.

## Gotchas
- BACPAC fails on objects unsupported in the target (e.g. cross-DB references, Windows logins, some SQL Agent artefacts when going SQL Server → SQL DB); fix with the reported errors.
- Storage behind a firewall is not supported for service import/export; import/export over private link is in preview (see the export article).
- Import creates the database with the default geo-redundant backup storage; to choose another redundancy, create an empty database first.

## Verify
- [ ] `sys.dm_database_copies` empty and the copy `ONLINE`; row counts on key tables match the source at copy time.
- [ ] BACPAC import completes; `SELECT COUNT(*)` on key tables and schema comparison show no drift.
- [ ] Copied non-prod DB has masking applied and no prod credentials.

## Checked
2026-10-27. Confirmed on Microsoft Learn: database-copy (T-SQL `CREATE DATABASE ... AS COPY OF`, `sys.dm_database_copies`, login and SID guidance), database-export (consistency advice,
200 GB blob limit, storage behind firewall unsupported, private link in preview), database-import (new or existing empty database, default backup redundancy), sqlpackage-export
(`/a:Export`, `/ssn`, `/sdn`, `/ua`, `/tid`, `/tf`, `/p:` properties), CLI reference for `az sql db copy`, `az sql db export` and `az sql db restore` (flags in the examples).
Removed: 150 GB threshold, DMS and Extract/DeployReport syntax, Allow Azure services and cross-tenant claims, ALTER USER remap tip, private link support claim.

Method: documentation only; no commands were run.
