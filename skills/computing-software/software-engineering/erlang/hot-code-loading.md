---
id: computing-software.software-engineering.erlang.hot-code-loading
name: hot-code-loading
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-code, hot-code-loading]
level: sme
status: draft
description: "Erlang code replacement: current and old code, code:purge, soft_purge, fully qualified calls and process impact."
sources:
  - https://www.erlang.org/doc/apps/kernel/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reloading modules at runtime
**Goal:** reload a module without a restart and know what breaks.

```erlang
c(mymod).                          % compile and load
code:load_file(mymod).             % load a new beam
code:soft_purge(mymod),            % remove old code only if no process uses it
code:purge(mymod).                 % kills processes still running old code
```
- At most two versions per module: current and old. Loading a third purges the old one and kills processes still running it.
- A process switches to new code at its next fully qualified call (`?MODULE:loop(State)`), not at local calls `loop(State)`.
- Funs created from old code keep running old code until dropped.
- `sys:suspend/1`, `sys:change_code/4`, `sys:resume/1` apply `code_change/3` to behaviour processes.
```erlang
loop(S) -> receive upgrade -> ?MODULE:loop(S); X -> loop(handle(X, S)) end.
```

## Gotchas
- State shape changes need explicit conversion; test with real state.

## Self-check
Reload a module that a running process loops through and verify the new behaviour.
