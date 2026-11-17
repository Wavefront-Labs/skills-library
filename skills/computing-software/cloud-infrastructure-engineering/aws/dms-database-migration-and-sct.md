---
id: computing-software.cloud-infrastructure-engineering.aws.dms-database-migration-and-sct
name: dms-database-migration-and-sct
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dms, database-migration, database-migration-service, schema-conversion, sct, schema-conversion-tool, dms-schema-conversion, replication-instance, replication-task, full-load, cdc, change-data-capture, ongoing-replication, table-mappings, transformation-rules, lob-handling, validation, dms-serverless, heterogeneous-migration, oracle-to-postgresql, sql-server-to-aurora, babelfish, cutover, binlog, logical-replication, dms-validation, data-validation, task-monitoring, dms-endpoint, test-connection]
level: advanced
status: draft
description: "Migrate databases with DMS and SCT: assess and convert schemas, size replication instances, build full-load + CDC tasks with table mappings and LOB settings, validate, cut over."
sources: ["https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TableMapping.html", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Validating.html", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.html", "https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Welcome.html", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_SchemaConversion.html", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Serverless.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Database migration with DMS and the Schema Conversion Tool

**Goal:** move a production database to AWS (same engine or a different one) with a
converted schema whose remaining manual work is known up front, a replication task
that copies history then streams changes with validated row counts, and a cut-over
window measured in minutes.

## 1. Plan: homogeneous vs heterogeneous
- **Homogeneous** (Oracle → RDS Oracle, PostgreSQL → Aurora PostgreSQL, MySQL → Aurora
  MySQL): native tools are often better — `pg_dump`/logical replication,
  `mysqldump`/binlog replica, Oracle Data Pump, SQL Server native backup to S3 —
  or **DMS homogeneous migrations** (managed native-tool pipelines). Use DMS CDC when
  you need a long-running sync with transformation or no native replica option.
- **Heterogeneous** (Oracle/SQL Server → PostgreSQL/MySQL, Cassandra → DynamoDB,
  MongoDB → DocumentDB): **SCT converts the schema and code**, DMS moves the data.
  SQL Server → Aurora PostgreSQL can also use **Babelfish** to keep T-SQL clients.
- DMS does **not** migrate secondary objects (indexes, FKs, triggers, sequences,
  views, procedures) in heterogeneous mode — SCT or hand-written DDL does. Create
  tables + PKs before full load; add indexes/FKs/triggers after.

## 2. SCT: assess, convert, hand-fix
```bash
# desktop SCT (Windows/macOS/Linux) with source + target JDBC drivers; or DMS Schema Conversion in the console
# 1. new project -> source Oracle, target Aurora PostgreSQL 16
# 2. Assessment report: % automatic conversion per object type + action items by complexity
# 3. Convert schema -> review, Apply to database (or save SQL)
```
- The **assessment report** (PDF/CSV) is the planning document: objects that convert
  automatically vs "complex actions" (packages, `CONNECT BY`, dynamic SQL,
  `UTL_FILE`, proprietary types). Budget the manual items before promising a date.
- **Extension packs**: SCT installs an `aws_oracle_ext` / `aws_sqlserver_ext` schema
  of emulation functions in the target (e.g. `aws_oracle_ext.nvl2`, `sysdate`);
  decide whether to keep them long-term or refactor.
- Multi-server assessor scans a fleet and recommends targets (Aurora vs RDS, instance size).
- SCT also converts application SQL embedded in code (Java/C#/Python folders) and
  ETL (SSIS → Glue), with the same report.
- Data warehouse conversions (Teradata/Netezza/Oracle → Redshift) use **SCT data
  extraction agents** rather than DMS.

## 3. DMS components
```bash
aws dms create-replication-instance --replication-instance-identifier mig-1 --replication-instance-class dms.r6i.xlarge \
  --allocated-storage 200 --vpc-security-group-ids sg-dms --replication-subnet-group-identifier private --multi-az --engine-version 3.5.3
aws dms create-endpoint --endpoint-identifier src-ora --endpoint-type source --engine-name oracle \
  --server-name ora.corp --port 1521 --username dms_user --password <PASSWORD> --database-name ORCL \
  --extra-connection-attributes "useLogminerReader=N;useBfile=Y;archivedLogDestId=1"
aws dms create-endpoint --endpoint-identifier tgt-apg --endpoint-type target --engine-name aurora-postgresql \
  --server-name app.cluster-xxxx.<REGION>.rds.amazonaws.com --port 5432 --username dms --password <PASSWORD> --database-name app \
  --extra-connection-attributes "afterConnectScript=SET session_replication_role='replica'"
aws dms test-connection --replication-instance-arn <RI> --endpoint-arn <EP>
```
- **Replication instance**: sized by memory for CDC (it buffers transactions) and
  storage for swap/logs; `dms.r6i`/`dms.r7g` memory-optimised classes; Multi-AZ for
  long CDC. Or **DMS Serverless** (`create-replication-config` with min/max DCUs) that
  auto-scales for full load + CDC.
- **Source prerequisites** (the part people skip):
  - Oracle: `ARCHIVELOG` mode, supplemental logging (`ALTER DATABASE ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS` or per-table PK logging), DMS user grants; Binary Reader (`useBfile`) over LogMiner for throughput.
  - SQL Server: full recovery model, `MS-CDC` or `MS-REPLICATION` enabled, sysadmin or specific grants; `exec sys.sp_cdc_enable_db`.
  - MySQL/Aurora MySQL: `binlog_format=ROW`, `binlog_row_image=FULL`, binlog retention ≥ 24 h (`CALL mysql.rds_set_configuration('binlog retention hours', 24)`).
  - PostgreSQL: `wal_level=logical`, `max_replication_slots`, `max_wal_senders` ≥ 1 per task, `REPLICA IDENTITY FULL` for tables without PK, `pglogical`/test_decoding plugin; the slot holds WAL — a stopped task fills the disk.
  - MongoDB: replica set (oplog), `_id` handling mode (document vs table).
- **Target tips**: disable FK/trigger enforcement during load (`session_replication_role='replica'` for PostgreSQL; `foreign_key_checks=0` via `initstmt` for MySQL), `maxFileSize`/`parallelLoadThreads` for bulk; for Redshift/S3 targets use the S3 bucket settings.

## 4. The task
```json
{"TargetMetadata": {"TargetSchema": "", "SupportLobs": true, "FullLobMode": false, "LobChunkSize": 64,
                    "LimitedSizeLobMode": true, "LobMaxSize": 32, "ParallelLoadThreads": 8, "BatchApplyEnabled": true},
 "FullLoadSettings": {"TargetTablePrepMode": "DO_NOTHING", "CreatePkAfterFullLoad": false,
                      "MaxFullLoadSubTasks": 8, "CommitRate": 10000},
 "Logging": {"EnableLogging": true},
 "ValidationSettings": {"EnableValidation": true, "ThreadCount": 5, "FailureMaxCount": 10000},
 "ErrorBehavior": {"DataErrorPolicy": "LOG_ERROR", "TableErrorPolicy": "SUSPEND_TABLE", "RecoverableErrorCount": -1},
 "ChangeProcessingTuning": {"BatchApplyPreserveTransaction": true, "BatchApplyTimeoutMin": 1, "BatchApplyTimeoutMax": 30}}
```
```json
{"rules": [
  {"rule-type": "selection", "rule-id": "1", "rule-name": "app-schema", "object-locator": {"schema-name": "APP", "table-name": "%"}, "rule-action": "include"},
  {"rule-type": "selection", "rule-id": "2", "rule-name": "skip-audit", "object-locator": {"schema-name": "APP", "table-name": "AUDIT_%"}, "rule-action": "exclude"},
  {"rule-type": "transformation", "rule-id": "3", "rule-name": "lower-schema", "rule-target": "schema", "object-locator": {"schema-name": "APP"}, "rule-action": "rename", "value": "app"},
  {"rule-type": "transformation", "rule-id": "4", "rule-name": "lower-tables", "rule-target": "table", "object-locator": {"schema-name": "APP", "table-name": "%"}, "rule-action": "convert-lowercase"},
  {"rule-type": "table-settings", "rule-id": "5", "rule-name": "big-table-parallel", "object-locator": {"schema-name": "APP", "table-name": "ORDERS"},
   "parallel-load": {"type": "ranges", "columns": ["ORDER_ID"], "boundaries": [["1000000"], ["2000000"], ["3000000"]]}}]}
```
```bash
aws dms create-replication-task --replication-task-identifier app-mig --source-endpoint-arn <SRC> --target-endpoint-arn <TGT> \
  --replication-instance-arn <RI> --migration-type full-load-and-cdc --table-mappings file://mappings.json --replication-task-settings file://settings.json
aws dms start-replication-task --replication-task-arn <TASK> --start-replication-task-type start-replication
aws dms describe-table-statistics --replication-task-arn <TASK>   # FullLoadRows, Inserts/Updates/Deletes, ValidationState
```
- **Migration types**: `full-load` (one-off), `cdc` (from a checkpoint/LSN you supply —
  use when you loaded with native tools), `full-load-and-cdc` (DMS caches changes
  during the load, applies them, then streams).
- **LOBs**: *Limited LOB mode* (truncates above `LobMaxSize` KB, fast) for most;
  *Full LOB mode* (chunked, slow, needs PK) only for tables with big documents;
  *Inline LOB mode* combines both. Tables without a PK cannot replicate LOB updates.
- Parallel full load: `MaxFullLoadSubTasks` (tables at once) × per-table `parallel-load`
  partitions/ranges for the monsters. `TargetTablePrepMode: DO_NOTHING` when SCT
  created the schema; `DROP_AND_CREATE` makes DMS create lowest-common-denominator tables (avoid).
- **Validation** compares rows source↔target (needs PK, costs source reads); states
  `Validated`/`Mismatched records`/`No primary key`; `awsdms_validation_failures_v1`
  table on the target lists the differences.
- CDC monitoring: `CDCLatencySource` (reading lag), `CDCLatencyTarget` (apply lag),
  `CDCIncomingChanges`, `FreeableMemory`, `SwapUsage` (> 0 = under-sized instance).
  Target latency climbing with source flat = missing indexes on the target or FK/trigger overhead.
- Resume: `resume-processing` from the last checkpoint; `reload-target` restarts tables
  from scratch; `reload-tables` for individual tables after fixing a `Table error`.

## 5. Cut-over runbook
1. Full load complete, CDC latency < 10 s for 24 h, validation `Validated` for all tables.
2. Create remaining indexes, FKs, triggers, sequences on the target (set sequence
   values above the source max + margin).
3. Freeze writes on the source (app read-only / revoke write grants).
4. Wait until `CDCLatencyTarget` = 0 and `describe-table-statistics` row deltas match;
   run the final validation and application smoke tests against the target.
5. Repoint the application (connection string / DNS), re-enable FK/trigger enforcement
   (`session_replication_role='origin'`), stop the DMS task, release the source
   replication slot/binlog retention.
6. Optional **reverse CDC** (target → source task prepared in advance) for a rollback window.

## Gotchas
- Oracle `NUMBER` without precision → target `NUMERIC` (decimal) or `DOUBLE` per
  `numberDataTypeScale`; dates/timezones (`TIMESTAMP WITH LOCAL TIME ZONE`) and
  `RAW`/`BLOB` sizes need explicit mapping checks.
- Case: Oracle/SQL Server upper-case identifiers become quoted names in PostgreSQL
  unless you add the `convert-lowercase` transformations — the app's SQL then breaks.
- Tables without a primary key: full load fine, CDC `UPDATE`/`DELETE` become
  full-row matches (slow, or impossible with LOBs) — add a PK or unique index first.
- DDL during CDC: supported for some engines (`CREATE/ALTER/DROP TABLE` replicated),
  but not index/trigger changes; freeze schema changes during migration.
- PostgreSQL source slot left behind after the task is deleted keeps WAL forever → disk full. `SELECT pg_drop_replication_slot(...)`.
- Replication instance public accessibility is off by default; source on-prem needs DX/VPN or a public endpoint with IP allow-list.
- Unconfirmed: DMS engine version feature matrix (e.g. Babelfish target, specific Oracle 23 support) changes per release; check release notes for 3.5.x+.

## Verify
- [ ] SCT assessment report reviewed; every "complex action" has an owner and the converted schema applied with zero errors.
- [ ] `test-connection` succeeds for both endpoints; source prerequisites confirmed (supplemental logging / binlog ROW / wal_level logical).
- [ ] Full load of the largest table runs in parallel (sub-task count > 1 in task logs) and finishes within the rehearsal window.
- [ ] `describe-table-statistics` shows `ValidationState = Validated` for all tables and `TableState = Table completed`; zero rows in `awsdms_validation_failures_v1`.
- [ ] Rehearsed cut-over on a clone: write freeze → latency 0 → repoint → app tests green, total downtime recorded and within the agreed window.
