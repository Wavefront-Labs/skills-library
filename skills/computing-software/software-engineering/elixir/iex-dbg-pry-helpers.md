---
id: computing-software.software-engineering.elixir.iex-dbg-pry-helpers
name: iex-dbg-pry-helpers
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, iex, dbg, iex-pry, io-inspect, recompile, h-helper, break, iex-break, iex-debugging, elixir-debugging]
level: practitioner
status: docs-checked
description: "Debug with dbg/2 and IO.inspect labels, IEx.pry, breakpoints, h/1, i/1, recompile/0 and the iex -S mix workflow."
sources: ["https://hexdocs.pm/iex/IEx.html", "https://hexdocs.pm/elixir/Kernel.html#dbg/2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IEx helpers, dbg and IEx.pry

**Goal:** inspect running code quickly.

```elixir
x |> Enum.map(&f/1) |> dbg()                       # prints each pipeline step and value
IO.inspect(value, label: "after parse", limit: :infinity, pretty: true)
require IEx; IEx.pry()                              # needs iex -S mix; `respawn` / `continue`
# in IEx
h Enum.map/2 ; i some_value ; v(-1) ; recompile() ; r MyMod ; b MyMod
break! MyMod.fun/2 ; breaks ; whereami()
IEx.configure(inspect: [limit: 50])
```
```bash
iex -S mix                      # IEx inside the Mix project
```

## Rules
- `dbg/2` works with pipelines and respects `pry` when run in IEx.
- Remove `dbg`/`IO.inspect` before committing.
- `IEx.pry` needs the process to run inside `iex`; in a plain `mix test` use `iex -S mix test --trace`.
- Use `.iex.exs` in the project root for helper imports on startup.

## Self-check
Pipe a three-step pipeline into `dbg()` and read every intermediate value.

## Checked
2026-11-08: confirmed against the IEx page (pry, respawn, break!, breaks, whereami, .iex.exs, IEx.configure, iex -S mix test --trace) and Kernel dbg. Removed: exports/1, the phx.server variant, the dbg version number and the Credo remark.
Method: documentation only; no commands were run.
