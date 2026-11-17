---
id: computing-software.cloud-infrastructure-engineering.observability.opamp-bridge-and-remote-collector-config
name: opamp-bridge-and-remote-collector-config
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [opamp-bridge, opamp-remote-config, otel-kubernetes, otel-operator, fleet-management]
level: advanced
status: draft
description: "Manage collector fleets with OpAMP: Operator OpAMPBridge CR, capabilities and allowed components, opamp extension and supervisor for non-Kubernetes collectors, and security."
sources: ["https://opentelemetry.io/docs/specs/opamp/", "https://github.com/open-telemetry/opentelemetry-operator/tree/main/cmd/operator-opamp-bridge", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/cmd/opampsupervisor"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OpAMP bridge and remote configuration

OpAMP (Open Agent Management Protocol) lets a server see agent health/effective config and push config. Servers:
vendor fleet managers or self-built using `opamp-go`.

## Kubernetes: Operator OpAMP bridge
The bridge reports and manages `OpenTelemetryCollector` CRs on behalf of the server.
```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: OpAMPBridge
metadata: {name: bridge, namespace: observability}
spec:
  endpoint: wss://opamp.example.com/v1/opamp
  headers: {Authorization: "Secret-Key ${env:OPAMP_KEY}"}
  capabilities:
    AcceptsRemoteConfig: true
    ReportsEffectiveConfig: true
    ReportsHealth: true
    ReportsRemoteConfig: true
    ReportsOwnTraces: false
  componentsAllowed:
    receivers: [otlp, prometheus]
    processors: [memory_limiter, batch, filter, transform]
    exporters: [otlphttp, debug]
```
Only CRs labelled `opentelemetry.io/opamp-reporting: "true"` (report) / `opentelemetry.io/opamp-managed: "true"`
(managed) are included - check label names for your operator version. Pushed configs using components outside
`componentsAllowed` are rejected.

## Outside Kubernetes
- **opamp extension** in the collector: reports status/effective config (read-only).
  `extensions: {opamp: {server: {ws: {endpoint: wss://opamp.example.com/v1/opamp}}}}`
- **opampsupervisor**: a separate process that starts/stops the collector, writes received config, and can restart on
  change. Configure `server.endpoint`, `capabilities.accepts_remote_config: true`, `agent.executable: /usr/bin/otelcol-contrib`.

## Security
Remote config can redirect all telemetry or exfiltrate data: require TLS + strong auth, restrict components
(`componentsAllowed`), keep a Git audit trail on the server side, and stage rollouts (canary group first).

## Verify
Server shows each collector with health and effective config; push a harmless change (batch timeout) to one
collector and confirm `ReportsRemoteConfig` status applied, and the CR in Kubernetes was updated.
