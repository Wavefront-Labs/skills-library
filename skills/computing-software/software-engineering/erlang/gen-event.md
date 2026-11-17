---
id: computing-software.software-engineering.erlang.gen-event
name: gen-event
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-otp-more, gen-event]
level: advanced
status: docs-checked
description: "OTP gen_event: event manager, add_handler, notify, sync_notify and handler callbacks."
sources:
  - https://www.erlang.org/doc/system/design_principles.html
  - https://www.erlang.org/doc/apps/stdlib/gen_event.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gen_event managers and handlers
**Goal:** broadcast events to pluggable handlers.

```erlang
gen_event:start_link({local, my_events}),
gen_event:add_handler(my_events, my_handler, []),
gen_event:notify(my_events, {user, joined}),
gen_event:sync_notify(my_events, {user, left}).
%% handler callbacks
init(Args) -> {ok, State}.
handle_event(Event, State) -> {ok, State}.   % or remove_handler / {swap_handler, ...}
handle_call(Req, State) -> {ok, Reply, State}.
terminate(Reason, State) -> ok.
```
- When the manager receives an event sent with `notify/2` or `sync_notify/2`, `Module:handle_event/2` is called for each installed handler. `sync_notify/2` returns `ok` after the handlers have run.
- Returning `remove_handler` deletes the handler by calling `Module:terminate(remove_handler, State)`. Returning `{swap_handler, Args1, NewState, Handler2, Args2}` terminates the old handler and calls `Module2:init({Args2, Term})`, where `Term` is the return value of the old `terminate/2`.
- `add_sup_handler/3` also supervises the connection between the handler and the calling process. When a process that called it terminates, handlers attached to the manager should expect callbacks of the shape `Module:handle_info({'EXIT', Pid, Reason}, State)`. See the gen_event page for the messages the calling process receives when a handler is removed.

## Gotchas
- Handlers and manager are one process: since the manager calls every handler for every event, a slow handler delays the others (inference from the documented call model, not a stated guarantee).
- For release upgrades, a handler whose `.appup` uses `{advanced, Extra}` must implement `code_change/3`, otherwise it crashes with `undef`.

## Self-check
Add two handlers and confirm both see each notification.

## Checked
Read the gen_event reference (stdlib): notify/sync_notify, handle_event/handle_call/terminate callbacks, remove_handler and swap_handler semantics, add_sup_handler, code_change note. Removed: the advice to prefer plain processes or `pg`, and the claim that unsupervised crashing handlers are dropped silently (not stated on the page).
Method: docs-only read of cited pages, 2026-11-08
