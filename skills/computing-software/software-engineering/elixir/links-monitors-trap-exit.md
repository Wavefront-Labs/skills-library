---
id: computing-software.software-engineering.elixir.links-monitors-trap-exit
name: links-monitors-trap-exit
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, link, monitor, trap-exit, exit-signal, down-message, process-flag, links-monitors]
level: advanced
status: docs-checked
description: "Use links for fate sharing, monitors for one-way observation (:DOWN messages) and trap_exit to convert exit signals to messages."
sources: ["https://hexdocs.pm/elixir/Process.html", "https://www.erlang.org/doc/system/ref_man_processes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Links, monitors and trapping exits

**Goal:** react to other processes dying correctly.

```elixir
ref = Process.monitor(pid)
receive do
  {:DOWN, ^ref, :process, ^pid, reason} -> handle(reason)
end
Process.demonitor(ref, [:flush])

Process.flag(:trap_exit, true)
Process.link(pid)
receive do {:EXIT, ^pid, reason} -> reason end     # instead of dying with it
Process.exit(pid, :shutdown)
```

## Rules
- A link is bidirectional: if one process exits abnormally, the other receives an exit signal and dies unless trapping exits. Reason `:normal` does not kill linked processes.
- A monitor delivers `{:DOWN, ref, :process, pid, reason}` when the process exits; monitoring an already dead pid delivers a `:DOWN` message immediately (reason `:noproc`).
- `Process.exit(pid, :kill)` is untrappable. A GenServer that traps exits has `terminate/2` called when its parent sends an exit signal (for example on supervisor shutdown).
- A trapped exit signal becomes an `{:EXIT, from, reason}` message; `Process.exit(pid, :normal)` does not stop another process, but a trapping process receives `{:EXIT, from, :normal}`.

## Self-check
Link to a process that exits with `:boom` and confirm the caller exits too unless it traps exits.

## Checked
2026-11-03: confirmed against the Elixir Process docs (`link/1`, `monitor`, `demonitor/2` `:flush`, `exit/2` with `:normal` and `:kill`, `flag(:trap_exit, ...)`, immediate `:DOWN` with `:noproc`) and GenServer docs (`terminate/2` when trapping exits). Removed: the "exactly one :DOWN" and "supervisors link to children" claims, and the IEx shell-restart expectation.
Method: documentation only; no commands were run.
