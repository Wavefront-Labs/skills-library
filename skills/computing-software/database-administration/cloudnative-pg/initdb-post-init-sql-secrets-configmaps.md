---
id: computing-software.database-administration.cloudnative-pg.initdb-post-init-sql-secrets-configmaps
name: initdb-post-init-sql-secrets-configmaps
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [initdb, postinitsql, postinitapplicationsql, postinittemplatesql, superuser, configmap]
level: practitioner
status: docs-checked
description: "Run one-off SQL after initdb as the superuser against postgres, template1 and the app database, inline or from Secrets and ConfigMaps, and know the ordering and failure behaviour."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/bootstrap.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
After the cluster is created, CloudNativePG can run queries once, as the `postgres` superuser, against three databases in this order:

1. `postgres` (`postInitSQL`, `postInitSQLRefs`)
2. `template1` (`postInitTemplateSQL`, `postInitTemplateSQLRefs`)
3. the application database (`postInitApplicationSQL`, `postInitApplicationSQLRefs`)

Within each section inline SQL runs first, then the referenced objects; Secrets are processed before ConfigMaps, each list sequentially.

```yaml
  bootstrap:
    initdb:
      database: app
      owner: app
      postInitApplicationSQLRefs:
        secretRefs:
        - name: my-secret
          key: secret.sql
        configMapRefs:
        - name: my-configmap
          key: configmap.sql
```

Inline form: `postInitSQL: [ "CREATE DATABASE angus" ]`.

Cautions from the page:

- An error in any query interrupts bootstrap and leaves the cluster incomplete, needing manual intervention. The referenced Secret/ConfigMap keys must exist or bootstrap fails.
- Queries run as superuser, so mistakes can disrupt the whole cluster.
- Each statement is a single exec following PostgreSQL multi-statement protocol semantics; comments are allowed but `psql` meta-commands are not.
- These scripts use the standard `"$user", public` search_path (unlike operator connections); schema-qualify names to be independent.

## Checked

2026-11-08. Read in full: docs/src/bootstrap.md (sections bootstrap, externalClusters, initdb post-init queries). Execution order, SQL ref ordering and the failure warning confirmed on the Bootstrap page, section Executing Queries After Initialization.

Method: documentation only; no commands were run.
