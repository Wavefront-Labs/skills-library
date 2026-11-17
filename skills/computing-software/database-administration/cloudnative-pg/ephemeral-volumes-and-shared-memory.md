---
id: computing-software.database-administration.cloudnative-pg.ephemeral-volumes-and-shared-memory
name: ephemeral-volumes-and-shared-memory
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [ephemeral-volumes, emptydir, shm, temporary-data, ephemeralvolumesizelimit, posix]
level: practitioner
status: docs-checked
description: "Size or replace the ephemeral storage CloudNativePG uses for temporary data and shared memory: emptyDir limits, ephemeralVolumeSource claim templates and the shm size limit."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/cluster_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CloudNativePG uses ephemeral volumes, which exist only for the life of a pod, for part of its internal work. By default the temporary data volume is an `emptyDir`.

Options:

- `.spec.ephemeralVolumesSizeLimit` caps the volume sizes (the page refers to the `temporaryData` and `shm` sub-fields).
- `.spec.ephemeralVolumeSource` replaces the `emptyDir` with a volume claim template.
- You cannot specify both `.spec.ephemeralVolumeSource` and `.spec.ephemeralVolumesSizeLimit.temporaryData` at once.

Example of a 1Gi claim-template-backed ephemeral volume:

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: cluster-example-ephemeral-volume-source
spec:
  instances: 3
  ephemeralVolumeSource:
    volumeClaimTemplate:
      spec:
        accessModes: ["ReadWriteOnce"]
        # example storageClassName, replace with one existing in your Kubernetes cluster
        storageClassName: "scratch-storage-class"
        resources:
          requests:
            storage: 1Gi
```

Shared memory: a memory-backed ephemeral volume serves as PostgreSQL shared memory. Bound it with `.spec.ephemeralVolumesSizeLimit.shm`, and only when PostgreSQL runs with `posix` dynamic shared memory allocation (see the dynamic shared memory settings in the PostgreSQL configuration page).

## Checked

2026-11-08. Read in full: docs/src/cluster_conf.md. Ephemeral volume options, mutual exclusion rule and shm use confirmed on the Instance Pod configuration page.

Method: documentation only; no commands were run.
