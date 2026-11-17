---
id: computing-software.cloud-infrastructure-engineering.contour.contour-envoy-graceful-shutdown-manager
name: contour-envoy-graceful-shutdown-manager
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [shutdown-manager, prestop, terminationgraceperiodseconds, drain, healthcheck-fail, min-open-connections, redeploy-envoy]
level: advanced
status: docs-checked
description: "Redeploying Envoy without dropping connections: shutdown-manager sidecar, preStop hooks, serve-port, ready-file, and shutdown flags check-interval, drain-delay."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/redeploy-envoy.md", "https://github.com/projectcontour/contour/blob/main/site/content/docs/main/deploy-options.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Envoy graceful shutdown (shutdown-manager)

Goal when redeploying Envoy: stop new connections, drain existing ones by POSTing to `/healthcheck/fail`, and wait for them to finish before Kubernetes sends SIGTERM.

`contour envoy shutdown-manager` runs as a second container in the Envoy pod:

```yaml
- name: shutdown-manager
  command: [/bin/contour]
  args: [envoy, shutdown-manager]
  lifecycle:
    preStop:
      exec:
        command: [/bin/contour, envoy, shutdown]
```

The Envoy container's `preStop` hook calls the shutdown-manager's `/shutdown` endpoint, which blocks until connections drain, keeping Envoy alive. Set the pod's `terminationGracePeriodSeconds` high enough: it is the upper bound for long-lived sessions, after which the pod is killed.

shutdown-manager options: `serve-port` (8090), `ready-file` (`/admin/ok`, polled while waiting).

`contour envoy shutdown` options:
- `check-interval` (5s): how often to poll Envoy for open connections.
- `check-delay` (0s): wait before first poll.
- `drain-delay` (0s): wait before draining begins.
- `min-open-connections` (0): drain completes when open connections fall to this number.
- `admin-address` (`/admin/admin.sock`, a unix socket; `admin-port` deprecated), `ready-file` (`/admin/ok`, written when done).

DaemonSets do not run proper `preStop` on node scale-down, so consider the Envoy Deployment model when nodes come and go.

## Checked

2026-11-04. Confirmed against the Contour redeploy Envoy page (redeploy-envoy.md); the DaemonSet preStop remark is from deploy-options.md: the fields, defaults, flags and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
