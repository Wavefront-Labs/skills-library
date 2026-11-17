---
id: computing-software.cloud-infrastructure-engineering.istio.istio-telemetry-api
name: istio-telemetry-api
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, telemetry-api, telemetry, extensionproviders]
level: practitioner
status: docs-checked
description: "Set mesh, namespace and workload telemetry (tracing providers, sampling, custom tags) with Telemetry resources and field-level override inheritance."
sources: ["https://istio.io/latest/docs/tasks/observability/telemetry/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Telemetry resources inherit down a hierarchy: the root configuration namespace (typically `istio-system`, mesh-wide, no workload selector), then a namespace-scoped resource with no selector, then a namespace-scoped resource with a workload selector.

Providers are defined in MeshConfig `extensionProviders`; Istio ships `prometheus` (metrics), `stackdriver` (legacy and limited tracing) and `envoy` (access logging).

```yaml
# meshConfig.extensionProviders entry
- name: "localtrace"
  zipkin: {service: "zipkin.istio-system.svc.cluster.local", port: 9411, maxTagLength: 56}
---
apiVersion: telemetry.istio.io/v1
kind: Telemetry
metadata: {name: mesh-default, namespace: istio-system}
spec:
  tracing:
  - providers: [{name: localtrace}]
    randomSamplingPercentage: 100
    customTags: {foo: {literal: {value: bar}}}
```

Override rules: any field set in a child resource completely replaces that field from its parent, including provider selection. In the task, a namespace resource that sets only `customTags` (`userId` from the `userId` header) keeps the parent's provider and sampling but drops the parent's `foo: bar` tag. A workload override uses `selector.matchLabels` (for example `service.istio.io/canonical-name: frontend`); `disableSpanReporting: true` stops spans being reported while tracing headers are still forwarded.

Gotchas: only one mesh-wide Telemetry in the root namespace, and a workload selector there is ignored or rejected. Two Telemetry resources selecting the same workload, or two selector-less ones in one namespace, are invalid (the behaviour is undefined). If you use Sidecar configuration, add the provider's service to it. Providers do not support `$(HOST_IP)`.

## Checked

2026-11-03. Confirmed against the Istio Telemetry API page: hierarchy, override semantics, provider examples and defaults, workload selection rules. Removed: the unsourced `otel` provider name in the example (replaced with the page's `localtrace`), the `istioctl proxy-config bootstrap` verify step, sampling and governance advice.
Method: documentation only; no commands were run.
