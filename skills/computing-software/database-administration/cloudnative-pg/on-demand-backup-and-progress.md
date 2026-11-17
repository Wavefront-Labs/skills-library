---
id: computing-software.database-administration.cloudnative-pg.on-demand-backup-and-progress
name: on-demand-backup-and-progress
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [backup, on-demand, backup-resource, kubectl-describe, secrets, phase]
level: practitioner
status: docs-checked
description: "Request an on-demand Backup resource, follow its phase with kubectl describe; backups exclude superuser and app user Secrets."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/backup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create a `Backup` custom resource to take a backup at any time:

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Backup
metadata:
  name: backup-example
spec:
  method: barmanObjectStore
  cluster:
    name: pg-backup
```

With the native object store method the operator runs `barman-cloud-backup` and stores the result in the configured store. Other methods are `plugin` (requires `.spec.plugins`) and `volumeSnapshot`. `method` defaults to `barmanObjectStore` for backward compatibility, even though it is deprecated.

Follow progress:

```bash
kubectl describe backup backup-example
```

While running, status shows `Phase: running` and `Started At`. On success `Phase` becomes `completed` and the status adds `Backup Id` (e.g. `20201026T135740`), `Destination Path`, `Server Name`, `Started At` and `Stopped At`.

Important: on-demand backups do **not** include the Kubernetes Secrets for the PostgreSQL superuser or application user. Include them in your wider Kubernetes cluster backup strategy.

For the plugin method, set `method: plugin` and configure the plugin; the Barman Cloud Plugin documentation has the base backup example under "Performing a Base Backup".

## Checked

2026-11-08. Backup manifest, describe output fields and the secrets warning confirmed on the Backup page, section On-Demand Backups.

Method: documentation only; no commands were run.
