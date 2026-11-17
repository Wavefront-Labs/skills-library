---
id: computing-software.software-engineering.erlang.call-cast-info
name: call-cast-info
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-gen-server, call-cast-info]
level: practitioner
status: docs-checked
description: "OTP gen_server messaging: synchronous call with 5000 ms default timeout, asynchronous cast, raw info messages and delayed replies."
sources:
  - https://www.erlang.org/doc/system/design_principles.html
  - https://www.erlang.org/doc/apps/stdlib/gen_server.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# call vs cast vs info and timeouts
**Goal:** choose the right messaging function and handle timeouts.

- `gen_server:call(Srv, Req)` is synchronous and equivalent to `call(Srv, Req, 5000)`; `call/3` takes milliseconds or `infinity`. If no reply arrives in time, the call exits the calling process with an exit term whose reason is `timeout`.
- `gen_server:cast/2` is asynchronous and returns `ok` immediately, ignoring a destination node or process that does not exist. Use cast only when you do not need delivery feedback or backpressure.
- `handle_info/2` receives every other message (a plain `Pid ! Msg`, monitor `'DOWN'` messages, timers), including the atom `timeout` produced by a `{noreply, S, Time}`/`{reply, R, S, Time}` timeout action. The default implementation logs an unexpected message, drops it and returns `{noreply, State}`.
- Reply later: return `{noreply, S}` from `handle_call` and call `gen_server:reply(From, Reply)` when ready; this keeps the server free to handle other requests. The same applies before `{stop, _, _}`: a reply must be sent with `reply(From, Reply)` first.
- `gen_server:send_request/2` (since OTP 23.0) and `receive_response/2` (since OTP 24.0) let one process have several requests outstanding.
```erlang
handle_call({slow, X}, From, S) ->
    spawn_link(fun() -> gen_server:reply(From, work(X)) end),
    {noreply, S}.
```

## Gotchas
- One gen_server process handles messages one at a time, so a slow callback delays every other caller.
- `infinity` as a call timeout waits indefinitely; combine with monitoring or supervision so a hung server does not hang its callers silently.

## Self-check
Write a handler that sleeps 6 seconds and confirm the caller exits with a timeout.

## Checked
Read the gen_server reference (stdlib): call/2 default of 5000, call/3 timeout exit, cast semantics, handle_info default and timeout action, noreply and reply/2 rule, send_request and receive_response "since" versions. Removed: the literal `{timeout, {gen_server, call, ...}}` tuple shape (the page only says the exit term contains the reason `timeout`) and the "OTP 23+" claim for both functions.
Method: docs-only read of cited pages, 2026-11-08
