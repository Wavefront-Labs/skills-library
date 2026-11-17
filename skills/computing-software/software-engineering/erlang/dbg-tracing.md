---
id: computing-software.software-engineering.erlang.dbg-tracing
name: dbg-tracing
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-debugging, dbg-tracing]
level: sme
status: draft
description: "Erlang dbg tracing: tracer, p, tpl with exception_trace, limits and safe use in production."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# dbg and erlang:trace
**Goal:** trace function calls on a live node safely.

```erlang
dbg:tracer(),
dbg:p(all, c),                                      % trace calls in all processes
dbg:tpl(my_mod, my_fun, x),                         % x: also print return and exceptions
dbg:tpl(my_mod, my_fun, dbg:fun2ms(fun([A, _]) when A > 10 -> return_trace() end)),
dbg:stop().
```
- `dbg:stop()` / `dbg:stop_clear()` must always run afterwards; a forgotten trace on a hot function can swamp the node.
- Narrow the pattern (module, function, arity, argument guards) and the process set before enabling.
- `erlang:trace/3` and `erlang:trace_pattern/3` are the low-level BIFs; prefer a rate-limited tool (recon_trace) on production.
- Large arguments are printed in full and can flood output.

## Gotchas
- Tracing `all` processes and `all` functions can take down a node.

## Self-check
Trace a single function in the shell, call it, then `dbg:stop()`.
