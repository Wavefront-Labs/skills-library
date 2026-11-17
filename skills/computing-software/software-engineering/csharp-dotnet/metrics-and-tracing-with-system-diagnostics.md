---
id: computing-software.software-engineering.csharp-dotnet.metrics-and-tracing-with-system-diagnostics
name: metrics-and-tracing-with-system-diagnostics
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, activitysource, system-diagnostics-metrics, opentelemetry-dotnet, meter, distributed-tracing, dotnet-diagnostics]
level: practitioner
status: docs-checked
description: "Instrument .NET code with System.Diagnostics.Metrics (Meter, Counter, Histogram) and ActivitySource spans, export via OpenTelemetry, and inspect locally with dotnet-counters."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/diagnostics/metrics-instrumentation", "https://learn.microsoft.com/en-us/dotnet/core/diagnostics/distributed-tracing-instrumentation-walkthroughs", "https://opentelemetry.io/docs/languages/dotnet/getting-started/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics and tracing with System.Diagnostics

**Goal:** custom business and performance telemetry using the BCL APIs that
OpenTelemetry, dotnet-counters and APM vendors all consume.

## Metrics
```csharp
public sealed class CheckoutMetrics
{
    private readonly Counter<long> _orders;
    private readonly Histogram<double> _paymentMs;
    public CheckoutMetrics(IMeterFactory factory)
    {
        var meter = factory.Create("Acme.Checkout");             // DI-friendly, testable (.NET 8)
        _orders = meter.CreateCounter<long>("acme.checkout.orders", unit: "{order}");
        _paymentMs = meter.CreateHistogram<double>("acme.checkout.payment.duration", unit: "ms");
    }
    public void OrderPlaced(string channel) => _orders.Add(1, new KeyValuePair<string, object?>("channel", channel));
    public void PaymentTook(double ms, bool ok) => _paymentMs.Record(ms, new("outcome", ok ? "ok" : "failed"));
}
```
Instruments: `Counter` (monotonic), `UpDownCounter` (in-flight), `Histogram` (latency/size),
observable gauges/counters for sampled values (queue length). Keep tag cardinality low - never
user IDs or URLs with IDs as tags.

## Tracing
```csharp
private static readonly ActivitySource Source = new("Acme.Checkout");

public async Task<Receipt> PayAsync(Order o, CancellationToken ct)
{
    using var activity = Source.StartActivity("checkout.pay");     // null when nobody listens: cheap
    activity?.SetTag("order.id", o.Id);
    try { return await _gateway.ChargeAsync(o, ct); }
    catch (Exception ex)
    {
        activity?.SetStatus(ActivityStatusCode.Error, ex.Message);
        throw;
    }
}
```
`Activity` is .NET's span.

## Export
Use the OpenTelemetry .NET SDK, or any other consumer of these APIs, to export the data (see the OpenTelemetry .NET documentation).



## Verify
- [ ] Custom meters/sources registered with the telemetry SDK and visible in the backend.
- [ ] Metric tags reviewed for bounded cardinality.

## Checked

- Date: 2026-10-28
- Confirmed on Microsoft Learn (metrics instrumentation, distributed tracing instrumentation): Meter, IMeterFactory (.NET 8), instruments, ActivitySource and Activity.
- Removed: OpenTelemetry builder code and environment variable (page not readable), dotnet-counters and Aspire dashboard commands, MetricCollector/ActivityListener testing notes, AddException, automatic propagation remark.
Method: documentation only; no commands were run.
