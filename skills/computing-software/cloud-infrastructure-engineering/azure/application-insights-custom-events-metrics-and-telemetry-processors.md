---
id: computing-software.cloud-infrastructure-engineering.azure.application-insights-custom-events-metrics-and-telemetry-processors
name: application-insights-custom-events-metrics-and-telemetry-processors
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, application-insights, custom-events, custom-metrics, telemetry-processors, opentelemetry]
level: advanced
status: docs-checked
description: "Emit custom events and metrics to Application Insights with OpenTelemetry or the classic SDK, and adjust telemetry with processors."
sources: ["https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-add-modify", "https://learn.microsoft.com/azure/azure-monitor/app/api-custom-events-metrics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Insights custom telemetry and processors

**Goal:** send business events and metrics, and adjust telemetry before it is exported.

## Custom events with OpenTelemetry
Application Insights stores custom events in the `customEvents` table. With the Microsoft OpenTelemetry Distro for .NET, send one through `ILogger` by putting the `microsoft.custom_event.name` attribute in the message template:
```csharp
app.Logger.LogInformation("{microsoft.custom_event.name} {additional_attrs}", "test-event-name", "val1");
```
The distro is enabled with `UseMicrosoftOpenTelemetry(options => options.Exporters = ExportTarget.AzureMonitor)`. The same attribute name routes log records to `customEvents` in Java (agent), Node.js (`logger.emit` attributes) and Python (`extra` argument of logging). It is not possible to send a custom event this way with Java native.

## Custom metrics with OpenTelemetry
Create a `Meter`, create instruments from it (for example `meter.CreateHistogram<long>("FruitSalePrice")`) and record values with attributes. Register the meter by name on the provider, for example `.WithMetrics(metrics => metrics.AddMeter("OTel.AzureMonitor.Demo"))`, or its measurements are not collected. Keep the provider alive for the process lifetime.

## Classic SDK custom metrics
- `TrackMetric()` sends one raw telemetry item per value and passes through the full telemetry initializer and processor pipeline each time; it is no longer the preferred method.
- `GetMetric()` pre-aggregates: it accumulates values from all `Track` calls and sends a summary once a minute, cutting cost and overhead. `GetMetric("name", "dimension").TrackValue(n)` supports a dimension.
- Custom metrics from `TrackMetric()` and `GetMetric()` are not subject to sampling, so alert thresholds stay reliable.
- `GetMetric()` does not support gauge-style last-value tracking or histograms.

## Processors (OpenTelemetry .NET)
A custom activity processor derives from `BaseProcessor<Activity>` and overrides `OnEnd`. Learn's example marks server-side HTTP 4xx responses as successful so they are not counted as failures: when `activity.Kind == ActivityKind.Server` and `http.response.status_code` is 400 to 499, call `activity.SetStatus(ActivityStatusCode.Ok)`; the status-code tag itself is unchanged. Register it with `.WithTracing(tracing => tracing.AddProcessor<Http4xxSuccessProcessor>())`.

## Verify
- [ ] `customEvents | where name == "test-event-name" | take 5` returns rows.
- [ ] A custom metric appears in `customMetrics` or Metrics explorer after the meter is registered.

## Checked
Method: docs-checked 2026-11-09 against opentelemetry-add-modify (downloaded with curl as Learn markdown; the custom events, custom metrics and 4xx processor sections read). The api-custom-events-metrics URL now resolves to the classic API 2.x page, whose GetMetric/TrackMetric section was read. Dropped the old UseAzureMonitor call, the filtering and sampling page, Java processor JSON, custom-dimension limits and parent/child drop advice, which were not confirmed.
