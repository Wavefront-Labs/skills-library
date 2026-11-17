---
id: computing-software.web-development.phoenix.telemetry-overview
name: telemetry-overview
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, telemetry, metrics, supervisor, telemetry-poller, events, observability]
level: practitioner
status: docs-checked
description: "Understand Phoenix Telemetry: the generated supervisor, event name/measurements/metadata, and the Phoenix and Ecto events to attach metrics to."
sources:
  - https://hexdocs.pm/phoenix/telemetry.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: know how `:telemetry` events, the Telemetry supervisor and metrics fit together in a Phoenix app.

## Concepts
`:telemetry` stores handlers by event name in an ETS table and invokes them when the event executes. An event has a `name` (string or list of atoms), `measurements` (map of atom keys to numbers, e.g. `:duration`) and `metadata` (map used for tagging metrics). Phoenix's tooling is a supervisor that lists `Telemetry.Metrics` definitions and works with reporters, which aggregate them and send them to a destination.

## The supervisor
New apps since v1.5 get `lib/my_app_web/telemetry.ex`: a `Supervisor` that starts `{:telemetry_poller, measurements: periodic_measurements(), period: 10_000}`, can hold reporters as children, and defines `metrics/0`. For older apps, add the deps and create the module:

```elixir
{:telemetry_metrics, "~> 1.0"},
{:telemetry_poller, "~> 1.0"}
```

Then list `MyAppWeb.Telemetry` in the application's children (in `lib/my_app/application.ex`, ahead of `MyApp.Repo` and `MyAppWeb.Endpoint` in the guide's example). Replace `MyApp` with your real app name.

The generated `metrics/0` includes `summary("phoenix.endpoint.stop.duration", unit: {:native, :millisecond})`, `summary("phoenix.router_dispatch.stop.duration", tags: [:route], unit: {:native, :millisecond})`, and VM metrics such as `summary("vm.memory.total", unit: {:byte, :kilobyte})` and `vm.total_run_queue_lengths.total/cpu/io`.

## Example events
- `[:phoenix, :endpoint, :stop]`, sent by `Plug.Telemetry` when the response is sent: measurement `%{duration: native_time}`, metadata `%{conn: Plug.Conn.t}`, emitted as `:telemetry.execute([:phoenix, :endpoint, :stop], %{duration: duration}, %{conn: conn})`.
- `[:ecto, :repo, :init]` from `Ecto.Repo`: measurement `%{system_time: native_time}`, metadata `%{repo: ..., opts: ...}`.
- Adapter events such as `[:my_app, :repo, :query]` and `[:my_app, :repo, :query, :queue_time]`, e.g. `summary("my_app.repo.query.query_time", unit: {:native, :millisecond})` or `distribution("my_app.repo.query.queue_time", unit: {:native, :millisecond})`.

The full Phoenix event list is in the "Instrumentation" section of `Phoenix.Logger`; Ecto's is under "Telemetry Events" in `Ecto.Repo`. Other libraries (Absinthe, Ash, Broadway, Oban, Plug, Tesla) also emit events.

Related: computing-software.web-development.phoenix.telemetry-metrics, computing-software.web-development.phoenix.telemetry-periodic

## Checked

2026-11-08. Confirmed against the Phoenix guide source (phoenixframework/phoenix, guides/telemetry.md, main branch, read in full), the published form of the cited hexdocs page: the generated supervisor, event structure, Phoenix and Ecto event examples and the dependency versions. Removed: nothing.

Method: documentation only; no commands were run.
