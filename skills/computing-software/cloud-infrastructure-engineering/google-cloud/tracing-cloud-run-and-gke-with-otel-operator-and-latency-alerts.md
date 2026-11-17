---
id: computing-software.cloud-infrastructure-engineering.google-cloud.tracing-cloud-run-and-gke-with-otel-operator-and-latency-alerts
name: tracing-cloud-run-and-gke-with-otel-operator-and-latency-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-trace, cloud-run-tracing, trace-cloud-run-gke, otel-operator, otel-collector-gke, trace-latency-alerts, opentelemetry, spanmetrics]
level: advanced
status: docs-checked
description: "Get end-to-end traces in Cloud Trace from Cloud Run and GKE using OpenTelemetry (SDK exporters, OTel Operator, collector), and derive latency metrics from spans."
sources: ["https://cloud.google.com/trace/docs/setup", "https://cloud.google.com/run/docs/trace", "https://cloud.google.com/stackdriver/docs/instrumentation/opentelemetry-collector-gke", "https://opentelemetry.io/docs/kubernetes/operator/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/spanmetricsconnector"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tracing Cloud Run and GKE with OpenTelemetry

## 1. Cloud Run
Incoming requests to Cloud Run services generate traces automatically, and the W3C `traceparent` header is populated.
Automatic traces are not billed; spans you add with Cloud Trace libraries are billed as normal Cloud Trace usage.
Cloud Run samples at a limited per-instance rate and does not let you configure it.
Add instrumentation when you need custom spans or want trace context propagated so a multi-service request shows as one trace.

Recommended path (Cloud Trace setup page): instrument with OpenTelemetry, send OTLP to a collector, and have the collector send
to your project through the Telemetry (OTLP) API. Alternatives: OTLP direct to the Telemetry API, or the Cloud Trace exporter.
Roles on the runtime service account: `roles/cloudtrace.agent` to write through the Cloud Trace API, `roles/telemetry.writer` to
write through the Telemetry API. To view traces: `roles/cloudtrace.user`.

## 2. GKE
- The OpenTelemetry Operator manages collectors and workload auto-instrumentation. It needs cert-manager first; install with
  `kubectl apply -f https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml`
  (pin a release in production instead of `latest`). Then create an `OpenTelemetryCollector` resource (`apiVersion: opentelemetry.io/v1beta1`)
  with an `otlp` receiver, a `memory_limiter` processor and your exporter.
- Google's own collector deployment (otlp-k8s-ingest, deployed with `kubectl kustomize ... | envsubst | kubectl apply -f -`) uses the
  `googlecloud` exporter and an `otlphttp` exporter to `https://telemetry.googleapis.com` with the `googleclientauth` extension.
  Its config also sets `gcp.project_id`, `memory_limiter` and `batch`; Google advises adding to it, not removing elements.
- Grant the collector's Kubernetes service account `roles/monitoring.metricWriter`, `roles/logging.logWriter` and
  `roles/cloudtrace.agent` (Workload Identity principal on the project).
- Sampling: you cannot force sampling; each component decides independently. Set the sampled flag in the trace header as a hint and use the
  OpenTelemetry `ParentBased` sampler so children respect the parent decision.

## 3. Latency metrics from traces
The OpenTelemetry Collector Contrib span metrics connector turns spans into request-count and duration histograms (per service, span name,
span kind and status). The component was renamed from `spanmetrics` to `span_metrics`; the old name still works but is deprecated.
Histogram type is `explicit` (default) or `exponential`, and the buckets are configurable. Export the metrics to Managed Service for
Prometheus or Cloud Monitoring and alert on a high quantile of the duration histogram for server spans. Check the exact exported
metric name in Metrics Explorer before writing the alert.

## Gotchas
- A collector without `memory_limiter` is at risk under bursts; keep it in every pipeline.
- Context must be propagated by your code across service boundaries (including queues) or the trace breaks.
- Tracing a Compute Engine host can use the Ops Agent OTLP receiver instead of a collector.

## Checked
2026-11-09. Confirmed against the Cloud Run distributed tracing page, Cloud Trace "Instrument" page (approaches, roles, ParentBased and sampled-flag hint),
Google-built collector on GKE page (roles, exporters, otlp-k8s-ingest command), OpenTelemetry Operator page (cert-manager, install command, v1beta1
OpenTelemetryCollector) and the span metrics connector README (rename, histogram types). Removed unconfirmed: X-Cloud-Trace-Context/gcp propagator
detail, logging trace field format, Instrumentation CR and inject annotations, sampler ratio, PromQL expression and metric name, tail-sampling advice, and the
Cloud Run per-instance sampling figure.
Method: documentation only; no commands were run.

## Verify
- [ ] A request through the load balancer and Cloud Run to GKE shows one trace with all spans in Trace Explorer.
- [ ] The latency alert fires on a synthetic slow endpoint.
