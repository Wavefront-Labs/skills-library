---
id: computing-software.cloud-infrastructure-engineering.thanos.tracing-configuration
name: tracing-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-tracing, tracing-config, otlp, jaeger]
level: practitioner
status: docs-checked
description: "Enable request tracing for any Thanos component with --tracing.config and pick a backend."
sources: ["https://thanos.io/tip/thanos/tracing.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tracing configuration

Every component accepts `--tracing.config-file` (path) or `--tracing.config` (inline YAML). The docs recommend inline for a static per-component view.

Backends documented, by `type`: `OTLP` (OpenTelemetry), `JAEGER`, `GOOGLE_CLOUD` (formerly Stackdriver), `ELASTIC_APM` and `LIGHTSTEP`.

```yaml
type: JAEGER
config:
  service_name: ""
  sampler_type: ""
  sampler_param: 0
  agent_host: ""
  agent_port: 0
```

In Kubernetes, multiline inline flags work, for example a `--tracing.config=` argument followed by a YAML block in the container args.

Once enabled, Thanos generates traces for all gRPC and HTTP APIs through generic middleware, with extra low-level spans for APIs such as `query` and `query_range`. The Querier's gRPC calls to other components appear as child spans.

**Finding trace IDs.** Search in the tracing UI by labels, time or latency; use exemplars; or read the trace ID from a response header of a sampled request. Sending the header `X-Thanos-Force-Tracing` on a request forces it to be sampled when a backend is configured.

**Verify.** Run a `query_range` call and confirm a single trace spans the Querier and its stores.

## Checked

2026-11-08. Read in full the raw Thanos tracing page (docs/tracing.md): config flags, inline-config recommendation, backend types and the Jaeger fields, the GOOGLE_CLOUD/STACKDRIVER note, usage and spans, trace ID discovery, and X-Thanos-Force-Tracing. Nothing removed.

Method: documentation only; no commands were run.
