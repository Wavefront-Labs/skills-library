---
id: computing-software.devops-ci-cd.flagger.flagger-zero-downtime-rollouts
name: flagger-zero-downtime-rollouts
category: computing-software
field: devops-ci-cd
product: flagger
tags: [zero-downtime, probes, graceful-shutdown, rolling-update]
level: practitioner
status: docs-checked
description: "Prepare deployments for Flagger promotions with maxUnavailable zero, liveness and readiness probes and graceful shutdown settings."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/tutorials/zero-downtime-deployments.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Things to set on high-traffic production workloads to minimise the impact of rolling updates and downscaling:

- Limit unavailable pods and fail faster than the default ten minute progress deadline:

```yaml
spec:
  progressDeadlineSeconds: 120
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
```

- Liveness probe: an HTTP endpoint (for example `/healthz`) to detect an unrecoverable broken state. If mTLS is enabled use `exec` probes (for example `wget --spider`), since the kubelet is outside the mesh and has no access to the TLS certificate.
- Readiness probe: an endpoint such as `/readyz`; if the app depends on external services, check them before accepting traffic. The Envoy sidecar can start more slowly than the app.
- Graceful shutdown: Kubernetes sends SIGTERM and waits 30s by default; handle SIGTERM and raise `terminationGracePeriodSeconds` (the example uses 60) with a `lifecycle` hook if requests need draining.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/tutorials/zero-downtime-deployments.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
