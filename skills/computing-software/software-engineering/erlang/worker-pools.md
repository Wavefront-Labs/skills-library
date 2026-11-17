---
id: computing-software.software-engineering.erlang.worker-pools
name: worker-pools
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-patterns, worker-pools]
level: advanced
status: draft
description: "Erlang worker pools: poolboy or wpool, bounded concurrency, checkout and checkin patterns and when a pool is the wrong tool."
sources:
  - https://www.erlang.org/doc/system/design_principles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Worker pools
**Goal:** bound concurrent work against a scarce resource.

```erlang
PoolArgs = [{name, {local, db_pool}}, {worker_module, db_worker}, {size, 10}, {max_overflow, 5}],
{ok, _} = poolboy:start_link(PoolArgs, WorkerArgs),
poolboy:transaction(db_pool, fun(W) -> gen_server:call(W, {query, Sql}) end).
```
- Pools protect external resources (DB connections) from unbounded concurrency; plain processes are cheap, so do not pool plain computation.
- `poolboy:transaction/2` checks out a worker, runs the fun and checks it in even on exceptions.
- Alternatives: `wpool`, `pooler`, or a supervisor with `simple_one_for_one` plus a limiter.
- Size pools from the downstream limit, not the CPU count.
- Poolboy API shown from memory of its README; verify option names for your version.

## Gotchas
- Blocking checkouts with long timeouts create hidden queues; set a timeout and shed load.

## Self-check
Run more concurrent callers than workers and confirm throughput is capped.
