---
id: computing-software.cloud-infrastructure-engineering.contour.contour-envoy-stuck-draining-fix
name: contour-envoy-stuck-draining-fix
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [envoy-draining, unready, shutdown-manager, liveness-probe, kubectl-delete, issue-4851]
level: advanced
status: docs-checked
description: "Fix Envoy containers stuck unready and draining after a shutdown-manager restart: delete the pod, set requests, change liveness probes."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/troubleshooting/envoy-container-draining.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Envoy stuck in unready/draining state

Cause: an unintended side effect of the kubelet restarting the shutdown-manager sidecar (Contour issue 4851), leaving Envoy draining and never ready again.

Immediate fix: `kubectl delete` the affected pods so replacements are created.

Prevention:
- Set resource requests on all containers.
- Make sure the shutdown-manager container has no liveness probe (removed from the example YAML in Contour 1.24.0).
- If that is not enough, add a liveness probe to the Envoy container itself:

```yaml
livenessProbe:
  httpGet:
    path: /ready
    port: 8002
  initialDelaySeconds: 15
  periodSeconds: 5
  failureThreshold: 6
```

With this, the kubelet restarts Envoy if it gets stuck. A graceful drain may or may not occur in that case, depending on the sequence of events before the probe fails.

## Checked

2026-11-08: read the Contour docs troubleshooting/envoy-container-draining in full. Confirmed: cause (shutdown-manager restarted by the kubelet, issue 4851), kubectl delete, resource requests, no shutdown-manager liveness probe (removed from the example YAML in 1.24.0), the Envoy /ready liveness probe values, and the graceful-drain caveat. Removed: the overload-manager paragraph and the OOM rationale, which are not in this page.

Method: documentation only; no commands were run.
