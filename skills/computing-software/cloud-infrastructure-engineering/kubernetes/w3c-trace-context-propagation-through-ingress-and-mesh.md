---
id: computing-software.cloud-infrastructure-engineering.kubernetes.w3c-trace-context-propagation-through-ingress-and-mesh
name: w3c-trace-context-propagation-through-ingress-and-mesh
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, trace-context-propagation, w3c-traceparent, opentelemetry, tracing, ingress, service-mesh, b3]
level: advanced
status: docs-checked
description: "Keep one trace across ingress, mesh sidecars and services: W3C traceparent format, aligning propagators, enabling ingress/gateway tracing, and finding where traces break."
sources: ["https://www.w3.org/TR/trace-context/", "https://opentelemetry.io/docs/languages/sdk-configuration/general/", "https://istio.io/latest/docs/tasks/observability/distributed-tracing/overview/", "https://kubernetes.github.io/ingress-nginx/user-guide/third-party-addons/opentelemetry/", "https://github.com/kubernetes/ingress-nginx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# W3C trace context propagation

## The header
```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
             ver  trace-id (32 hex)               parent span (16)  flags (01 = sampled)
tracestate:  vendor=value,...      (optional vendor data)
baggage:     key=value,...         (OTel baggage, separate spec)
```
Every hop must read the incoming header, create a child span, and send a new `traceparent`
with the same trace-id downstream.

## Where traces break, and fixes
1. **Ingress/gateway not participating**: enable tracing so it continues (or starts) the
   trace. Each gateway and mesh implementation has its own tracing config (Istio uses its
   Telemetry API); ingress-nginx offered `enable-opentelemetry: "true"` and `otlp-collector-host` in
   its ConfigMap, but the ingress-nginx project has announced its retirement (best-effort
   maintenance only until March 2026), so plan the replacement controller's tracing settings.
2. **Propagator mismatch**: Zipkin/older Envoy setups use B3 (`x-b3-traceid`), apps use W3C.
   Configure every SDK the same way:
```yaml
env:
- {name: OTEL_PROPAGATORS, value: "tracecontext,baggage"}   # add b3multi during migrations
```
3. **Mesh sidecars cannot propagate for you**: Istio proxies send spans, but the application must
   copy the incoming trace headers to its outgoing requests; Istio lists `x-request-id`,
   `traceparent` and `tracestate` (plus the B3 headers for Zipkin) as the headers to forward (OTel
   auto-instrumentation does this).
4. **Async hops** (Kafka, SQS, job queues): inject the context into message headers on
   produce and extract on consume; otherwise each consumer starts a new trace.
5. **Edge stripping**: CDNs/WAFs/LBs that drop unknown headers. Decide policy: trust
   external `traceparent` (useful for partners) or restart traces at the edge (prevents
   clients forcing sampling).
6. **Sampling disagreement**: use `parentbased_traceidratio` so services honour the
   upstream sampled flag; independent random sampling yields fragmentary traces.

## Debug technique
Deploy an echo service and look at what arrives:
```bash
kubectl run echo --image=<http-echo-image-you-trust> --port 8080 && kubectl expose pod echo --port 80 --target-port 8080
curl -s -H 'traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01' https://app.example.com/echo | jq .headers
```
Same trace-id, different parent span = propagating. Missing or new trace-id = that hop broke it.

## Verify
- [ ] One request through ingress -> service A -> service B -> queue -> worker shows as a
  single trace in Tempo/Jaeger with all spans connected.

## Checked

2026-10-27. Release: W3C Trace Context Recommendation, OpenTelemetry docs (main), Istio docs, ingress-nginx docs (accessed October 2026)
- Confirmed the `traceparent` layout (`00-<32 hex trace-id>-<16 hex parent-id>-<flags>`, version 00) in the W3C Trace Context specification.
- Confirmed `OTEL_PROPAGATORS` default `tracecontext,baggage`, accepted values `tracecontext`, `baggage`, `b3multi`, and the `parentbased_traceidratio` sampler in the OpenTelemetry SDK configuration page.
- Confirmed Istio's header-forwarding list and that applications must propagate headers (Istio tracing overview), and ingress-nginx's `enable-opentelemetry` and `otlp-collector-host` settings (ingress-nginx OpenTelemetry page); added the ingress-nginx retirement notice from the project README.
- Removed the pinned echo-image tag and the claim that named gateway implementations each have a tracing config, because neither was confirmed.

Method: documentation only; no commands were run.
