---
id: computing-software.web-development.phoenix.telemetry-periodic
name: telemetry-periodic
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, telemetry, telemetrypoller, execute, custom-events, genserver, last-value, spans]
level: advanced
status: docs-checked
description: "Emit periodic measurements with telemetry_poller and custom start/stop/exception events from your own GenServer, with metrics."
sources:
  - https://hexdocs.pm/phoenix/telemetry.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: measure your own app values on an interval and emit start/stop/exception events from your own code.

## Periodic measurements
In `lib/my_app_web/telemetry.ex`, add entries to `periodic_measurements/0` (polled by `:telemetry_poller`; the generated supervisor uses `period: 10_000`):
```elixir
defp periodic_measurements do
  [
    {MyApp, :measure_users, []},
    {:process_info,
      event: [:my_app, :my_server],
      name: MyApp.MyServer,
      keys: [:message_queue_len, :memory]}
  ]
end
```
The MFA function emits its event by calling `:telemetry.execute/3`; define metrics for the events as shown below:
```elixir
def measure_users do
  :telemetry.execute([:my_app, :users], %{total: MyApp.users_count()}, %{})
end
```
```elixir
last_value("my_app.users.total"),
last_value("my_app.my_server.memory", unit: :byte),
last_value("my_app.my_server.message_queue_len"),
summary("my_app.my_server.call.stop.duration"),
counter("my_app.my_server.call.exception")
```

## Custom events
The guide's `MyApp.MyServer` GenServer (`lib/my_app/my_server.ex`) wraps a function call in a span using the prefix `@prefix [:my_app, :my_server, :call]`:
- `:start`, before the call: measurement `%{system_time: System.system_time()}`, metadata `%{}`
- `:stop`, after success: measurement `%{duration: native_time}`
- `:exception`, on throw or raise: measurement `%{duration: ...}`, metadata `%{kind: kind, reason: reason, stacktrace: stacktrace}`

Each is emitted like `:telemetry.execute(@prefix ++ [:stop], %{duration: duration}, %{})`, where duration is `System.monotonic_time() - start_time` with `start_time` taken before the call. The wrapper uses `try ... catch kind, reason -> ... :erlang.raise(kind, reason, stacktrace) else result -> ...`. Document the events in the function's `@doc`, as the guide does.

Start it in the application supervisor, passing a zero-arity function:
```elixir
children = [
  {MyApp.MyServer, fn -> "Hello, world!" end},
]
```
With the ConsoleReporter enabled, `iex> MyApp.MyServer.call!` prints a `[Telemetry.Metrics.ConsoleReporter] Got new event!` block for `my_app.my_server.call.stop` and returns `"Hello, world!"`.

Related: computing-software.web-development.phoenix.telemetry-metrics

## Checked

2026-11-08. Read the Phoenix Telemetry guide Periodic measurements and Custom Events sections and the supervisor snippet (period: 10_000); the other sections of the page were not read closely and no claim here depends on them. Confirmed periodic_measurements/0, the process_info entry, the metrics, and the span events with their measurements and metadata. Softened a sentence that said the MFA function must emit the event; the guide only shows it doing so.

Method: documentation only; no commands were run.
