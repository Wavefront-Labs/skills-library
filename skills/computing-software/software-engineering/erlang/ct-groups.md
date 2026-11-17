---
id: computing-software.software-engineering.erlang.ct-groups
name: ct-groups
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-common-test, ct-groups]
level: advanced
status: draft
description: "Common Test groups: groups/0, {group, Name}, parallel, sequence, shuffle, repeat and init_per_group."
sources:
  - https://www.erlang.org/doc/apps/common_test/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Groups, properties and parallel cases
**Goal:** organise cases and run subsets in parallel.

```erlang
all() -> [{group, reads}, {group, writes}].
groups() ->
  [{reads,  [parallel], [get_a, get_b]},
   {writes, [sequence], [put_a, put_b]}].
init_per_group(writes, Config) -> [{db, start_db()} | Config];
init_per_group(_, Config) -> Config.
end_per_group(writes, Config) -> stop_db(?config(db, Config));
end_per_group(_, _) -> ok.
```
- Properties: `parallel`, `sequence` (skip rest on failure), `shuffle`, `{repeat, N}`, `{repeat_until_any_fail, N}`.
- Run just a group: `rebar3 ct --group=reads`.
- `init_per_testcase/2` and `end_per_testcase/2` wrap every case.

## Gotchas
- Cases in a `parallel` group must not share mutable state; start with sequence when debugging.

## Self-check
Run `rebar3 ct --group=reads` and see only those cases.
