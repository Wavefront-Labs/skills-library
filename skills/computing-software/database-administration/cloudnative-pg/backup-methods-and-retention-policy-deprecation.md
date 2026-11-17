---
id: computing-software.database-administration.cloudnative-pg.backup-methods-and-retention-policy-deprecation
name: backup-methods-and-retention-policy-deprecation
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [backup, method, plugin, volumesnapshot, barmanobjectstore, retention-policy, deprecation, barman-cloud-plugin]
level: advanced
status: docs-checked
description: "Pick the backup method (plugin, volumeSnapshot, barmanObjectStore), plan for native Barman Cloud removal in 1.32.0, and know why spec.backup.retentionPolicy is deprecated."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/backup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `.spec.method` field of `Backup` and `ScheduledBackup` accepts:

- `plugin`: a CNPG-I plugin (requires `.spec.plugins` in the Cluster).
- `volumeSnapshot`: native Kubernetes volume snapshots.
- `barmanObjectStore`: native Barman Cloud; deprecated since 1.26, still the default for backward compatibility.

```yaml
spec:
  method: volumeSnapshot
```

For the plugin, set `method: plugin` and follow the Barman Cloud Plugin docs.

Warning: native Barman Cloud support, both the `barmanObjectStore` method and the `.spec.backup.barmanObjectStore` stanza, is removed starting with 1.32.0. Releases up to 1.31 and their patches keep it while supported. Follow the plugin guide "Migrating from Built-in CloudNativePG Backup" **before** upgrading to 1.32 or later. Because the default method is still `barmanObjectStore`, explicitly set `method: plugin` in manifests you migrate.

Retention: the project is moving to a backup-agnostic design where plugins own advanced retention. `spec.backup.retentionPolicy` in the `Cluster` is **deprecated** and will be removed. Use the retention mechanism of your plugin (for the Barman Cloud Plugin, its "Retention Policies" page) so retention stays consistent with the backup method. Note volume snapshots have no retention policy in the native feature, so you must delete old `VolumeSnapshot` objects through your own process.

## Checked

2026-11-04. Method list, 1.32.0 removal warning and retentionPolicy deprecation confirmed on the Backup page, sections Backup Methods and Retention Policies.

Method: documentation only; no commands were run.
