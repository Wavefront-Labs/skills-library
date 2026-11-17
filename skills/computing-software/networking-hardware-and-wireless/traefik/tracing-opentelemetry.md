---
id: computing-software.networking-hardware-and-wireless.traefik.tracing-opentelemetry
name: tracing-opentelemetry
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, tracing, opentelemetry, otlp, samplerate, safequeryparams]
level: practitioner
status: docs-checked
description: "Enable OpenTelemetry tracing in Traefik with sample rate, captured headers, resource attributes and query parameter redaction."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/observability/tracing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tracing opentelemetry
Tracing options: `addInternals`, `serviceName`, `resourceAttributes`, `sampleRate` (0.0 to 1.0, parent-based so an upstream sampling decision wins), `capturedRequestHeaders`, `capturedResponseHeaders`, `safeQueryParams` and `otlp.http.endpoint` (gRPC is also an option under otlp).

```yaml
tracing:
  serviceName: traefik-edge
  sampleRate: 0.1
  capturedRequestHeaders:
    - X-Request-Id
  otlp:
    http:
      endpoint: http://otel-collector:4318/v1/traces
```
Query parameters are redacted in spans by default; list the safe ones in `safeQueryParams`. Router-level `observability.traceVerbosity` (minimal or detailed) and entrypoint `observability.tracing` control detail per route.

Gotchas: `sampleRate` defaults to 1.0; root spans follow it and child spans inherit the sampling decision of the incoming trace context. `tracing.addInternals` (default false) traces internal resources such as `ping@internal`. The gRPC exporter defaults to `localhost:4317`.

## Checked
2026-11-03. Confirmed against the Traefik tracing reference page: tracing options and defaults, parent-based `sampleRate`, `safeQueryParams` redaction, the OTLP HTTP and gRPC exporters, and entrypoint and router `traceVerbosity`. Removed: the overhead, secrets and dropped-span claims and the traceparent Verify step.
Method: documentation only; no commands were run.


