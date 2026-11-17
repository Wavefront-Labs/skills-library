---
id: computing-software.software-engineering.erlang.spawn-and-send
name: spawn-and-send
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-processes, spawn-and-send]
level: intro
status: docs-checked
description: "Erlang process basics: spawn variants, message sending with !, receive with timeout, self() and pid identity."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# spawn, send and receive
**Goal:** write a small server loop with spawned processes.

```erlang
loop(State) ->
    receive
        {From, Ref, get} -> From ! {Ref, State}, loop(State);
        {set, V} -> loop(V);
        stop -> ok
    after 60000 -> loop(State)
    end.
Pid = spawn(fun() -> loop(0) end),
Ref = make_ref(), Pid ! {self(), Ref, get},
receive {Ref, V} -> V after 1000 -> timeout end.
```
- `spawn/1,3`, `spawn_link/1,3`, `spawn_monitor/1,3`, `spawn_opt/2,4` (options include `link`, `monitor`, `{min_heap_size, N}`, `{max_heap_size, N}`).
- `Pid ! Msg` returns `Msg`; sending to a pid never fails, even if the process does not exist. Sending to an unregistered name raises `badarg`.
- Message data is copied between processes, except refc binaries and literals.
- A new process uses 327 words of memory (233 of them heap). The default limit is 1,048,576 simultaneous processes, configurable with the `+P` erl flag.
- The main loop of a process must be tail-recursive or its stack grows until the process dies.

## Gotchas
- Tag requests with a unique `make_ref()` and match it on the reply, otherwise stray replies pollute the mailbox.

## Self-check
Run the example and send `stop`; check `is_process_alive/1`.

## Checked
2026-11-02. Reference Manual "Expressions" (Send), Efficiency Guide "Processes" (327 words, 233-word heap, copying rules, tail-recursive main loop), "System Limits" (1,048,576 processes, `+P`), ERTS `erlang:spawn_opt` option list. Removed: the old 262144 default limit (wrong), "about 300 words", and the `spawn/3` vs closures reload claim.
Method: documentation only; no commands were run.
