---
id: computing-software.database-administration.cloudnative-pg.recovery-from-object-store-barman-cloud-plugin
name: recovery-from-object-store-barman-cloud-plugin
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [recovery, barman-cloud-plugin, objectstore, externalclusters, bootstrap-recovery, servername, superusersecret]
level: advanced
status: docs-checked
description: "Restore into a new cluster from an object store via the Barman Cloud Plugin: ObjectStore, bootstrap.recovery.source, externalClusters."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/recovery.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Recovery is **never in place**: it bootstraps a **new** cluster from a physical backup and replays WAL. The object store must contain data produced by a CloudNativePG `Cluster`, through the plugin or the deprecated native integration.

Define the store holding base backups and WAL with the plugin's `ObjectStore` resource (Azure Blob example):

```yaml
apiVersion: barmancloud.cnpg.io/v1
kind: ObjectStore
metadata:
  name: cluster-example-backup
spec:
  configuration:
    destinationPath: https://STORAGEACCOUNTNAME.blob.core.windows.net/CONTAINERNAME/
    azureCredentials:
      storageAccount:
        name: recovery-object-store-secret
        key: storage_account_name
      storageKey:
        name: recovery-object-store-secret
        key: storage_account_key
    wal:
      maxParallel: 8
```

Then reference it from the new `Cluster`:

```yaml
spec:
  superuserSecret:
    name: superuser-secret

  bootstrap:
    recovery:
      source: origin

  externalClusters:
    - name: origin
      plugin:
        name: barman-cloud.cloudnative-pg.io
        parameters:
          barmanObjectName: cluster-example-backup
          serverName: cluster-example
```

To keep the original postgres password, set `enableSuperuserAccess` and supply a `superuserSecret`. `wal.maxParallel` speeds up WAL fetching by downloading in parallel.

By default, recovery runs to the latest WAL on timeline `latest`; add a `recoveryTarget` for PITR.

## Checked

2026-11-08. ObjectStore and recovery Cluster manifests plus the recovery-is-never-in-place rule confirmed on the Recovery page.

Method: documentation only; no commands were run.
