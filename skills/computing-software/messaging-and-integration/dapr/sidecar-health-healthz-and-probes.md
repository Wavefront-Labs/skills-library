---
id: computing-software.messaging-and-integration.dapr.sidecar-health-healthz-and-probes
name: sidecar-health-healthz-and-probes
category: computing-software
field: messaging-and-integration
product: dapr
tags: [health-checks, healthz, readiness, liveness, kubernetes, block-shutdown-duration, graceful-shutdown, sdk]
level: practitioner
status: docs-checked
description: "Use the Dapr sidecar healthz and healthz/outbound endpoints, DAPR_HEALTH_TIMEOUT, the probes the injector sets on Kubernetes, and shutdown delay annotations."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/resiliency/health-checks/sidecar-health.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The sidecar exposes `v1.0/healthz`, which succeeds only when all components are initialized, the Dapr HTTP port is available and the app channel is initialized. `DAPR_HEALTH_TIMEOUT` controls how long a wait for it lasts, useful in higher-latency environments.

`v1.0/healthz/outbound` succeeds earlier: components initialized and HTTP port available, but the app channel not yet established. That is the check for an app that needs Dapr APIs during its own startup; SDKs expose it as `waitForSidecar` / `wait_until_ready` (documented for the .NET, Java, Python and JavaScript SDKs).

On Kubernetes the Sidecar Injector adds these probes to the sidecar automatically (Dapr HTTP port 3500):

```yaml
    livenessProbe:
      httpGet:
        path: v1.0/healthz
        port: 3500
      initialDelaySeconds: 5
      periodSeconds: 10
      timeoutSeconds : 5
      failureThreshold : 3
    readinessProbe:
      httpGet:
        path: v1.0/healthz
        port: 3500
      initialDelaySeconds: 5
      periodSeconds: 10
      timeoutSeconds : 5
      failureThreshold: 3
```

Any HTTP code from 200 to 399 counts as success. The sidecar is ready once the app is reachable on its configured port, and the app cannot use components during its own startup before then.

Delay shutdown for apps that call Dapr while stopping: `dapr.io/block-shutdown-duration` (CLI `--dapr-block-shutdown-duration`) holds the full shutdown for that duration or until the app reports unhealthy; during it all subscriptions and input bindings are closed. Related: `dapr.io/graceful-shutdown-seconds` (`--dapr-graceful-shutdown-seconds`).

Actors have their own health endpoint, in the actor API, which probes the actor app.

## Checked

2026-11-08. healthz and healthz/outbound semantics, DAPR_HEALTH_TIMEOUT, SDK wait methods, the injected probe values, the 200-399 success range, the ready-state note and the shutdown delay flags confirmed on the Sidecar health page. All claims unchanged.

Method: documentation only; every cited page read in full; no commands were run.
