---
id: computing-software.software-engineering.erlang.proper-statem
name: proper-statem
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-proper, proper-statem]
level: sme
status: draft
description: "PropEr stateful testing: initial_state, command, precondition, postcondition, next_state and run_commands."
sources:
  - https://github.com/proper-testing/proper
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stateful testing with proper_statem
**Goal:** model-test a stateful system against a simple model.

```erlang
-behaviour(proper_statem).
initial_state() -> #{}.
command(S) -> oneof([{call, kv, put, [key(), val()]},
                     {call, kv, get, [key()]}]).
precondition(_S, _Call) -> true.
next_state(S, _Res, {call, kv, put, [K, V]}) -> S#{K => V};
next_state(S, _, _) -> S.
postcondition(S, {call, kv, get, [K]}, Res) -> Res =:= maps:get(K, S, undefined);
postcondition(_, _, _) -> true.
prop_kv() ->
    ?FORALL(Cmds, commands(?MODULE),
        begin kv:reset(),
              {H, S, R} = run_commands(?MODULE, Cmds),
              ?WHENFAIL(io:format("~p ~p ~p~n", [H, S, R]), R =:= ok)
        end).
```
- Commands are symbolic during generation (`next_state` gets symbolic results) and concrete during execution.
- Always reset external state at the start of each iteration.

## Gotchas
- Using real values inside `next_state` that only exist at run time breaks generation; treat results opaquely.

## Self-check
Seed a bug (e.g. wrong delete) and confirm PropEr produces a short command sequence.
