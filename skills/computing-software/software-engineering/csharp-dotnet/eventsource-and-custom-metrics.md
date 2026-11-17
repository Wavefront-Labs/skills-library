---
id: computing-software.software-engineering.csharp-dotnet.eventsource-and-custom-metrics
name: eventsource-and-custom-metrics
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-diagnostics, eventsource, system-diagnostics-metrics, meter, eventpipe, activitysource]
level: advanced
status: draft
description: "Emit diagnostics from .NET code: EventSource for EventPipe/ETW tracing, System.Diagnostics.Metrics Meter instruments, ActivitySource spans, and collecting them with dotnet-counters and trace."
sources: ["https://learn.microsoft.com/en-us/dotnet/core/diagnostics/eventsource", "https://learn.microsoft.com/en-us/dotnet/core/diagnostics/metrics-instrumentation", "https://learn.microsoft.com/en-us/dotnet/core/diagnostics/distributed-tracing-instrumentation-walkthroughs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EventSource, Meter and ActivitySource

## Prefer Meter and ActivitySource (.NET 6+/8)
```csharp
static readonly Meter M = new("Acme.Orders", "1.0");
static readonly Counter<long> Placed = M.CreateCounter<long>("orders.placed", "{order}");
static readonly Histogram<double> Latency = M.CreateHistogram<double>("orders.latency", "ms");
Placed.Add(1, new KeyValuePair<string, object?>("channel", "web"));         // low-cardinality tags only
M.CreateObservableGauge("orders.queue", () => queue.Count);                // sampled callback

static readonly ActivitySource Src = new("Acme.Orders");
using var a = Src.StartActivity("PlaceOrder", ActivityKind.Internal);       // null when nobody listens: zero cost
a?.SetTag("order.id", id);
```
In DI apps use `IMeterFactory` (.NET 8) for testable meters. Export through OpenTelemetry (`AddMeter("Acme.Orders")`, `AddSource("Acme.Orders")`). Local view: `dotnet-counters monitor --counters Acme.Orders -p <pid>`; Prometheus via dotnet-monitor/OTel.

## EventSource (low-level, high-volume tracing)
```csharp
[EventSource(Name = "Acme-Orders")]
public sealed class OrdersEvents : EventSource
{
    public static readonly OrdersEvents Log = new();
    [Event(1, Level = EventLevel.Informational)] public void OrderPlaced(int id) { if (IsEnabled()) WriteEvent(1, id); }
    [NonEvent] public void Placed(Order o) { if (IsEnabled()) OrderPlaced(o.Id); }        // keep expensive formatting out of event methods
}
```
Collect: `dotnet-trace collect -p <pid> --providers Acme-Orders:0xFFFFFFFF:5`. Rules: unique sequential event ids matching `WriteEvent`'s first arg, simple primitive/string args, guard with `IsEnabled()`, singleton instance, names stable (they are an external contract). Use `EventCounter`/`PollingCounter` only for legacy; `Meter` supersedes.

## Gotchas
- High-cardinality tags (user ids, URLs) explode time series cost.
- Mismatched event id vs `WriteEvent` id silently logs nothing (check `EventSource` self-diagnostics `EventSourceException` in debug).
- Activities need a listener (OTel) to be created.
- Do not log PII or secrets in tags/events.

## Verify
`dotnet-counters monitor` shows the instrument updating; a `.nettrace` opened in PerfView/VS lists the custom events; unit test uses `MeterListener` to assert counter increments.
