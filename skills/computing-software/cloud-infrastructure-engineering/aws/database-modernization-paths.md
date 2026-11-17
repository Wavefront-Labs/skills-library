---
id: computing-software.cloud-infrastructure-engineering.aws.database-modernization-paths
name: database-modernization-paths
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, migration, database-modernization, dms, schema-conversion, babelfish, aurora-postgresql, replatform]
level: practitioner
status: draft
description: "Pick a database modernisation path: rehost on EC2, replatform to RDS, convert engines with DMS Schema Conversion, Babelfish for SQL Server apps, or move to purpose-built stores."
sources: ["AWS Prescriptive Guidance - Database migration strategy", "AWS DMS User Guide - DMS Schema Conversion and Fleet Advisor", "Amazon Aurora User Guide - Babelfish for Aurora PostgreSQL", "AWS Schema Conversion Tool User Guide - Assessment reports"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Database modernisation paths

## Options
| Path | Example | Effort | Gains |
|---|---|---|---|
| Rehost | Oracle on EC2 | low | DC exit; you still run the DB |
| Replatform (same engine) | SQL Server -> RDS for SQL Server; MySQL -> Aurora MySQL | low-medium | managed backups, HA, patching |
| Engine conversion | Oracle/SQL Server -> Aurora PostgreSQL | high | licence savings, cloud-native features |
| Compatibility layer | SQL Server apps -> Babelfish for Aurora PostgreSQL | medium | keep T-SQL and TDS protocol for many apps |
| Purpose-built | session/catalog -> DynamoDB; search -> OpenSearch; cache -> ElastiCache | high (app changes) | scale, cost per use case |

## Assess
- **DMS Fleet Advisor** inventories database servers and sizes targets.
- **DMS Schema Conversion** (or SCT) assessment report: % of objects converted automatically,
  action items by complexity; generative AI assistance for stored procedure conversion in newer versions.
- Look for blockers: heavy PL/SQL or T-SQL packages, CLR, linked servers, Oracle-specific features
  (autonomous transactions, advanced queuing), application ORMs pinned to an engine.
- Babelfish compatibility assessment (Babelfish Compass) for SQL Server.

## Migrate data
- DMS full load + CDC for minimal downtime; native tools (pg_dump, mysqldump, RMAN, backup/restore to RDS SQL Server via S3) for simpler cutovers.
- DMS data validation on critical tables; LOB settings and parallel load tuning for large tables.

## Decide
- Licence costs and contract dates often decide timing.
- Do engine conversion as its own project after a replatform when the application is large; doing both with a DC exit deadline is the classic overrun.
- Purpose-built moves are application refactors; do them per bounded context, not per database.

## Gotchas
- Converted code compiles but behaves differently: collations, NULL/empty string (Oracle), implicit casts, transaction isolation defaults, sequence and identity semantics.
- Performance regressions after conversion: execution plans differ; load test with production volumes.
- Reporting tools and ETL jobs connected to the old database are often forgotten.

## Verify
- [ ] Assessment report per database with chosen path and rationale.
- [ ] Converted database passes application regression and performance tests before cutover.
