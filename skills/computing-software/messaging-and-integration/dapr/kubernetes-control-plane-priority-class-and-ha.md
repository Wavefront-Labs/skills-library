---
id: computing-software.messaging-and-integration.dapr.kubernetes-control-plane-priority-class-and-ha
name: kubernetes-control-plane-priority-class-and-ha
category: computing-software
field: messaging-and-integration
product: dapr
tags: [kubernetes, priorityclass, high-availability, placement, scheduler, resourcequota, eviction]
level: advanced
status: docs-checked
description: "Protect the Dapr control plane from eviction with system-cluster-critical, enable HA on an existing install by deleting the placement StatefulSet, and the pre-1.14 ResourceQuota."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/kubernetes/kubernetes-production.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Under node memory or CPU pressure the control plane pods may be evicted. The Scheduler is the most sensitive: restarts can make in-flight jobs fire duplicate times. Set the priority class at install time:

```bash
--set global.priorityClassName=system-cluster-critical
```

(works with Helm and the CLI). `system-node-critical` is higher; the page recommends `system-cluster-critical` and says your own application priority classes should have a lower value.

For Dapr versions below 1.14, also add a ResourceQuota in the control plane namespace so scheduling is allowed where the cluster limits high-priority classes (from 1.14 the Helm chart adds it):

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dapr-system-critical-quota
  namespace: dapr-system
spec:
  scopeSelector:
    matchExpressions:
      - operator : In
        scopeName: PriorityClass
        values: [system-cluster-critical]
```

Enabling HA on an existing deployment takes two steps. In HA mode placement adds Raft for leader election and Kubernetes only lets a few StatefulSet fields be patched, so first delete the old one (safe; sidecars re-register):

```bash
kubectl delete statefulset.apps/dapr-placement-server -n dapr-system
helm upgrade dapr ./charts/dapr -n dapr-system --set global.ha.enabled=true
```

Remember `global.ha.enabled=true` cannot be overridden per service; use `dapr_scheduler.ha` and `dapr_placement.ha` with the global flag false for selective HA.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
