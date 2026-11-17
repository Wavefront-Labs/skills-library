---
id: computing-software.software-engineering.erlang.proper-properties
name: proper-properties
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-proper, proper-properties]
level: advanced
status: draft
description: "PropEr: ?FORALL properties, built-in generators, ?LET, ?SUCHTHAT, shrinking and running via rebar3 proper."
sources:
  - https://github.com/proper-testing/proper
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Properties and generators
**Goal:** test invariants over generated inputs.

```erlang
-include_lib("proper/include/proper.hrl").
prop_reverse() ->
    ?FORALL(L, list(integer()), lists:reverse(lists:reverse(L)) =:= L).
prop_sort_sorted() ->
    ?FORALL(L, non_empty(list(range(0, 100))),
            begin S = lists:sort(L), hd(S) =< lists:last(S) end).
```
- Generators: `integer()`, `binary()`, `list(T)`, `oneof([...])`, `frequency([{W, G}])`, `?LET(X, G, Expr)`, `?SUCHTHAT(X, G, Cond)`, `?SIZED`.
- Run: `rebar3 proper` (plugin `rebar3_proper`); number of tests set with a flag or option (name unconfirmed here, e.g. `-n`); or `proper:quickcheck(prop_reverse())` in the shell.
- On failure PropEr shrinks to a minimal counter-example; keep failing seeds as unit tests.

## Gotchas
- Too many `?SUCHTHAT` rejections make generation fail; build values constructively.
- Properties must be deterministic apart from the generated input.

## Self-check
Break the property deliberately and read the shrunk counter-example.
