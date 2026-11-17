---
id: computing-software.devops-ci-cd.spinnaker.orca-redis-to-sql-migration
name: orca-redis-to-sql-migration
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [orca, sql, redis, migration, dualexecutionrepository, zero-downtime, migrators]
level: advanced
status: docs-checked
description: "Migrate a live Orca from Redis to SQL with no downtime: dual execution repository, a dedicated migration cluster with pollers, and the final disable step."
sources:
  - https://spinnaker.io/docs/guides/operator/orca-redis-to-sql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page applies only to an existing Orca deployment; for a fresh one use the Orca SQL setup. It describes a three-step zero-downtime migration.

1. **Enable the DualExecutionRepository** in `orca.yml`, on top of the baseline SQL configuration:

```yaml
executionRepository:
  dual:
    enabled: true
    primaryName: sqlExecutionRepository
    previousName: redisExecutionRepository
  sql:
    enabled: true
  redis:
    enabled: true
```

Both repositories must be enabled, or Orca fails to start. Writes go to Redis or SQL, and executions are migrated to SQL only once they have **completed** (success or terminal failure), which keeps the design simple.

2. **Deploy a migration cluster.** At Netflix the main cluster `orca-main` served traffic while `orca-main-sqlmigration` took no API traffic and did not process the queue. The latter runs with a `sqlmigration` Spring profile, `pollers.orchestrationMigrator` and `pollers.pipelineMigrator` enabled with `intervalMs: 1800000`, and Redis queue processing disabled. A separate cluster is optional, but migration is memory hungry so the process may need more resources.

3. **Finish.** Once all executions are migrated, delete the migration cluster and disable the dual repository.

How long to run migrators depends on execution length: Netflix ran them for two weeks because canaries make pipelines long; you may need only an hour.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Orca Redis to SQL Migration page. Confirmed the three steps, dual repository YAML, migration cluster settings (launched with `-Dspring.profiles.active=sqlmigration`) and the timing guidance.
