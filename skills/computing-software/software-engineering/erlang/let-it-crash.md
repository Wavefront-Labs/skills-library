---
id: computing-software.software-engineering.erlang.let-it-crash
name: let-it-crash
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-errors, let-it-crash]
level: advanced
status: draft
description: "Erlang failure philosophy: crash on the unexpected, supervisors restart, validate only at boundaries and return tagged tuples for expected failures."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Let it crash and error kernel design
**Goal:** decide what to handle and what to let die.

- Expected, recoverable outcomes (file missing, user input invalid) return `{error, Reason}`.
- Unexpected states (bug, corrupt invariants) should crash the process; the supervisor restarts it in a known good state.
- Keep crucial state in a small "error kernel" process that does little and rarely crashes; push risky work to short-lived workers.
- Do not catch errors only to log and continue with half-initialised state.
- Use links/monitors to propagate failures; restart intensity in the supervisor turns repeated crashes into escalation.
```erlang
%% worker: pattern match asserts the happy path, a bad value crashes the worker
handle(Req) -> {ok, Parsed} = parse(Req), do(Parsed).
```

## Gotchas
- Crash loops: a worker that fails in `init/1` forever exhausts supervisor intensity and takes down its parent; do slow setup in `handle_continue`.
- Defensive programming everywhere hides the real root cause in logs.

## Self-check
Kill a supervised worker with `exit(Pid, kill)` and confirm a fresh pid with clean state.
