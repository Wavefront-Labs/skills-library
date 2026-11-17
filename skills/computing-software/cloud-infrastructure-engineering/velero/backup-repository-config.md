---
id: computing-software.cloud-infrastructure-engineering.velero.backup-repository-config
name: backup-repository-config
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [backup-repository-configmap, repositoryconfig, cachelimitmb, fullmaintenanceinterval, kopia-gc]
level: advanced
status: docs-checked
description: "Tune the Kopia cache limit and full maintenance interval through the backup repository ConfigMap or the repositoryConfig field."
sources:
  - https://velero.io/docs/main/backup-repository-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Backup repository settings live in the `repositoryConfig` field of each BackupRepository CR. You can also set them before the CR exists with a ConfigMap in the Velero namespace, named by the server parameter `--backup-repository-configmap` (install with `velero install --backup-repository-configmap=<ConfigMap-Name>`). Values are copied into the CR when it is created.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: <config-name>
  namespace: velero
data:
  kopia: |
    {
      "cacheLimitMB": 2048,
      "fullMaintenanceInterval": "fastGC"
    }
```

Apply with `kubectl apply -f <yaml-file-name>`. One ConfigMap per Velero namespace, one entry per repository type, applied to all repositories of that type. Editing `repositoryConfig` on an existing CR affects only that repository and needs no server restart.

Kopia options:
- `cacheLimitMB`: local data cache size limit. More cache means fewer downloads, but keep it below free disk space.
- `fullMaintenanceInterval`: default is the Kopia default of 24 hours (`normalGC`); `fastGC` is 12 hours; `eagerGC` is 6 hours.

Backup deletion does not remove Kopia data immediately. Shorter intervals remove unused blobs sooner, but unused data is deleted permanently after full maintenance, so shorter intervals can weaken data safety if misused.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/backup-repository-configuration/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
