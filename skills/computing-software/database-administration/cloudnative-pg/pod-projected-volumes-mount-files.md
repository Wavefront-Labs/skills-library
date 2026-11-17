---
id: computing-software.database-administration.cloudnative-pg.pod-projected-volumes-mount-files
name: pod-projected-volumes-mount-files
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [projected-volume, projectedvolumetemplate, secret, configmap, mount, pods]
level: practitioner
status: docs-checked
description: "Mount extra Secret or ConfigMap files into CloudNativePG Postgres pods with spec.projectedVolumeTemplate; they appear under the /projected directory."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/cluster_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.spec.projectedVolumeTemplate` is a Kubernetes projected-volume template whose contents are mounted under `/projected` in every Postgres pod. It suits PostgreSQL features and extensions that need extra data files, such as certificates, key files or configuration.

This example mounts the keys of an existing Secret `sample-secret` as `/projected/certificate/tls.crt` and `/projected/certificate/tls.key`:

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: cluster-example-projected-volumes
spec:
  instances: 3
  projectedVolumeTemplate:
    sources:
      - secret:
          name: sample-secret
          items:
            - key: tls.crt
              path: certificate/tls.crt
            - key: tls.key
              path: certificate/tls.key
  storage:
    size: 1Gi
```

The `path` in each item is relative to `/projected`. You can mix Secret and ConfigMap sources in one template; the repository ships a complete sample, `cluster-example-projected-volume.yaml`, that does exactly that.

Then reference the mounted paths from PostgreSQL parameters or extension settings (for example a certificate path), rather than baking files into the image. Typical contents are certificates, key files and extra configuration needed by extensions.

## Checked

2026-11-08. Read in full: docs/src/cluster_conf.md. projectedVolumeTemplate example and mount root /projected confirmed on the Instance Pod configuration page.

Method: documentation only; no commands were run.
