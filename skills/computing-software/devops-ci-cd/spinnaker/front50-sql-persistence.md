---
id: computing-software.devops-ci-cd.spinnaker.front50-sql-persistence
name: front50-sql-persistence
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [front50, sql, mysql, persistence, compositestorageservice, migration, front50-local-yml]
level: advanced
status: docs-checked
description: "Replace Front50's S3/GCS backing store with MySQL: database grants, front50-local.yml settings, and the dual-read/write CompositeStorageService for a no-downtime migration."
sources:
  - https://spinnaker.io/docs/setup/productionize/persistence/front50-sql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Front50 can use a MySQL-compatible database instead of any cloud storage service. Netflix reported eventual-consistency problems with versioned S3 buckets against Front50's read-after-write expectations; SQL gives a strongly consistent store with object versioning built in.

**Setup.** Front50 ships with `mysql-connector-java` and was developed against Amazon Aurora's MySQL 5.7 engine; other RDBMS families will likely need development work. Create database `front50` (`utf8mb4`, `utf8mb4_unicode_ci`) and two users: `front50_service` with `SELECT, INSERT, UPDATE, DELETE, CREATE, EXECUTE, SHOW VIEW`, and `front50_migrate` with those plus `DROP, REFERENCES, INDEX, ALTER, LOCK TABLES`.

**Configuration.** Add to `front50-local.yml`: `sql.enabled: true`, `connectionPools.default` with `default: true`, `jdbcUrl: jdbc:mysql://your.database:3306/front50` and `user: front50_service`, and a `migration` block with `front50_migrate`. Disable any previously enabled storage services such as S3 or GCS.

**Migration without downtime.** Use `CompositeStorageService` with `spinnaker.migration.primaryClass: com.netflix.spinnaker.front50.model.SqlStorageService` and `previousClass` set to your current implementation (the page uses `S3StorageService`), with `compositeStorageService.enabled: true` and `reads.primary: false`, `reads.previous: true`. This enables primary and previous writes while leaving reads on the previous store.

Then enable the migrator with `spinnaker.migration.enabled: true`. Lastly set `compositeStorageService.reads.primary: true` (and `previous: true` to fall back when an object is not found, `false` to disable fallback). When satisfied, remove the `spinnaker.migration` block and disable the previous storage service.

The page's Netflix account: the migrator ran on a temporary cluster outside the load balancer, results were checked by searching logs for `StorageServiceMigrator` and `CompositeStorageService`, and the migration was spread over a week with pipelines holding both SQL and non-SQL deploy stages for easy rollback.

## Checked

2026-11-04. Rationale, driver and version note, grants, YAML keys and the migration stages and Netflix account were confirmed on the Front50 SQL page. Removed: the claim that Halyard does not natively support it (not on the page).

Method: documentation only; no commands were run.
