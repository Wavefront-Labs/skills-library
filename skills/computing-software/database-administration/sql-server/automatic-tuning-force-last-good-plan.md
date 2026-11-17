---
id: computing-software.database-administration.sql-server.automatic-tuning-force-last-good-plan
name: automatic-tuning-force-last-good-plan
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, automatic-tuning, force-last-good-plan, automatic-index-management, dm-db-tuning-recommendations, plan-regression, query-store]
level: advanced
status: docs-checked
description: "Turn on SQL Server automatic plan correction (FORCE_LAST_GOOD_PLAN), read sys.dm_db_tuning_recommendations, and manage Azure SQL automatic index create/drop."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/automatic-tuning/automatic-tuning
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-db-tuning-recommendations-transact-sql
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/automatic-tuning-enable
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-database-automatic-tuning-options-transact-sql
  - https://learn.microsoft.com/en-us/sql/sql-server/editions-and-components-of-sql-server-2025
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic tuning: FORCE_LAST_GOOD_PLAN and automatic index management

## Automatic plan correction (SQL Server 2017+ Enterprise, Azure SQL)
Query Store detects a query whose new plan is significantly slower (CPU) than a previous plan,
forces the previous plan, verifies the improvement, and un-forces it if it did not help.
```sql
ALTER DATABASE CURRENT SET QUERY_STORE = ON (OPERATION_MODE = READ_WRITE);
ALTER DATABASE CURRENT SET AUTOMATIC_TUNING (FORCE_LAST_GOOD_PLAN = ON);
SELECT name, desired_state_desc, actual_state_desc, reason_desc FROM sys.database_automatic_tuning_options;
```
`actual_state_desc` OFF with `reason_desc` QUERY_STORE_READ_ONLY or QUERY_STORE_OFF means Query Store is read-only (for example full) or off: fix Query Store first. `NOT_SUPPORTED` means the edition is not Enterprise. In Azure SQL, FORCE_LAST_GOOD_PLAN is on by default while CREATE_INDEX and DROP_INDEX are off.

## Recommendations (also produced when the option is off)
```sql
SELECT reason, score,
  JSON_VALUE(details, '$.implementationDetails.script') AS fix_script,
  JSON_VALUE(state, '$.currentValue') AS state,
  JSON_VALUE(details, '$.planForceDetails.queryId') AS query_id,
  JSON_VALUE(details, '$.planForceDetails.regressedPlanId') AS bad_plan,
  JSON_VALUE(details, '$.planForceDetails.recommendedPlanId') AS good_plan
FROM sys.dm_db_tuning_recommendations ORDER BY score DESC;
```
States: Active, Verifying, Success, Reverted, Expired. With the option off, apply `fix_script`
(`sp_query_store_force_plan`) yourself after review. The DMV clears on restart. With the option on, the engine forces a recommendation when the estimated CPU gain exceeds 10 seconds or the new plan has more errors, then verifies it; a forced plan that is not yet verified is unforced on restart, a verified one stays until a recompile.

## Automatic index management (Azure SQL Database only)
```sql
ALTER DATABASE CURRENT SET AUTOMATIC_TUNING (CREATE_INDEX = ON, DROP_INDEX = ON);
```
Or configure the logical server and set `AUTOMATIC_TUNING = INHERIT` on databases. The service
creates indexes it predicts help, validates against the workload, and reverts those that regress.
DROP_INDEX never drops unique indexes (including those backing primary key and unique constraints).
Many teams keep `CREATE_INDEX` on and `DROP_INDEX` off, because an index used only by an infrequent job can look unused.

## Gotchas
- Automatic plan correction forces a plan that is the same as or similar to the last good plan, so performance can differ; if the forced plan does not beat the regressed one it is unforced.
- Recommendations are CPU-time based; the engine auto-forces only above the 10-second estimated-gain or error-count thresholds, so small regressions stay as Active recommendations.
- Schema-managed teams: automatic indexes are drift; script them back into source control or disable.

## Verify
`actual_state_desc` = ON, and recommendations reviewed weekly (or alerts on new Reverted entries).

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: automatic tuning article for SQL Server 2025 (automatic plan correction since SQL Server 2017, depends on Query Store, FORCE_LAST_GOOD_PLAN syntax, auto-force when estimated CPU gain exceeds 10 s or errors are higher, verification and unforce, restart behaviour, JSON paths implementationDetails.script and planForceDetails, DMV not persisted across restart, automatic index management is Azure SQL Database and Fabric only), sys.database_automatic_tuning_options (reason_desc DISABLED, QUERY_STORE_OFF, QUERY_STORE_READ_ONLY, NOT_SUPPORTED = Enterprise only), sys.dm_db_tuning_recommendations state values, SQL Server 2025 editions table (automatic tuning Enterprise only), Azure SQL automatic tuning pages (defaults, INHERIT, DROP_INDEX never drops unique indexes). Wrong in the draft: the reason_desc names were invented. Removed as unconfirmed: the nci_wi_ index naming and the last_force_failure_reason_desc remark.
Method: documentation only; no commands were run.
