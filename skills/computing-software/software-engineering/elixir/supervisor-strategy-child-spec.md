---
id: computing-software.software-engineering.elixir.supervisor-strategy-child-spec
name: supervisor-strategy-child-spec
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, supervisor, one-for-one, rest-for-one, one-for-all, child-spec, max-restarts, restart-temporary, supervisor-strategies, elixir-supervision]
level: practitioner
status: docs-checked
description: "Define supervision trees with child_spec, choose :one_for_one/:rest_for_one/:one_for_all, and tune restart intensity (max_restarts/max_seconds)."
sources: ["https://hexdocs.pm/elixir/Supervisor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Supervisor strategies and child specs

**Goal:** structure restart behaviour deliberately.

```elixir
children = [
  MyApp.Repo,                                # module with child_spec/1
  {MyApp.Cache, ttl: 60_000},               # {module, arg}
  Supervisor.child_spec({Task, fn -> warm() end}, id: :warm, restart: :temporary),
  %{id: :custom, start: {Mod, :start_link, [arg]}, restart: :permanent, shutdown: 5000, type: :worker}
]
Supervisor.start_link(children, strategy: :one_for_one, max_restarts: 3, max_seconds: 5, name: MyApp.Supervisor)
```

## Rules
- `:one_for_one`: restart only the crashed child; `:rest_for_one`: restart it and children started after it (use when later children depend on earlier ones); `:one_for_all`: restart all.
- Children start in list order and stop in reverse order.
- `restart:` `:permanent` (always), `:transient` (only on abnormal exit), `:temporary` (never).
- Exceeding `max_restarts` in `max_seconds` (default 3 in 5) makes the supervisor itself exit, escalating up the tree.
- `:transient` children are not restarted when they exit with `:normal`, `:shutdown` or `{:shutdown, term}`.
- The `:shutdown` key defaults to 5_000 for workers and `:infinity` for supervisors.

## Failure modes
- A child that keeps crashing (for example `init/1` failing every time) exceeds `max_restarts`; keep `init/1` light and move slow work to `handle_continue`.

## Self-check
Kill a child with `Process.exit(pid, :kill)` and verify it restarts with a new pid.

## Checked
2026-11-03: confirmed against the Elixir Supervisor docs (strategies, `max_restarts` default 3 and `max_seconds` default 5, `restart` values, `shutdown` defaults, `Supervisor.child_spec/2`, reverse-order shutdown). Removed: the subtree placement advice and the claim that a failing `init/1` ends in `:shutdown`.
Method: documentation only; no commands were run.
