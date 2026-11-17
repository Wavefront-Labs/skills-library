---
id: computing-software.database-administration.cloudnative-pg.recovery-from-volumesnapshot-and-backup-object
name: recovery-from-volumesnapshot-and-backup-object
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [recovery, volumesnapshot, backup-object, walstorage, pg-basebackup, replica-cluster]
level: advanced
status: docs-checked
description: "Recover a cluster from a VolumeSnapshot (with optional walStorage snapshot) or an existing Backup object; avoid slow pg_basebackup replicas."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/recovery.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**From VolumeSnapshots.** A new cluster can start from a `VolumeSnapshot` of a PVC of an existing cluster. It also needs an external cluster providing the WAL archive to finish recovery:

```yaml
  bootstrap:
    recovery:
      source: origin
      volumeSnapshots:
        storage:
          name: <snapshot name>
          kind: VolumeSnapshot
          apiGroup: snapshot.storage.k8s.io

  externalClusters:
    - name: origin
      plugin:
        name: barman-cloud.cloudnative-pg.io
        parameters:
          barmanObjectName: cluster-example-backup
          serverName: cluster-example
```

For an online backup reference only the `storage` snapshot; no WAL volume snapshot is taken, and WAL comes from the archive in `source`. If the backup does include a WAL volume snapshot (for example a cold backup), also reference it in `volumeSnapshots.walStorage`, and the new cluster must define `.spec.walStorage`.

Warning: after recovering a primary from a snapshot, the operator may build replicas with `pg_basebackup`, which can be much slower for large databases. To use snapshots for standbys when bootstrapping a **replica-mode** cluster: start with a single-instance replica cluster, snapshot its primary, then increase the instance count.

**From a Backup object** in the same namespace:

```yaml
  bootstrap:
    recovery:
      backup:
        name: backup-example
```

Both assume the application database and owner are named `app`; otherwise configure them as described in the recovery application database skill. While a cluster is in recovery no database change, role overrides included, is permitted until promotion. The operator does not back up the underlying secrets.

## Checked

2026-11-08. volumeSnapshots and backup.name manifests, walStorage requirement and the replica-from-snapshot procedure confirmed on the Recovery page.

Method: documentation only; no commands were run.
