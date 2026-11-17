---
id: computing-software.software-engineering.elixir.observer-recon-tracing-dbg
name: observer-recon-tracing-dbg
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, observer, recon, tracing, erlang-dbg, sys-get-state, process-info, remote-shell, runtime-tools, observer-tracing]
level: advanced
status: draft
description: "Inspect a live node with :observer / observer_cli, :sys.get_state, :recon and Erlang tracing, with attention to production safety."
sources: ["https://www.erlang.org/doc/apps/runtime_tools/", "https://hexdocs.pm/recon", "https://hexdocs.pm/observer_cli"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Observer, recon and tracing

**Goal:** diagnose a running system without restarting it.

```elixir
:observer.start()                       # GUI (needs wx); remote nodes: connect first, then Nodes menu
:sys.get_state(pid) ; :sys.trace(pid, true) ; :sys.get_status(pid)
Process.info(pid, [:message_queue_len, :memory, :current_stacktrace])
:erlang.memory() ; :erlang.system_info(:process_count)
:recon.proc_count(:memory, 10) ; :recon.proc_count(:message_queue_len, 10)
:recon_trace.calls({MyMod, :fun, :_}, 10)         # limit the number of trace messages!
:erlang.garbage_collect(pid)
```

## Rules
- Add `:runtime_tools` to extra_applications/release applications so tools are available in production.
- Tracing can overload a production node; always cap trace output (recon_trace takes a count) and prefer targeted match specs.
- `:sys.get_state/1` works on OTP-compliant processes (GenServer etc.) and blocks while the process is busy.
- Common finds: huge mailboxes (a slow consumer), memory in binaries, ETS growth, runaway process counts.

## Self-check
List the top 5 processes by message queue length on a dev node with load.
