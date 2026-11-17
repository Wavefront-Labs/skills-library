---
id: computing-software.database-administration.cloudnative-pg.vpa-and-hpa-autoscaling-guidance
name: vpa-and-hpa-autoscaling-guidance
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [vpa, hpa, autoscaling, recommendation-only, scale-subresource, updatemode, resources]
level: advanced
status: docs-checked
description: "Use the Vertical Pod Autoscaler on a CloudNativePG Cluster in recommendation-only mode and see why updateMode Auto and horizontal autoscaling of instances are not recommended."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/resource_management.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `Cluster` CRD exposes the `scale` subresource and a label selector for its pods, so it is a valid `targetRef` for a VPA. Run the VPA in **recommendation-only** mode and apply the numbers to `spec.resources` yourself; CloudNativePG then does its switchover-aware rolling update. Use the recommendation for the `postgres` container.

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: cluster-example-vpa
spec:
  targetRef:
    apiVersion: postgresql.cnpg.io/v1
    kind: Cluster
    name: cluster-example
  updatePolicy:
    updateMode: "Off"
```

Do not use `Auto`, `Recreate` or `Initial`. The operator treats `spec.resources` as the source of truth and does not adopt what VPA writes to a running pod, so live and declared resources silently diverge (and tuning such as `shared_buffers` no longer matches the real limits). VPA also evicts through the eviction API, bypassing the operator's sequencing, and the default primary `PodDisruptionBudget` blocks the primary eviction, so VPA stalls.

HPA can technically drive `spec.instances`, but it is **not recommended**. Scaling only adds standby replicas and never relieves primary write load, and the scale selector matches the primary and replicas, whose workloads differ, so average CPU or memory is not a meaningful signal. HPA also ignores constraints: with synchronous replication, scaling below `maxSyncReplicas + 1` is rejected by the webhook and HPA keeps retrying. If you still use it, drive it from a custom read-load metric and set `minReplicas` above the synchronous floor.

## Checked

2026-11-04. VPA manifest, updateMode warning and the HPA reasoning confirmed on the Resource management page.

Method: documentation only; no commands were run.
