---
id: computing-software.software-engineering.elixir.telemetry-execute-attach
name: telemetry-execute-attach
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, telemetry, telemetry-execute, telemetry-attach, telemetry-span, event-name, measurements, metadata, telemetry-events, elixir-telemetry]
level: advanced
status: draft
description: "Emit events with :telemetry.execute/span and attach handlers using module functions (not anonymous ones) with the event name list."
sources: ["https://hexdocs.pm/telemetry"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Emitting and handling Telemetry events

**Goal:** expose instrumentation points that tools can consume.

```elixir
:telemetry.execute([:my_app, :checkout, :stop], %{duration: dur}, %{user_id: id, status: :ok})
:telemetry.span([:my_app, :job], %{job: name}, fn ->
  result = run()
  {result, %{job: name}}                            # emits :start, :stop (or :exception) with duration
end)

defmodule MyApp.Telemetry do
  def attach do
    :telemetry.attach_many("my-handler", [[:my_app, :checkout, :stop]], &__MODULE__.handle_event/4, nil)
  end
  def handle_event(event, measurements, metadata, _config), do: Logger.info("#{inspect(event)} #{inspect(measurements)}")
end
```

## Rules
- Event names are lists of atoms: `[:app, :thing, :start | :stop | :exception]`; measurements are numbers, metadata is context.
- Attach with a `&Module.fun/4` external capture; local or anonymous functions work but are slower and the library warns.
- A handler that raises is detached automatically; keep handlers cheap and non-blocking.
- Durations from `System.monotonic_time()` are in native units; convert with `System.convert_time_unit/3`.
- Libraries emit events (Phoenix, Ecto, Plug, Finch/Req); you attach to them.

## Self-check
Attach to `[:phoenix, :endpoint, :stop]` and log the request duration.
