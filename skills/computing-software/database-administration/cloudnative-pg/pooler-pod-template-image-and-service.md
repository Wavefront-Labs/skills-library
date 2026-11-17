---
id: computing-software.database-administration.cloudnative-pg.pooler-pod-template-image-and-service
name: pooler-pod-template-image-and-service
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [pooler, pgbouncer, pod-template, image-catalog, servicetemplate, anti-affinity, admission-policy]
level: advanced
status: docs-checked
description: "Customise PgBouncer pods and Service: the pgbouncer container name, mandatory containers array, image precedence (template, image, imageCatalogRef) and serviceTemplate ports."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/connection_pooling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `template` section of a `Pooler` is a standard `PodSpec`, so `containers` is **mandatory**; use `containers: []` if you change no container settings, otherwise the API server returns a `ValidationError`. A container you override must be named `pgbouncer`:

```yaml
  template:
    spec:
      containers:
        # This name MUST be "pgbouncer"
        - name: pgbouncer
          resources:
            requests:
              cpu: "0.1"
              memory: 100Mi
            limits:
              cpu: "0.5"
              memory: 500Mi
```

Spread pods with `podAntiAffinity` (`requiredDuringSchedulingIgnoredDuringExecution`, `topologyKey: "kubernetes.io/hostname"`) keyed on a label set in `template.metadata.labels`.

**Image precedence**, first match wins: the `image` on the `pgbouncer` container in the template, then `spec.pgbouncer.image`, then `spec.pgbouncer.imageCatalogRef` (a `key` in an `ImageCatalog` or `ClusterImageCatalog` `componentImages` list), then the operator default. `image` and `imageCatalogRef` are mutually exclusive. Catalog updates roll out automatically. Check `status.image`, and `status.phase` (`active`, `paused`, `inactive`, `failed`; see `status.phaseReason`).

Warning: admission policies that restrict PgBouncer images must gate all three sources, or the template `image` is an unguarded escape hatch. Same for `Cluster.spec.imageName` and `imageCatalogRef`.

`serviceTemplate` changes Service labels, annotations or type (for example `LoadBalancer`). The operator adds a `pgbouncer` ServicePort on 5432; declaring a port named `pgbouncer` or numbered `5432` suppresses that default.

## Checked

2026-11-04. Template requirements, image precedence list, policy-gating warning and serviceTemplate port rule confirmed on the Connection pooling page.

Method: documentation only; no commands were run.
