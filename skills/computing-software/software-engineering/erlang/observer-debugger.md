---
id: computing-software.software-engineering.erlang.observer-debugger
name: observer-debugger
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-debugging, observer-debugger]
level: practitioner
status: draft
description: "Erlang observer GUI over a hidden node, interactive debugger with interpreted modules, and etop."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# observer, debugger and etop
**Goal:** inspect nodes graphically and step through code.

- `observer:start()` needs the `wx` application; for a remote production node, start a local hidden node and connect: `erl -name dbg@host -hidden -setcookie <cookie>` then `observer:start()` and choose Nodes, Connect.
- `etop` and `observer_cli` (third-party) work in a terminal without wx; prefer them on servers.
- Debugger: `debugger:start()`, interpret a module with `int:i(Mod)`, set breakpoints in the GUI. It requires the module compiled with `debug_info` and slows execution.
- The break-point style debugger is for development; use tracing in production.
- Remote shell without a GUI: `erl -remsh app@host -name x@host -setcookie <cookie>` or `bin/myapp remote_console`.

## Gotchas
- Connecting observer exposes full node control; do it over a trusted network only.

## Self-check
Start observer on a local node and open the Processes tab.
