---
id: computing-software.messaging-and-integration.dapr.app-health-checks
name: app-health-checks
category: computing-software
field: messaging-and-integration
product: dapr
tags: [health-checks, app-health, probe-interval, threshold, pubsub, input-bindings, actors, kubernetes]
level: practitioner
status: docs-checked
description: "Enable Dapr app health checks: flags and annotations, 5 s interval, 500 ms timeout, threshold 3, what Dapr pauses while the app is unhealthy, and the Kubernetes caveat."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/resiliency/health-checks/app-health.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
App health checks are off by default. When enabled the sidecar polls the app over HTTP or gRPC. On failure Dapr temporarily stops sending work: it unsubscribes from all pub/sub subscriptions, stops all input bindings, short-circuits service invocation requests inside the runtime, and unregisters actor types so instances migrate to another replica. It resumes when the app is healthy again.

They complement, not replace, platform liveness probes. They are the "soft" option (pause work for a busy app) while liveness probes restart. On Kubernetes a failing Dapr check does not remove the pod from service discovery.

Options (flag / annotation, default):

- `--enable-app-health-check` / `dapr.io/enable-app-health-check`: disabled; this alone is enough.
- `--app-health-check-path` / `dapr.io/app-health-check-path`: path probed on HTTP app channels, ignored for gRPC. The page's options table lists `/healthz` as the default while its prose says `/health`, so set the path explicitly.
- `--app-health-probe-interval` / `dapr.io/app-health-probe-interval`: seconds, `5`.
- `--app-health-probe-timeout` / `dapr.io/app-health-probe-timeout`: milliseconds, `500`.
- `--app-health-threshold` / `dapr.io/app-health-threshold`: consecutive failures, `3`.
- `--app-protocol` / `dapr.io/app-protocol`: `http`, `grpc`, `https`, `grpcs`, `h2c`.

HTTP is healthy on any 200-299 status. For gRPC apps Dapr calls `/dapr.proto.runtime.v1.AppCallbackHealthCheck/HealthCheck`. At startup Dapr waits for a first successful probe before enabling subscriptions, bindings and invocation. A single success restores health; thresholds apply to failures only. If load causes false unhealthy results raise the timeout.

```sh
dapr run \
  --app-id my-app \
  --app-port 7001 \
  --app-protocol http \
  --enable-app-health-check \
  --app-health-check-path=/healthz \
  --app-health-probe-interval 3 \
  --app-health-probe-timeout 200 \
  --app-health-threshold 2 \
  -- \
    <command to execute>
```

## Checked

2026-11-08. Options, defaults, pause behaviour, 200-299 rule, gRPC method, first-probe wait, threshold semantics and both examples confirmed on the App health checks page. Changed: the page contradicts itself on the default path (table `/healthz`, prose `/health`), now stated. Other claims unchanged.

Method: documentation only; every cited page read in full; no commands were run.
