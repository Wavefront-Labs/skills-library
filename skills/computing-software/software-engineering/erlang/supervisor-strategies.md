---
id: computing-software.software-engineering.erlang.supervisor-strategies
name: supervisor-strategies
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-supervisor, supervisor-strategies]
level: practitioner
status: docs-checked
description: "OTP supervisor flags: one_for_one, one_for_all, rest_for_one, intensity and period, auto_shutdown."
sources:
  - https://www.erlang.org/doc/system/design_principles.html
  - https://www.erlang.org/doc/apps/stdlib/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restart strategies and intensity
**Goal:** choose a restart strategy that matches dependencies.

```erlang
init([]) ->
    SupFlags = #{strategy => rest_for_one, intensity => 5, period => 10},
    {ok, {SupFlags, ChildSpecs}}.
```
- `one_for_one` (default): only the failed child restarts. `one_for_all`: all other children are terminated and then all are restarted. `rest_for_one`: the children after the failed one in start order are terminated, then the failed child and those after it restart. `simple_one_for_one` is for dynamically added instances of one child type.
- `intensity` defaults to 1 and `period` to 5 (seconds). If more than `intensity` restarts occur within `period` seconds, the supervisor terminates all its children and then itself with reason `shutdown`.
- Children start in the order of the child list and are terminated in reverse start order.
- `auto_shutdown` (since OTP 24) is `never` (default), `any_significant` or `all_significant`, used with `significant => true` on children (not allowed for `permanent` children).

## Gotchas
- The default of 1 restart in 5 seconds is easy to exceed; set intensity and period deliberately.

## Self-check
Kill children in sequence and confirm the restart set matches the strategy.

## Checked
2026-11-02. STDLIB `supervisor` docs (strategies, intensity/period defaults and shutdown behaviour, auto_shutdown OTP 24 and significant rules), OTP Design Principles "Supervisor Behaviour" (start and reverse termination order). Removed: the rest_for_one ordering advice about failure-prone children (not in the docs).
Method: documentation only; no commands were run.
