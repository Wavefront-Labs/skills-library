---
id: computing-software.software-engineering.erlang.child-specs
name: child-specs
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-supervisor, child-specs]
level: practitioner
status: docs-checked
description: "OTP supervisor child_spec map: id, start MFA, restart, shutdown, type, modules; permanent, transient, temporary."
sources:
  - https://www.erlang.org/doc/system/design_principles.html
  - https://www.erlang.org/doc/apps/stdlib/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Child specifications
**Goal:** write child specs that shut down cleanly.

```erlang
#{id => worker1,
  start => {worker, start_link, [Arg]},
  restart => permanent,          % permanent | transient | temporary
  shutdown => 5000,              % ms | brutal_kill | infinity
  type => worker,                % worker | supervisor
  modules => [worker]}
```
- `id` and `start` are mandatory. Defaults: `restart => permanent`, `shutdown => 5000` for workers and `infinity` for supervisors, `type => worker`, `significant => false`, `modules => [M]` from the start `{M,F,A}`.
- `permanent` is always restarted; `temporary` never; `transient` only if it terminates abnormally, that is with a reason other than `normal`, `shutdown` or `{shutdown, Term}`.
- The start function must create and link the child and return `{ok, Pid}`, `{ok, Pid, Info}`, `ignore` or `{error, Error}`.
- With an integer `shutdown` the supervisor sends the `shutdown` exit signal and kills the child if it has not exited within that many milliseconds; `brutal_kill` kills it at once.
- For a child that is itself a supervisor the shutdown must be `infinity`.
- `modules` is used by the release handler: `[Module]` for supervisor, gen_server or gen_statem, `dynamic` for gen_event with dynamic handlers.

## Gotchas
- A worker that does not trap exits is terminated at once by the shutdown signal; one that traps exits must exit on `shutdown` or it is killed after the timeout.

## Self-check
Print `supervisor:which_children/1` and `count_children/1` for your tree.

## Checked
2026-11-02. STDLIB `supervisor` docs (child specification keys, defaults, start function return values, restart types, shutdown semantics, modules). Removed: the `child_spec/1` shorthand claim (not in the pages read).
Method: documentation only; no commands were run.
