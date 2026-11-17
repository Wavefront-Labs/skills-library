---
id: computing-software.devops-ci-cd.flagger.flagger-canary-service-config
name: flagger-canary-service-config
category: computing-software
field: devops-ci-cd
product: flagger
tags: [canary, service, clusterip, ports, routing]
level: practitioner
status: docs-checked
description: "Configure the Kubernetes services Flagger generates from a Canary: names, port discovery, headless services, metadata, retries and timeouts."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/how-it-works.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `service` block describes how the target is exposed. Flagger creates ClusterIP services:
- `<name>.<ns>.svc.cluster.local` selecting `app=<name>-primary`
- `<name>-primary.<ns>...` selecting `app=<name>-primary`
- `<name>-canary.<ns>...` selecting `app=<name>` (available during analysis, handy for conformance and load tests)

```yaml
spec:
  service:
    name: podinfo
    port: 9898
    portName: http
    appProtocol: http
    targetPort: 9898
    portDiscovery: true
    headless: false
    trafficDistribution: PreferClose
```

The container port must match `port` or `targetPort`. `name` defaults to `targetRef.name`; `portName` defaults to `http` (use `grpc` for gRPC). With `portDiscovery` Flagger scans the workload containers' ports (excluding the canary port and mesh sidecar ports) for the generated services.

Metadata for generated services goes under `apex`, `canary` and `primary` (`annotations` and `labels`). `apex` metadata is also applied to the mesh or ingress object, which makes external-dns work with Istio VirtualServices and TraefikServices. Anything else added to those objects is removed on reconcile unless listed under `unmanagedMetadata`.

Routing options include `match` (URI prefix), `rewrite`, `retries` (`attempts`, `perTryTimeout`), `timeout`, and `backendTimeout` (Gateway API only).

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/how-it-works.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
