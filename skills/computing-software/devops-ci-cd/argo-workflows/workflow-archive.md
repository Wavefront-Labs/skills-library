---
id: computing-software.devops-ci-cd.argo-workflows.workflow-archive
name: workflow-archive
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [workflow-archive, persistence, archive-ttl, archive-migration, argo-archived-workflows]
level: practitioner
status: docs-checked
description: "Enable the SQL workflow archive in the persistence config section with a database secret, plus TTL, cluster name, migration and required permissions."
sources: ["https://argo-workflows.readthedocs.io/en/latest/workflow-archive/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow archive
The archive keeps completed Workflow status (not pod logs) in Postgres (9.4+), MySQL (5.7.8+) or MariaDB (10.2+). For logs, use an artifact repository. The quick-start includes Postgres with archive already enabled; use a production database otherwise.

Enable in the controller config:

```yaml
persistence:
  archive: true
  postgresql:
    host: localhost
    port: 5432
    database: postgres
    tableName: argo_workflows
    userNameSecret: {name: argo-postgres-config, key: username}
    passwordSecret: {name: argo-postgres-config, key: password}
```
Create that secret in the controller's namespace (`kubectl create secret generic argo-postgres-config -n argo --from-literal=...`). Tables created: `argo_workflows`, `argo_archived_workflows`, `argo_archived_workflows_labels`, `schema_history`.

Migration runs at every controller start; if it fails, the controller will not start, and the remedy is deleting the tables and restarting. `persistence.skipMigration: true` skips it for experts. Postgres users need `CREATE` and `USAGE` on schema `public`.

Retention: `archiveTTL: 10d` (default forever). Garbage collection runs every `ARCHIVED_WORKFLOW_GC_PERIOD`, first run only after one full period, not at startup. `clusterName` fills the `clustername` column.

Disable with `archive: false`.

## Checked

2026-11-08. Read the Argo Workflows workflow archive page in full (raw markdown) and confirmed supported databases, persistence config, secret, created tables, migration behaviour, skipMigration, Postgres permissions, archiveTTL, GC period behaviour, clusterName, and disabling. Nothing removed.

Method: documentation only; no commands were run.
