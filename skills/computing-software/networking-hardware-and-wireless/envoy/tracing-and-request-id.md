---
id: computing-software.networking-hardware-and-wireless.envoy.tracing-and-request-id
name: tracing-and-request-id
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, tracing, x-request-id, x-client-trace-id, zipkin, jaeger, datadog, skywalking, opentelemetry]
level: practitioner
status: docs-checked
description: "Enable Envoy request ID generation, client trace ID joining and an external tracer, and know which tracers ship in the tree."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/observability/tracing.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tracing and request id
Envoy has three tracing-related features:
- Request ID generation: Envoy makes UUIDs where needed and fills `x-request-id`. Applications should forward it so logs and traces correlate. Behaviour is configurable per HCM through an extension.
- Client trace ID joining: `x-client-trace-id` joins an untrusted client request id to the trusted internal `x-request-id`.
- External trace service: in-tree tracers include Zipkin, Jaeger, Datadog, SkyWalking, AWS X-Ray and Fluentd; Instana comes as a third-party plugin.

```yaml
tracing:
  provider:
    name: envoy.tracers.zipkin
    typed_config:
      "@type": type.googleapis.com/envoy.config.trace.v3.ZipkinConfig
      collector_cluster: zipkin
      collector_endpoint: /api/v2/spans
      collector_endpoint_version: HTTP_JSON
```
(The `tracing` block sits inside the HCM `typed_config`; the cluster `zipkin` must exist.)

Gotchas: Envoy sanitizes `x-request-id` and `x-envoy-force-trace` on external requests unless the request is internal (see header sanitizing), so an edge must set `use_remote_address`. Applications that do not propagate trace headers break the span chain. Verify with a sampled request appearing in the collector.

## Checked

2026-11-03. Confirmed against: tracing.rst (request id, x-client-trace-id, tracer list) and zipkin.proto (collector_cluster, collector_endpoint, HTTP_JSON). Removed or corrected: the stats filter verify step and the version hedge.

Method: documentation only; no commands were run.
