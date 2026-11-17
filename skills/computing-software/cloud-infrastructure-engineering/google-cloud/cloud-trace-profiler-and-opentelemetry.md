---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-trace-profiler-and-opentelemetry
name: cloud-trace-profiler-and-opentelemetry
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-trace, cloud-profiler, opentelemetry, otel, distributed-tracing, trace-context, traceparent, x-cloud-trace-context, otel-collector, sampling, trace-exemplars, latency-analysis, flame-graphs, cpu-profiling, heap-profiling, telemetry-api, trace-explorer, span-attributes]
level: practitioner
status: docs-checked
description: "Instrument with OpenTelemetry for Cloud Trace and Profiler: collector vs direct export, trace headers, sampling hints, per-platform advice, IAM roles, profile types and overhead."
sources: ["https://cloud.google.com/trace/docs/overview", "https://cloud.google.com/trace/docs/setup", "https://cloud.google.com/trace/docs/trace-context", "https://cloud.google.com/profiler/docs/about-profiler", "https://cloud.google.com/stackdriver/docs/instrumentation/choose-approach", "https://github.com/GoogleCloudPlatform/opentelemetry-operations-collector"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Trace, Cloud Profiler and OpenTelemetry

**Goal:** one trace ID follows a request through every service, slow spans are findable in Trace Explorer, and CPU/heap hotspots show up in Profiler.

## 1. Instrument with OpenTelemetry
- Google recommends an open-source, vendor-neutral framework such as OpenTelemetry over vendor-specific client libraries; OpenTelemetry libraries are simpler and export OTLP.
- Two export architectures:
  - Collector-based (recommended where the platform supports a collector): the app uses the OpenTelemetry SDK and an in-process OTLP exporter to send to a collector (the Google-Built OpenTelemetry Collector or an Ops Agent receiver), which forwards to your project through the Telemetry (OTLP) API. App code stays vendor-neutral.
  - Direct export: the SDK sends to the Telemetry API itself; no collector, but the code carries vendor-specific dependencies. Use it where running a collector is impractical.
- Two ingest APIs: the Telemetry API (`telemetry.googleapis.com`, recommended: OpenTelemetry-compatible, often more generous limits) and the Cloud Trace API (`cloudtrace.googleapis.com`). Do not disable the Telemetry API to stop trace storage (it also takes logs and metrics); disable the Cloud Trace API.
- Automatic tracing exists for Cloud Run and Cloud Run functions (latency of incoming and outgoing HTTP requests) and App Engine standard; elsewhere instrument yourself.
- The Google-Built OpenTelemetry Collector is an open-source production-ready build of the upstream collector using upstream components; `otelopscol` backs the Ops Agent and is supported only as part of it.

## 2. Platform recommendations (Choose an instrumentation approach)
| Platform | Traces |
|---|---|
| GKE | Deploy the Google-Built OpenTelemetry Collector; SDK with OTLP exporter |
| Compute Engine | Ops Agent with its OTLP receiver (traces go via the Cloud Trace API) |
| Cloud Run | SDK with OTLP exporter plus an OpenTelemetry sidecar; use instance-based billing so CPU is allocated for the whole instance lifecycle, because instrumentation does background processing |
| Cloud Run functions, App Engine | SDK with OTLP exporter; functions cannot write metrics directly (use log-based metrics) |
Logs: emit JSON-structured logs to stdout/stderr (GKE, Cloud Run, functions, App Engine collect them automatically); on Compute Engine write to a file and use the Ops Agent.

## 3. Context propagation
- W3C `traceparent` is the preferred header: `VERSION-TRACE_ID-PARENT_SPAN_ID-TRACE_FLAGS`; version `00`, 32-hex trace ID, 16-hex parent span ID, flags `01` when the parent sampled. `tracestate` is optional vendor metadata.
- Legacy `X-Cloud-Trace-Context: TRACE_ID/SPAN_ID;o=OPTIONS`, with a decimal span ID and `o=1` meaning the parent was sampled. Google Cloud services typically support both. Prefer `traceparent`; keep the legacy header as a fallback.
- gRPC uses metadata: `traceparent` or `grpc-trace-bin`.
- Propagation is the job of the components that submit data (Google services and your code), not Trace. Support varies by service (Apigee, App Engine, Cloud Endpoints, Cloud Run, Cloud Load Balancing, Cloud Scheduler, Cloud Tasks, Pub/Sub). For OpenTelemetry in Go, call `SetTextMapPropagator` to use W3C `traceparent`.
- Multi-threaded apps must propagate context across threads.

## 4. Sampling
- You cannot force sampling: each component decides independently. Setting the sampled flag in the trace header is only a hint; Google services generally accept it while enforcing their own rate limits.
- With OpenTelemetry use the `ParentBased` sampler so the parent's sampling flag is respected.
- Exemplars link a metric measurement to a trace for correlation.

## 5. Access and auth
- View: `roles/cloudtrace.user`. Write via Cloud Trace API: `roles/cloudtrace.agent`. Write via Telemetry API: `roles/telemetry.writer` (the Telemetry API needs a quota project).
- Cloud Trace and Telemetry APIs are on by default but an organisation policy can disable them. Check the Cloud Trace API access scope on custom-scope VMs and GKE nodes (`https://www.googleapis.com/auth/trace.append`).
- Outside Google Cloud use Application Default Credentials.
- Spans in the `_Trace` bucket are retained for 30 days.
- Analyse in Trace Explorer (heatmap, filters, trace scope across projects) or SQL in Observability Analytics.

## 6. Cloud Profiler
- Statistical, low-overhead continuous profiler for CPU and memory allocation, attributed to source code.
- Profile types: CPU time (Go, Java, Python); heap (Go, Java, Node.js); allocated heap (Go); contention (Go); threads (Go); wall time (Java, Node.js, Python).
- Environments: Compute Engine, GKE, App Engine, Dataflow (Java, Python), Spark (Java), and outside Google Cloud. The agent attaches as a library.
- A profile is typically 10 seconds of data every 1 minute for one instance of a service in a zone; with 10 replicas about 10 profiles appear per 10 minutes. Overhead during collection is under 5 percent, commonly under 0.5 percent amortised.
- Profile data is retained for 30 days; profiles can be downloaded.

## Gotchas
- Using only the legacy header in one service and only `traceparent` in another can split a trace; support both, prefer `traceparent`.
- OpenTelemetry needs CPU after a request returns; on Cloud Run request-based billing this is why the page asks for instance-based billing.

## Checked
Confirmed 2026-11-08 against the Cloud Trace overview, instrument and trace-context pages, the Profiler overview, Choose an instrumentation approach, and the operations-collector repository README. Removed claims the pages do not state: the Python SDK listing and package names, collector YAML and exporter names, tail-sampling and rate advice, load-balancer span behaviour, Pub/Sub attribute propagation, log-trace field names, Profiler agent invocations, per-language flags and the `roles/cloudprofiler.agent` role, and the example `http://otel-collector:4317` endpoint. The stackdriver instrumentation setup source returned 404 and was dropped.
Method: docs-only read of cited pages, 2026-11-08
