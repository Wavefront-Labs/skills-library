---
id: computing-software.cloud-infrastructure-engineering.kyverno.tracing
name: tracing
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [tracing, opentelemetry, otlp, jaeger, grafana-tempo, admission-spans]
level: practitioner
status: docs-checked
description: "Enable Kyverno tracing per controller via Helm, point it at an OTLP gRPC backend such as Jaeger or Tempo, and read the ADMISSION root spans."
sources:
  - https://kyverno.io/docs/guides/tracing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tracing is off by default. In Helm, each of `admissionController`, `backgroundController`, `cleanupController` and `reportsController` has its own `tracing.enabled`, `tracing.address` (backend host) and `tracing.port`; the examples use port `4317`, the OTLP gRPC receiver. Backends named: Jaeger, Grafana Tempo, Datadog. Kubernetes, registry and cosign clients are instrumented and propagate trace context.

Sampling: Kyverno samples every incoming request and its sampler is not configurable; do sampling in an OpenTelemetry Collector at the cost of complexity.

Jaeger walkthrough: Jaeger all-in-one chart in namespace `monitoring` with in-memory storage; Kyverno points at `jaeger-collector.monitoring` port 4317. Tempo walkthrough: Tempo registered in Grafana at `tempo.monitoring:3100`, Kyverno pointed at `tempo.monitoring` port 4317.

Reading traces: service name is `kyverno`. Root spans are named `ADMISSION <HTTP OPERATION> <HTTP PATH>`, for example `ADMISSION POST /validate/fail` (`/validate/fail` is a validating webhook in the default fail mode). Child spans cover each policy and rule checked, though not every rule is necessarily evaluated. Search by service `kyverno` and that span name.

Test with `Enforce` policies: `Audit` policies run asynchronously and produce a separate trace. The page does not document other span attributes.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
