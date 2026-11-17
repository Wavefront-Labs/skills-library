---
id: computing-software.cloud-infrastructure-engineering.kubernetes.service-mesh-observability-integration
name: service-mesh-observability-integration
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service-mesh, observability, istio, linkerd, cilium, kiali, hubble, prometheus, grafana, jaeger, opentelemetry, distributed-tracing, golden-signals, access-logs]
level: advanced
status: docs-checked
description: "Wiring mesh telemetry (metrics, traces, access logs) from Istio, Linkerd and Cilium into Prometheus, Grafana, Kiali or Hubble and a tracing backend, and where it misleads."
sources: ["https://istio.io/latest/docs/reference/config/metrics/", "https://istio.io/latest/docs/ops/integrations/prometheus/", "https://istio.io/latest/docs/tasks/observability/distributed-tracing/overview/", "https://istio.io/latest/docs/tasks/observability/distributed-tracing/sampling/", "https://istio.io/latest/docs/tasks/observability/metrics/customize-metrics/", "https://linkerd.io/2-edge/tasks/external-prometheus/", "https://linkerd.io/2-edge/tasks/distributed-tracing/", "https://docs.cilium.io/en/stable/observability/metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service mesh observability integration

**Goal:** get metrics, traces and flow logs out of whichever mesh you run into the
dashboards your team already uses, and know the specific ways mesh-generated telemetry
lies to you if you don't account for the proxy hop.

## 1. Metrics: the proxy, not the app, is the source
- **Istio**: every Envoy proxy (sidecar, gateway, waypoint) and ztunnel emits Prometheus metrics;
  `istio_requests_total` is the request counter and the full standard set is in Istio's metrics
  reference. Istio's documented Prometheus integration scrapes through the standard `prometheus.io`
  annotations (with merged metrics); the demo addons (`samples/addons/prometheus.yaml`,
  `grafana.yaml`, `kiali.yaml`) provide Prometheus, the Istio mesh and service Grafana dashboards,
  and Kiali for evaluation, not as a production Prometheus.
- **Linkerd**: `linkerd viz` installs its own Prometheus by default — **decide early**
  whether to point it at your existing Prometheus (the viz `prometheusUrl` value) or run a
  second one; a second always-on Prometheus per mesh is a real cost line, not a rounding
  error, at scale.
- **Cilium/Hubble**: enable Hubble metrics with the `hubble.metrics.enabled` Helm value; the chart
  creates a headless `hubble-metrics` Service annotated for Prometheus scraping.
- **Double-counting gotcha**: a request between two meshed pods generates metrics from
  *both* the client-side and server-side proxy. Dashboards built from `istio_requests_total`
  must filter on `reporter=destination` (or `source`) consistently, or you'll see request
  counts roughly double actual traffic.

## 2. Distributed tracing
- Istio proxies send spans, but the application must copy the inbound trace headers onto its
  outbound requests or the spans cannot be joined into one trace. Istio's docs list `x-request-id`,
  `traceparent` and `tracestate` for all applications, plus the B3 headers (`x-b3-*`) when using
  Zipkin. If traces are fragmented, first check that the application forwards the headers.
- Point the mesh at an OpenTelemetry Collector rather than directly at a backend where possible:
  Istio supports an OpenTelemetry extension provider (declared under `meshConfig.extensionProviders`)
  and most tracing backends now accept OTLP, so sampling and processing live in one place.
- Sampling: in Istio, use the Telemetry API (`randomSamplingPercentage`, scoped mesh-wide, per
  namespace or per workload); Istio's sampling page also lists mesh-config and per-pod
  `proxy.istio.io/config` options. For Linkerd, follow its distributed-tracing guide (install a trace collector, enable tracing, have
  the application emit spans); the `linkerd-jaeger` extension was deprecated and removed as of
  Linkerd 2.19. Choose the sampling rate deliberately.

## 3. Service graphs and flow visibility
- **Kiali** (Istio): shows the service graph and Istio configuration validation messages
  (Istio's Kiali task notes that `istioctl analyze` offers analysis usable in a CI pipeline and that
  the two approaches are complementary).
- **Hubble UI** (Cilium): a web interface that discovers the service dependency graph at L3/L4 and
  L7 from flow data and shows it as a service map; Hubble metrics still feed Prometheus.
- Neither tool replaces access logs for forensic debugging of a single request — enable
  access logs for anything beyond aggregate dashboards (Istio: `meshConfig.accessLogFile` or the
  Telemetry API; Linkerd: the `config.linkerd.io/access-log` annotation) and ship them through
  your normal log pipeline, not a mesh-specific one.

## 4. Gotchas
- Mesh-level golden-signal dashboards measure the **proxy's** view of latency, which includes its
  own processing time. Istio's performance page notes that telemetry filters have a moderate impact
  on latency, so do not diff mesh-reported p99 against app-reported p99 and call the gap a bug
  without accounting for the proxy; measure your own overhead.
- Cardinality: Istio's standard metrics carry labels such as `source_workload` and
  `destination_workload`. The Telemetry API (`metrics` with `tagOverrides`) lets you customize
  dimensions, so drop labels you do not query on instead of storing everything.

## Verify
- [ ] A single Prometheus (or federated set) holds mesh metrics with `reporter` filtering
  understood by whoever builds dashboards on it.
- [ ] A test request's trace shows up end-to-end in the tracing backend, confirming header
  propagation through at least one app hop, not just proxy-to-proxy.
- [ ] Sampling rate is a deliberate, documented number, not whatever the default shipped
  with.
- [ ] Someone can answer "was this specific request allowed or denied, and by which
  policy" from logs/Hubble/Kiali without guessing.

## Checked

2026-10-27. Release: Istio documentation tree (istio.io, supported releases up to 1.31, October 2026); Linkerd 2-edge docs; Cilium stable docs
- Confirmed `istio_requests_total` and the `reporter` label values (`destination` for server-side proxy, `source` for client-side) in the Istio metrics reference, and the standard `prometheus.io` annotation scraping and demo addons in the Prometheus integration page.
- Confirmed the Istio trace-header list (`x-request-id`, `traceparent`, `tracestate`, B3 for Zipkin), the OpenTelemetry extension provider, and Telemetry API sampling in the tracing pages.
- Corrected Linkerd tracing: the `linkerd-jaeger` extension was deprecated and removed as of Linkerd 2.19 (Linkerd tracing guide); confirmed the viz `prometheusUrl` value and the `config.linkerd.io/access-log` annotation.
- Confirmed `hubble.metrics.enabled`, the `hubble-metrics` service and the Hubble UI service map in the Cilium docs. Removed unsupported latency figures, the Istio 1.12 Telemetry version claim and unverified comparisons.

Method: documentation only; no commands were run.
