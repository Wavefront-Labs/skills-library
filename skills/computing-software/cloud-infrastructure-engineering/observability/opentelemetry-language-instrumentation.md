---
id: computing-software.cloud-infrastructure-engineering.observability.opentelemetry-language-instrumentation
name: opentelemetry-language-instrumentation
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [observability, opentelemetry, otel, otel-sdk, zero-code-instrumentation, auto-instrumentation, code-based-instrumentation, manual-instrumentation, java-agent, opentelemetry-javaagent, opentelemetry-instrument, python-auto-instrumentation, node-auto-instrumentations, dotnet-auto-instrumentation, go-instrumentation-libraries, otel-go, tracer, span, custom-spans, span-attributes, span-events, span-status, context-propagation, otel-env-vars, otel-sdk-configuration, declarative-configuration, instrumentation-libraries]
level: advanced
status: gated
description: "Instrument a service with OpenTelemetry: zero-code agents per language (Java agent, opentelemetry-instrument, Node auto-instrumentations, .NET), the env vars that configure them."
sources: ["https://opentelemetry.io/docs/concepts/instrumentation/", "https://opentelemetry.io/docs/zero-code/", "https://opentelemetry.io/docs/zero-code/js/", "https://opentelemetry.io/docs/zero-code/dotnet/", "https://opentelemetry.io/docs/languages/", "https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/", "https://opentelemetry.io/docs/specs/otel/protocol/exporter/", "https://opentelemetry.io/docs/languages/go/instrumentation/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OpenTelemetry language instrumentation (zero-code and code-based)

**Goal:** every service emits traces (and metrics/logs) in OTel format with the minimum
code change, then adds the handful of custom spans and attributes that make traces useful
for *your* domain.

## 1. Strategy
1. **Zero-code first**: agents hook popular frameworks (HTTP servers/clients, DB drivers,
   messaging, gRPC) and set up the SDK from env vars.
2. **Code-based on top**: use the API (`GetTracer`) to add spans around business steps,
   attributes (`order.id`, `tenant`), events, and to propagate context across custom
   thread pools/queues the agent cannot see.
3. Libraries you own should instrument with the **API only** (no SDK dependency); the
   application configures the SDK.

## 2. Zero-code per language
| Language | How | Notes |
|---|---|---|
| **Java** | `java -javaagent:opentelemetry-javaagent.jar -jar app.jar` | per-library switches to trim noise; Spring Boot alt: the OpenTelemetry Spring Boot starter (no agent); Quarkus has its own extension |
| **Python** | `pip install opentelemetry-distro opentelemetry-exporter-otlp && opentelemetry-bootstrap -a install` then `opentelemetry-instrument python app.py` | see the Python zero-code page for server-specific notes |
| **Node** | `node --require @opentelemetry/auto-instrumentations-node/register app.js` (`npm i @opentelemetry/auto-instrumentations-node @opentelemetry/sdk-node`) | `NODE_OPTIONS="--require @opentelemetry/auto-instrumentations-node/register"` works too; must load before frameworks |
| **.NET** | `otel-dotnet-auto-install.sh` then source `instrument.sh`, or in-code `AddOpenTelemetry()` with instrumentation packages | |
| **Go** | no agent (compiled); use instrumentation libraries: `otelhttp.NewHandler`, `otelgrpc`, `otelsql`, `otelgin`… ; eBPF `opentelemetry-go-instrumentation`/Beyla for true zero-code | |
| **Ruby/PHP** | see the language pages; PHP offers Composer + PECL auto-instrumentation or an OS-package distro (Linux only) | |
| **Kubernetes** | OTel Operator `Instrumentation` CR + pod annotation `instrumentation.opentelemetry.io/inject-java: "true"` injects agents via init container | see `...observability.opentelemetry-operator-and-kubernetes-telemetry` |

Core env vars (all SDKs):
```bash
OTEL_SERVICE_NAME=checkout
OTEL_RESOURCE_ATTRIBUTES=service.version=1.4.0,deployment.environment=prod,service.namespace=shop
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317     # grpc; http/protobuf uses :4318 (+ /v1/traces path auto-appended)
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_TRACES_EXPORTER=otlp OTEL_METRICS_EXPORTER=otlp OTEL_LOGS_EXPORTER=otlp   # none to disable
OTEL_TRACES_SAMPLER=parentbased_traceidratio OTEL_TRACES_SAMPLER_ARG=0.1
OTEL_PROPAGATORS=tracecontext,baggage                         # add b3multi for Zipkin-era services
OTEL_BSP_SCHEDULE_DELAY=5000 OTEL_BSP_MAX_QUEUE_SIZE=2048 OTEL_BSP_MAX_EXPORT_BATCH_SIZE=512
OTEL_SPAN_ATTRIBUTE_VALUE_LENGTH_LIMIT=1024 OTEL_SPAN_ATTRIBUTE_COUNT_LIMIT=128
OTEL_CONFIG_FILE=/etc/otel/sdk.yaml                           # declarative config file; overrides other SDK env vars (OTEL_EXPERIMENTAL_CONFIG_FILE is deprecated)
```

## 3. Code-based additions (the 20% that matters)
```java
Tracer tracer = GlobalOpenTelemetry.getTracer("checkout");          // or inject OpenTelemetry
Span span = tracer.spanBuilder("checkout.reserve_stock").setSpanKind(SpanKind.INTERNAL)
    .setAttribute("order.id", orderId).setAttribute("order.items", items.size()).startSpan();
try (Scope s = span.makeCurrent()) {
    reserve(items);                                                  // child spans from auto-instrumented DB calls attach here
    span.addEvent("stock.reserved", Attributes.of(AttributeKey.longKey("warehouse.id"), wh));
} catch (Exception e) {
    span.recordException(e); span.setStatus(StatusCode.ERROR, e.getMessage()); throw e;
} finally { span.end(); }
```
```python
from opentelemetry import trace
tracer = trace.get_tracer("checkout")
with tracer.start_as_current_span("checkout.reserve_stock", attributes={"order.id": order_id}) as span:
    ...
    span.set_attribute("order.items", len(items))
```
```go
ctx, span := otel.Tracer("checkout").Start(ctx, "checkout.reserve_stock", trace.WithAttributes(attribute.String("order.id", id)))
defer span.End()
// pass ctx down: every otel* library call with ctx becomes a child
if err != nil { span.RecordError(err); span.SetStatus(codes.Error, err.Error()) }
```
Guidelines: span names are low-cardinality verbs (`checkout.reserve_stock`, `HTTP GET /orders/{id}`),
ids go in attributes; `SpanKind` `SERVER/CLIENT/PRODUCER/CONSUMER` only at boundaries,
`INTERNAL` otherwise; set `ERROR` status only for real failures (a 404 is not an error
for a server span); use semconv attribute names where they exist (`db.system`, `messaging.destination.name`,
`enduser.id` carefully). Metrics: see `...observability.opentelemetry-metrics-sdk`.

## 4. Context across gaps the agent cannot see
- Thread pools/executors: Java agent wraps common executors; for custom ones use
  `Context.current().wrap(runnable)`. Python asyncio tasks inherit context; thread pools need
  `contextvars.copy_context()`. Go: always pass `ctx`.
- Message queues: inject with `propagator.inject(context, carrier)` into headers on produce,
  `extract` on consume, start a `CONSUMER` span with a **link** (not parent) for batch consumers.
- Background jobs: start a new root span with a link to the triggering trace id.
- HTTP frameworks not covered: use `otelhttp`-style middleware or the agent's `@WithSpan` annotation (Java) / `opentelemetry-instrumentation-*` package list.

## 5. Verify instrumentation output
```bash
# 1. console exporter first
OTEL_TRACES_EXPORTER=console opentelemetry-instrument python app.py
# 2. then a local collector with the debug exporter
docker run -p 4317:4317 -p 4318:4318 -v $PWD/otel.yaml:/etc/otelcol/config.yaml otel/opentelemetry-collector-contrib:latest
# otel.yaml: receivers otlp → exporters debug (verbosity: detailed)
# 3. generate test spans
telemetrygen traces --otlp-endpoint localhost:4317 --otlp-insecure --traces 5
```
Check: `service.name` is set (not `unknown_service`), spans nest (HTTP server → DB client),
`traceparent` leaves on outbound calls (`curl -v` the downstream to see the header), span
count per request is sane, attribute sizes bounded.

## Gotchas
- Agent loaded after the framework (Node `require` order, Python imports before `opentelemetry-instrument`) ⇒ no spans and no error.
- `unknown_service:java` means `OTEL_SERVICE_NAME` not reaching the JVM (Kubernetes env on the wrong container, Dockerfile `ENV` vs `ARG`).
- Java agent + Spring Boot starter together double-instrument; pick one.
- `OTEL_EXPORTER_OTLP_ENDPOINT` with `http/protobuf` must not include `/v1/traces` (signal paths are appended), but `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` must.
- Sampling at 10% plus an un-sampled parent ⇒ children not recorded; use `parentbased_*` samplers and tail sampling in the Collector for "keep all errors".
- Agent versions pin semconv versions; mixing old (`http.status_code`) and new (`http.response.status_code`) across services breaks dashboards; set `OTEL_SEMCONV_STABILITY_OPT_IN=http` fleet-wide during migration.

## Verify
- [ ] A request through two services yields one trace with SERVER→CLIENT→SERVER spans and shared `trace_id`; `service.name` correct on both.
- [ ] Custom span `checkout.reserve_stock` appears as a child with `order.id` and an `ERROR` status on a forced failure with `exception.stacktrace`.
- [ ] Removing the agent flag produces zero telemetry and no application change otherwise (proves it is truly zero-code).

## Checked

- Date: 2026-11-02.
- Confirmed against: OTEL_SERVICE_NAME, OTEL_RESOURCE_ATTRIBUTES, OTEL_EXPORTER_OTLP_ENDPOINT and _PROTOCOL, OTEL_TRACES_EXPORTER and OTEL_METRICS_EXPORTER (SDK environment variables and exporter spec pages).
- Not confirmed: per-language API call names in the Java, Python and Go examples (the fetched overview pages do not list them) (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
