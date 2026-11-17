---
id: computing-software.cloud-infrastructure-engineering.istio.istio-distributed-tracing
name: istio-distributed-tracing
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, distributed-tracing, tracing, trace-headers]
level: practitioner
status: docs-checked
description: "Enable trace export in Istio and propagate trace headers in application code, since sidecars cannot link inbound and outbound requests alone."
sources: ["https://istio.io/latest/docs/tasks/observability/distributed-tracing/overview/", "https://istio.io/latest/docs/reference/config/telemetry/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sidecars create spans but cannot connect an inbound request to the outbound calls the app makes. The app must forward trace headers.

```text
x-request-id  x-b3-traceid  x-b3-spanid  x-b3-parentspanid  x-b3-sampled  x-b3-flags  traceparent  tracestate
```

Enable the exporter via a Telemetry resource and `extensionProviders` (zipkin or opentelemetry) with a low `randomSamplingPercentage`.

Gotchas: the docs say proxies send spans automatically but applications must propagate the headers so the backend can join the spans into one trace. `x-request-id` is an Envoy-specific header used to consistently sample logs and traces. `disableSpanReporting: true` stops spans being reported for the selected workloads but does not affect context propagation or sampling.

Verify: send a request through two services; the tracing UI shows a single trace with spans from both sidecars.

## Checked

2026-11-03. Confirmed in the Istio distributed tracing overview (propagated header list, application must forward headers, Telemetry API selects provider and sampling rate) and the Telemetry reference (`randomSamplingPercentage`, `disableSpanReporting` semantics). Removed: the single-format advice, the 100 percent sampling remark, and the shared-library advice.

Method: documentation only; no commands were run.
