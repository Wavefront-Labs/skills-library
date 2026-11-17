---
id: computing-software.messaging-and-integration.dapr.kubernetes-production-resource-settings
name: kubernetes-production-resource-settings
category: computing-software
field: messaging-and-integration
product: dapr
tags: [kubernetes, production, resources, gomemlimit, sidecar, helm, annotations]
level: practitioner
status: docs-checked
description: "Size Dapr on Kubernetes: starting CPU and memory for operator, injector, sentry and placement, sidecar resource annotations, and the GOMEMLIMIT soft limit at 90 percent."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/kubernetes/kubernetes-production.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Control plane starting points from the page (test and tune for your cluster; the page suggests not adding memory limits to control plane components in production):

| Deployment | CPU | Memory |
|---|---|---|
| Operator | Limit 1, Request 100m | Request 100Mi |
| Sidecar Injector | Limit 1, Request 100m | Request 30Mi |
| Sentry | Limit 1, Request 100m | Request 30Mi |
| Placement | Limit 1, Request 250m | Request 75Mi |

The Helm chart sets no defaults; each component has a `resources` option such as `dapr_dashboard.resources`. Placement (actors), Sentry (mTLS) and Dashboard are optional.

Sidecar resources come from pod annotations: `dapr.io/sidecar-cpu-limit`, `dapr.io/sidecar-memory-limit`, `dapr.io/sidecar-cpu-request`, `dapr.io/sidecar-memory-request`. Unset means no limits, which the page says may cause issues. Suggested production sidecar: CPU limit 300m / request 100m; memory limit 1000Mi / request 250Mi. Baseline with a monitoring tool and adjust.

With a memory limit, also set a Go soft limit so the garbage collector frees memory before the heap doubles:

```yaml
  annotations:
    dapr.io/enabled: "true"
    dapr.io/app-id: "nodeapp"
    # our daprd memory settings
    dapr.io/sidecar-memory-limit: "1000Mi"   # your memory limit
    dapr.io/env: "GOMEMLIMIT=900MiB"         # 90% of your memory limit. Also notice the suffix "MiB" instead of "Mi"
```

Note the suffix difference: GOMEMLIMIT takes `B`, `KiB`, `MiB`, `GiB`, `TiB`.

## Checked

2026-11-04. Resource tables, annotations and the GOMEMLIMIT example confirmed on the Production guidelines on Kubernetes page.

Method: documentation only; no commands were run.
