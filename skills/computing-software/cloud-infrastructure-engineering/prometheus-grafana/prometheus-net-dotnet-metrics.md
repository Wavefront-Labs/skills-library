---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-net-dotnet-metrics
name: prometheus-net-dotnet-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, prometheus-net, dotnet-metrics, aspnetcore, system-diagnostics-metrics, opentelemetry-dotnet, csharp]
level: practitioner
status: docs-checked
description: "Expose .NET metrics to Prometheus with prometheus-net (MapMetrics, UseHttpMetrics, labels, timers) or OpenTelemetry's Prometheus exporter over System.Diagnostics.Metrics."
sources:
  - https://github.com/prometheus-net/prometheus-net
  - https://learn.microsoft.com/en-us/dotnet/core/diagnostics/metrics-collection
  - https://github.com/open-telemetry/opentelemetry-dotnet/tree/main/src/OpenTelemetry.Exporter.Prometheus.AspNetCore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# .NET metrics for Prometheus

## Option A: prometheus-net
Targets .NET Framework 4.6.2 and .NET 6.0 and newer. Packages: `prometheus-net` (core, HttpListener, Pushgateway), `prometheus-net.AspNetCore` (middleware and Kestrel server), `prometheus-net.AspNetCore.HealthChecks`, `prometheus-net.AspNetCore.Grpc`, `prometheus-net.NetFramework.AspNet`.

```csharp
private static readonly Counter ProcessedJobCount = Metrics
    .CreateCounter("myapp_jobs_processed_total", "Number of processed jobs.");
ProcessedJobCount.Inc();

private static readonly Counter RequestCountByMethod = Metrics
    .CreateCounter("myapp_requests_total", "Requests by HTTP method.", labelNames: new[] { "method" });
RequestCountByMethod.WithLabels("GET").Inc();

using (LoginDuration.NewTimer()) { /* Histogram LoginDuration; times the block in seconds */ }
```
- Metric types: Counter, Gauge, Summary, Histogram. The usual pattern is a static readonly field per metric. The library is thread-safe.
- Timers (`NewTimer()`) report seconds to a Summary, Histogram, Gauge or Counter; `Gauge.TrackInProgress()` and `Counter.CountExceptions(...)` are built in.
- Summaries report only sum and count unless you configure quantile objectives.
- A metric without labels is published immediately; one with labels is published when label values are first supplied. `SuppressInitialValue`, `Publish()` and `Unpublish()` control this.
- Delete with `.Dispose()` or `.RemoveLabelled()`, or use `Metrics.WithManagedLifetime(expiresAfter: ...)` for automatic expiry of high-cardinality label sets.
- Keep label cardinality low: HTTP method is a good label, URL is not.

### ASP.NET Core
```csharp
app.UseRouting();
app.UseHttpMetrics(options => options.ReduceStatusCodeCardinality());   // 200, 201 -> 2xx
app.UseEndpoints(endpoints => endpoints.MapMetrics());                  // /metrics by default
```
- `UseHttpMetrics()` goes after `UseRouting()`; it exposes requests in progress, total requests and request duration. It captures `action`, `controller` and `endpoint` route parameters by default (and `page` for Razor Pages); add more with `AddRouteParameter(...)` or `AddCustomLabel(...)`.
- Exception-handler middleware that changes status codes must be registered after `UseHttpMetrics()` so the right code is reported.
- Other integrations: `UseGrpcMetrics()`, `services.UseHttpClientMetrics()` for IHttpClientFactory clients, and `.ForwardToPrometheus()` on health checks (publishes `aspnetcore_healthcheck_status`).
- Protect the endpoint with `MapMetrics().RequireAuthorization("ReadMetrics")` or serve metrics from a separate `KestrelMetricServer(port: ...)` behind firewall rules.
- .NET Meters (`System.Diagnostics.Metrics`), EventCounters and DiagnosticSource are bridged: by default all Meters API data and the well-known EventCounters are published. Configure with `Metrics.ConfigureMeterAdapter()` / `ConfigureEventCounterAdapter()`; turn defaults off with `Metrics.SuppressDefaultMetrics()` before registering your own metrics. Output of these two integrations changed significantly between prometheus-net 6.0 and 7.0.
- Exemplars (trace_id and span_id from `Activity.Current`) appear only when scraped in OpenMetrics format; exemplar storage may need enabling on the Prometheus server.

## Option B: OpenTelemetry .NET
```csharp
builder.Services.AddOpenTelemetry()
  .WithMetrics(m => m.AddMeter("HatCo.HatStore").AddPrometheusExporter());
app.MapPrometheusScrapingEndpoint();      // default path /metrics
```
- `AddMeter(name)` transmits all metrics from a `System.Diagnostics.Metrics.Meter` (the name is case-sensitive); build the Meter with `new Meter("name", "version")`.
- The ASP.NET Core exporter package is `OpenTelemetry.Exporter.Prometheus.AspNetCore` (installed with `--prerelease`). Its README says it is still under development, depends on an experimental Prometheus/OpenMetrics compatibility specification and can have breaking changes before stable release; it recommends `OpenTelemetry.Exporter.OpenTelemetryProtocol` for production.
- `ScrapeResponseCacheDurationMilliseconds` defaults to 300 (scrapes inside that window get the same cached response); set 0 to disable. `ScrapeEndpointPath` defaults to `/metrics`, and a `target_info` metric is produced by default (`TargetInfoEnabled`). Older Generic Host apps use `UseOpenTelemetryPrometheusScrapingEndpoint()`.
- For a console app the Microsoft tutorial uses `OpenTelemetry.Exporter.Prometheus.HttpListener` with `AddPrometheusHttpListener(options => options.Port = 9184)`.
- `dotnet-counters monitor -n <app> <MeterName>` shows live Meter values without any exporter, for checking that instrumentation works.

## Choosing
Both read `System.Diagnostics.Metrics`. The prometheus-net README includes its own SDK comparison benchmarks against the OpenTelemetry SDK (a vendor claim: prometheus-net does less CPU work per existing time series, OpenTelemetry allocates less for new series).

## Verify
- [ ] `/metrics` returns your metrics and the default runtime or Meter metrics.
- [ ] Request metrics carry `action`, `controller` or `endpoint` labels, not raw URLs.

## Checked
Checked 2026-11-08 against the prometheus-net README, the Microsoft metrics-collection tutorial and the OpenTelemetry Prometheus ASP.NET Core exporter README. Removed because the pages do not state them: `UseMetricServer(port:)`, the "since v8" bridging claim, the claim that labels are empty if UseHttpMetrics precedes UseRouting, OTel semantic-convention metric names, `AddRuntimeInstrumentation` and `AddAspNetCoreInstrumentation` usage, and specific runtime metric names for verification.

Method: docs-only read of cited pages, 2026-11-08
