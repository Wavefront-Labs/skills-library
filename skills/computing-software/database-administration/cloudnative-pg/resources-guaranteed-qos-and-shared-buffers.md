---
id: computing-software.database-administration.cloudnative-pg.resources-guaranteed-qos-and-shared-buffers
name: resources-guaranteed-qos-and-shared-buffers
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [resources, qos, guaranteed, requests, limits, oom, shared-buffers, pg-oom-adjust-value]
level: practitioner
status: docs-checked
description: "Size CloudNativePG pods with equal requests and limits for Guaranteed QoS, understand PG_OOM_ADJUST_VALUE, and align shared_buffers (about 25 percent) with container memory."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/resource_management.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set the `resources` section with `requests` (initial requirement, used by scheduling) and `limits` (maximum). For PostgreSQL the recommended class is **Guaranteed**, which requires requests and limits for both memory and CPU set to the **same** value.

```yaml
spec:
  instances: 3
  postgresql:
    parameters:
      shared_buffers: "256MB"
  resources:
    requests:
      memory: "1024Mi"
      cpu: 1
    limits:
      memory: "1024Mi"
      cpu: 1
  storage:
    size: 1Gi
```

With Guaranteed QoS, CloudNativePG sets `PG_OOM_ADJUST_VALUE` for the `postmaster` to `0`. The postmaster keeps its low OOM score of `-997` while child processes run with an adjustment of `0`, so if the OOM killer fires it kills children first. That keeps the instance alive longer and allows a clean shutdown on eviction.

Sizing: a reasonable starting `shared_buffers` is 25% of system memory, so 256MB suggests about 1GB of container memory (the PostgreSQL default is 128MB). Keep PostgreSQL memory parameters consistent with the pod resources as you would on a VM.

Avoid `OOM Killed` and CPU throttling by always setting values explicitly, and consider a dedicated node using the `nodeSelector` and `tolerations` fields of the affinity configuration.

## Checked

2026-11-04. Trimmed claims the page does not state. QoS rules, OOM adjustment behaviour and the example manifest confirmed on the Resource management page.

Method: documentation only; no commands were run.
