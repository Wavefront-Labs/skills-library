---
id: computing-software.software-engineering.erlang.pg-groups
name: pg-groups
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-distribution, pg-groups]
level: advanced
status: docs-checked
description: "Erlang cluster process registry: pg process groups and scopes, global register_name, name conflict resolvers."
sources:
  - https://www.erlang.org/doc/apps/kernel/pg.html
  - https://www.erlang.org/doc/apps/kernel/global.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Process groups with pg and global names
**Goal:** find processes across nodes.

```erlang
{ok, _} = pg:start_link(),              % starts the default scope pg
ok = pg:join(my_group, self()),
Members = pg:get_members(my_group),
Local = pg:get_local_members(my_group).
global:register_name(leader, self()),
global:whereis_name(leader).
```
- `pg` groups are created when a process joins and removed when all members leave. A member that terminates is removed automatically. Scopes are independent of each other; the default scope is `pg`. A scope can be kept local-only by using a cluster-unique scope name such as `pg:start_link(node())`.
- `global` registers a name cluster-wide as an alias for a pid and unregisters it if the process terminates. Registration and locks are atomic across involved nodes. For reliable results the kernel parameters `connect_all` and `prevent_overlapping_partitions` must be enabled.
- Prefer `pg` for pub/sub and pools; use `global` for rare singleton lookups.

## Gotchas
- When two nodes register the same name, a resolve function decides: `global:random_exit_name/3` picks one pid at random and kills the other; `random_notify_name/3` sends the loser `{global_name_conflict, Name}`; `notify_all_name/3` unregisters both.
- Local `pg` membership is not preserved if the scope process exits and restarts.

## Self-check
Join groups on two nodes and read `pg:get_members/1` from both.

## Checked

2026-11-03. Confirmed in the `pg` and `global` module pages. Removed: "eventually consistent", node-disconnect membership removal, the "slow" and "sensitive to partitions" assertions, and the Ra leader-election suggestion.
Method: documentation only; no commands were run.
