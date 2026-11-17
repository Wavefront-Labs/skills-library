---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-sampling-strategy-types
name: jaeger-sampling-strategy-types
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, head-based-sampling, tail-based-sampling, remote-sampling, probabilistic-sampler]
level: practitioner
status: docs-checked
description: "Compare head-based, tail-based and remote sampling in Jaeger and the probabilistic and rate-limiting samplers."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/sampling/
  - https://www.jaegertracing.io/docs/2.22/operations/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose a sampling approach to control application overhead and storage cost.

- Head-based: the decision is made at the start of a trace, built into the OpenTelemetry SDKs.
- Tail-based: the decision is made after the trace is complete and all spans are collected, giving finer control over what is kept. Downsides: runtime overhead on the application, which must record and export all traces, and higher memory and processing cost in the Jaeger backend. Jaeger supports it through a tail sampling processor.
- Remote sampling: a form of head-based sampling where the SDKs fetch the strategy from the Jaeger backend, consolidating policies in one place. Jaeger's `remote_sampling` extension defines distinct rates per service and endpoint, either periodically loaded from a file or dynamically calculated from traffic.

The two basic head samplers used by remote sampling:
- Probabilistic: a random decision with a set probability; `probability=0.1` samples about 1 in 10 traces.
- Rate limiting: a leaky bucket gives a constant rate; `rate=2.0` samples 2 traces per second.

Related: the OpenTelemetry SDKs default to the `parentbased_always_on` sampler (effectively 100 percent), changeable through the `OTEL_TRACES_SAMPLER` environment variable.

## Checked

2026-11-03. Confirmed against the Sampling page: head-based, tail-based (with its two downsides and the tail sampling processor) and remote sampling definitions, and the probabilistic and rate limiting samplers with their examples. The parentbased_always_on default and OTEL_TRACES_SAMPLER are from the Troubleshooting page. Nothing removed.
Method: documentation only; no commands were run.
