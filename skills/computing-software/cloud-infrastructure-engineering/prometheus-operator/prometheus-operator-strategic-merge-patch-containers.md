---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-strategic-merge-patch-containers
name: prometheus-operator-strategic-merge-patch-containers
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [strategic-merge-patch, spec-containers, additionalargs, inject-sidecar, probe-override, gomemlimit]
level: advanced
status: docs-checked
description: "Override or extend operator-generated containers through spec.containers: probe thresholds, env vars, sidecars, extra CLI args and probe handler replacement."
sources: ["https://prometheus-operator.dev/docs/platform/strategic-merge-patch/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Prometheus`, `Alertmanager` and `ThanosRuler` expose `spec.containers`, which is merged with the operator-generated containers by strategic merge patch. You can override fields the CRD does not expose, or inject new containers.

## Patterns
- **Probe threshold:** under `containers` with `name: prometheus`, set `startupProbe.failureThreshold: 500`. For Alertmanager set liveness and readiness `failureThreshold`.
- **Environment variable:** add `env: [{name: GOMEMLIMIT, value: 6Gi}]` to the `prometheus` container.
- **Sidecar:** list a new container (for example `busybox` running `sleep 3600`) and it is added to the StatefulSet.
- **Extra CLI args:** use `spec.additionalArgs` (for example name `scrape.timestamp-tolerance`, value `15ms`). Setting `containers[*].args` instead replaces the whole args list, defaults included.

## Probe handler replacement
With `spec.web.tlsConfig` the operator enforces HTTPS `httpGet` probes; if `web.config` also demands auth such as Basic Auth, those probes fail because `httpGet` cannot send custom headers. Replace the handler with `tcpSocket`, `exec` or `grpc` by patching, e.g. `readinessProbe.tcpSocket.port: 9090` and the same for liveness. Earlier behaviour kept both handlers and the StatefulSet was rejected with `may not specify more than 1 handler type`.

Trade-off: a `tcpSocket` or `exec` probe no longer hits `/-/ready`, so a pod can be Ready before WAL replay finishes.

## Checked

2026-11-08. Read the strategic merge patch page in full. Claims match; no changes needed.

Method: documentation only; no commands were run.
