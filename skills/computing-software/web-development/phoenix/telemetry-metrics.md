---
id: computing-software.web-development.phoenix.telemetry-metrics
name: telemetry-metrics
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, telemetry, metrics, summary, counter, livedashboard, reporters, tag-values]
level: practitioner
status: docs-checked
description: "Define Telemetry.Metrics in Phoenix, attach reporters (ConsoleReporter, LiveDashboard), and group metrics with :tags and :tag_values."
sources:
  - https://hexdocs.pm/phoenix/telemetry.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: turn Telemetry events into metrics and see them through a reporter.

## Metric definitions
`Telemetry.Metrics` exposes five metric type functions; it only describes metrics, a reporter does the aggregation. Examples: `counter("phoenix.endpoint.stop.duration")` (requests completed), `distribution("phoenix.endpoint.stop.duration")` (time buckets), `summary("my_app.repo.query.query_time", unit: {:native, :millisecond})`. Put them in `metrics/0` of `lib/my_app_web/telemetry.ex`.

## Reporters
A reporter attaches to the events behind your metrics and aggregates them.
- Console: add `{Telemetry.Metrics.ConsoleReporter, metrics: metrics()}` to the supervisor's children, restart, and make requests; log lines appear in the terminal.
- `Phoenix.LiveDashboard` acts as a reporter and renders real-time charts.
- Reporters for StatsD, Prometheus and others exist; search "telemetry_metrics" on hex.pm.

## Tags
`:tags` is a list of metadata keys to group by (reporters handle tags differently depending on the service):
```elixir
summary("phoenix.router_dispatch.stop.duration",
  tags: [:route],
  unit: {:native, :millisecond}
)
```
`:tag_values` is a function that reshapes metadata. It runs for every event, so keep it fast. The HTTP method lives inside `conn` in the metadata, so lift it:
```elixir
summary("phoenix.router_dispatch.stop.duration",
  tags: [:method, :route],
  tag_values: &get_and_put_http_method/1,
  unit: {:native, :millisecond}
)

defp get_and_put_http_method(%{conn: %{method: method}} = metadata) do
  Map.put(metadata, :method, method)
end
```
`:tags` and `:tag_values` work on all metric types. The router event `[:phoenix, :router_dispatch, :stop]` has metadata `conn`, `route`, `plug`, `plug_opts`, `path_params` and `pipe_through`.

## Readable labels
For `phoenix.live_view.mount.stop.duration` with `tags: [:view, :connected?]`, LiveDashboard shows the label `"Elixir.Phoenix.LiveDashboard.MetricsLive true"`. Clean it up in `tag_values`:
```elixir
defp live_view_metric_tag_values(metadata) do
  metadata
  |> Map.put(:view, inspect(metadata.socket.view))
  |> Map.put(:connected?, get_connection_status(Phoenix.LiveView.connected?(metadata.socket)))
end

defp get_connection_status(true), do: "Connected"
defp get_connection_status(false), do: "Disconnected"
```
The label then reads `"Phoenix.LiveDashboard.MetricsLive Connected"`.

Related: computing-software.web-development.phoenix.telemetry-overview

## Checked

2026-11-08. Confirmed against the Phoenix guide source (phoenixframework/phoenix, guides/telemetry.md, main branch, read in full), the published form of the cited hexdocs page: metric types, reporters, tags and tag_values, and the LiveView label example. Removed: nothing.

Method: documentation only; no commands were run.
