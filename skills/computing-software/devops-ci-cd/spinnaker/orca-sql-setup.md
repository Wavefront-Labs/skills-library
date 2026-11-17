---
id: computing-software.devops-ci-cd.spinnaker.orca-sql-setup
name: orca-sql-setup
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [orca, sql, mysql, persistence, keiko, execution-repository, orca-local-yml, tx-isolation]
level: advanced
status: docs-checked
description: "Switch Orca's execution state and work queue from Redis to MySQL: READ-COMMITTED isolation, separate migrate and service users, and the orca-local.yml block."
sources:
  - https://spinnaker.io/docs/setup/productionize/persistence/orca-sql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Orca stores execution state in Redis. SQL makes an installation more durable. With SQL for state, Redis is still required unless you also move the work queue (the page's baseline moves both).

**Database.** Orca ships with MySQL drivers and is developed against **MySQL 5.7**. Setting `tx_isolation` to `READ-COMMITTED` is essential; Orca tries to set it per session but the server should have it. Create the schema `orca` with `utf8mb4` and `utf8mb4_unicode_ci`, and two users:
- `orca_service` for runtime traffic: `SELECT, INSERT, UPDATE, DELETE, CREATE, EXECUTE, SHOW VIEW`;
- `orca_migrate` for schema changes only: those plus `DROP, REFERENCES, INDEX, ALTER, LOCK TABLES`.

Orca migrates the schema at startup, and it is safe to start several Orca instances at once.

**Configuration** (the page puts this baseline in `orca-local.yml`): `sql.enabled: true`, a `sql.connectionPool` block with `jdbcUrl`, `user`, `password`, a `migration` block with the migrate user, `executionRepository.sql.enabled: true` with `redis.enabled: false`, `monitor.activeExecutions.redis: false`, `keiko.queue.sql.enabled: true` with Redis off, `queue.zombieCheck.enabled: true`, and `queue.pendingExecutionService.sql.enabled: true` with Redis off.

The queue settings come from Netflix and were only validated on AWS Aurora MySQL 5.7; the page invites reports for other databases. A MariaDB section follows.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Orca SQL setup page. Confirmed database requirements, user grants, YAML keys and the Netflix/Aurora validation caveat. Corrected the key name to `connectionPool` and removed the unsupported claim that `orca.yml` overwrites Halyard's config.
