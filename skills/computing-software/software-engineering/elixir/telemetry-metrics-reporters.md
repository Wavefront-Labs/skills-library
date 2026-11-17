---
id: computing-software.software-engineering.elixir.telemetry-metrics-reporters
name: telemetry-metrics-reporters
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, telemetry-metrics, telemetry-poller, prometheus, peep, live-dashboard, summary, counter, last-value]
level: advanced
status: draft
description: "Define Telemetry.Metrics (counter, sum, last_value, summary, distribution), feed a reporter such as LiveDashboard or a Prometheus exporter and add VM measurements via tel"
sources: ["https://hexdocs.pm/telemetry_metrics", "https://hexdocs.pm/telemetry_poller"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Telemetry.Metrics and reporters

**Goal:** turn events into metrics a monitoring system can scrape.

```elixir
import Telemetry.Metrics
def metrics do
  [
    summary("phoenix.endpoint.stop.duration", unit: {:native, :millisecond}),
    counter("my_app.checkout.stop.count", tags: [:status]),
    distribution("my_app.repo.query.total_time", unit: {:native, :millisecond}, reporter_options: [buckets: [5, 25, 100, 500]]),
    last_value("vm.memory.total", unit: {:byte, :kilobyte})
  ]
end
# Supervisor: {:telemetry_poller, measurements: [], period: 10_000, name: :poller}
# Dev dashboard: live_dashboard "/dashboard", metrics: MyAppWeb.Telemetry
```

## Rules
- Metric names map to event name + measurement: `phoenix.endpoint.stop.duration` is event `[:phoenix, :endpoint, :stop]`, measurement `:duration`.
- Tags must be low-cardinality (never user ids or full paths) or the time-series database will explode.
- The reporter is a separate library (Prometheus exporters such as `peep` or `telemetry_metrics_prometheus_core`, StatsD, OpenTelemetry); `Telemetry.Metrics` only defines.
- Phoenix generators create `MyAppWeb.Telemetry` with sensible defaults.

## Self-check
Open `/dashboard` in dev and watch a request metric change.
