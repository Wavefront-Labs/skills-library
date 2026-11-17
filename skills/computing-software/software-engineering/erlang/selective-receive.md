---
id: computing-software.software-engineering.erlang.selective-receive
name: selective-receive
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-processes, selective-receive]
level: advanced
status: docs-checked
description: "Erlang mailbox semantics: pattern-matched receive, queue scan cost, receive after, flush patterns and message_queue_data."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selective receive and mailbox management
**Goal:** avoid mailbox buildup and quadratic scans.

- `receive` takes the first message, from the start of the queue, that matches a clause (clauses tried top to bottom); all other messages stay in the queue.
- Matching a specific message in a huge queue costs time proportional to the number of messages before it.
- `receive ... after 0 -> ok end` times out immediately if nothing matches, but it still has to inspect the whole queue first. Flush: `flush() -> receive _ -> flush() after 0 -> ok end.`
- A receive on a reference created just before the request can be optimised by the compiler so only messages that arrived after the reference was created are scanned; `erlc +recv_opt_info Mod.erl` prints whether it applied (not meant as a permanent option).
- Inspect: `erlang:process_info(Pid, [message_queue_len, messages])`.
```erlang
process_flag(message_queue_data, off_heap).   % queue messages stay outside the heap, so are not part of its GC
```

## Gotchas
- A long-lived loop whose receive patterns do not cover every message type lets unmatched messages accumulate; add a catch-all clause that logs and drops.
- Monitor `message_queue_len` in production.

## Self-check
Send 100000 non-matching messages to a process and time a selective receive.

## Checked
2026-11-02. Reference Manual "Expressions" (Receive, including after 0 note and reference optimisation), Efficiency Guide "Processes" (message queue cost, recv_opt_info), ERTS `erlang` docs (process_flag message_queue_data, process_info message_queue_len and messages). Removed: "most common production failure" claim.
Method: documentation only; no commands were run.
