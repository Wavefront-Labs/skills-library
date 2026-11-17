---
id: computing-software.software-engineering.erlang.persistent-term
name: persistent-term
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-ets, persistent-term]
level: advanced
status: docs-checked
description: "Erlang persistent_term for read-mostly global data and counters/atomics for lock-free numeric state, with update cost caveats."
sources:
  - https://www.erlang.org/doc/apps/erts/persistent_term.html
  - https://www.erlang.org/doc/apps/erts/counters.html
  - https://www.erlang.org/doc/apps/erts/atomics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# persistent_term, counters and atomics
**Goal:** use the cheapest primitive for each shared-state pattern.

```erlang
persistent_term:put({myapp, config}, Config),
Config = persistent_term:get({myapp, config}),
persistent_term:get({myapp, missing}, default).
C = counters:new(4, [write_concurrency]),
counters:add(C, 1, 1), counters:get(C, 1).
A = atomics:new(1, [{signed, false}]),
atomics:add_get(A, 1, 1).
```
- `persistent_term:get/1` is constant time, takes no locks and does not copy the term to the heap (unlike ETS). Replacing or erasing a complex term starts a global garbage collection: every process scans its heap, and a process still using the term does a full-sweep GC. Atoms and other one-word terms avoid the global GC, but the key hash table is still copied on every update.
- Avoid updating or deleting several persistent terms at once; each triggers its own global GC. Group values that change together into one term such as a map.
- `counters` are 64-bit signed integer arrays; `write_concurrency` counters trade some read consistency for faster concurrent writes, `atomics` counters give consistent semantics. `atomics` arrays are signed by default (`{signed, false}` makes them unsigned).

## Gotchas
- Do not store a frequently changing value in persistent_term.
- Avoid holding a retrieved persistent term in a process if it may be updated or deleted: that process gets garbage collected and the term copied into it.

## Self-check
Benchmark `persistent_term:get` against `ets:lookup` for the same value.

## Checked

2026-11-03. Confirmed in the `persistent_term`, `counters` and `atomics` pages. Removed: the generic gen_server/ETS alternatives bullet.
Method: documentation only; no commands were run.
