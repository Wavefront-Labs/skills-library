---
id: computing-software.software-engineering.erlang.gen-server-callbacks
name: gen-server-callbacks
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-gen-server, gen-server-callbacks]
level: practitioner
status: docs-checked
description: "OTP gen_server: init, handle_call, handle_cast, handle_info, terminate, code_change, start_link and return tuples."
sources:
  - https://www.erlang.org/doc/system/design_principles.html
  - https://www.erlang.org/doc/apps/stdlib/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gen_server callbacks and structure
**Goal:** write a correct gen_server module.

```erlang
-behaviour(gen_server).
start_link() -> gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).
get() -> gen_server:call(?MODULE, get).
init([]) -> {ok, #{n => 0}}.
handle_call(get, _From, S = #{n := N}) -> {reply, N, S};
handle_call(inc, _From, S = #{n := N}) -> {reply, ok, S#{n := N + 1}}.
handle_cast(reset, S) -> {noreply, S#{n := 0}}.
handle_info(_Msg, S) -> {noreply, S}.
terminate(_Reason, _S) -> ok.
```
- Return forms: `{reply, R, S}`, `{noreply, S}`, `{stop, Reason, S}`, `{stop, Reason, Reply, S}`, each with an optional timeout, `hibernate` or `{continue, Term}` in place of the timeout where documented.
- `start_link/3,4` does not return until `init/1` has returned. For slow setup return `{ok, S, {continue, Term}}`; `handle_continue/2` runs before any external message is received.
- A `gen_server` does not trap exit signals by default. `terminate/2` is called after a callback returns a stop tuple; on a supervisor shutdown or an `'EXIT'` message from the parent it is called only if the process traps exits (with `Reason = shutdown` from a supervisor using an integer shutdown time).
- `gen_server:stop/1` stops the server synchronously (reason `normal`) and waits for it to terminate.
- Messages that are not calls or casts (including `'EXIT'` and `'DOWN'`) go to `handle_info/2`.

## Gotchas
- Stop reasons other than `normal`, `shutdown` or `{shutdown, Term}` are reported as errors through `logger`.

## Self-check
Start the module, call `inc`, kill it, and watch the supervisor restart it.

## Checked
2026-11-02. STDLIB `gen_server` docs (callback return forms, start_link blocking on init, handle_continue, hibernation, terminate/2 conditions, stop/1, error reporting), OTP Design Principles "gen_server Behaviour". Removed: the self-call deadlock gotcha and the catch-all handle_info opinion (not in the pages).
Method: documentation only; no commands were run.
