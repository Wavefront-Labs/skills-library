---
id: computing-software.software-engineering.erlang.backpressure-overload
name: backpressure-overload
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-patterns, backpressure-overload]
level: sme
status: draft
description: "Erlang overload protection: bounded mailboxes, call-based flow control, load shedding, sidejob/jobs libraries and TCP active-once."
sources:
  - https://www.erlang.org/doc/system/design_principles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backpressure and overload protection
**Goal:** stay responsive under overload.

- Prefer synchronous `gen_server:call` between producer and consumer so the producer slows down; avoid unbounded `cast`.
- Check `message_queue_len` and shed work early:
```erlang
case erlang:process_info(Pid, message_queue_len) of
    {_, N} when N > 10000 -> {error, overloaded};
    _ -> gen_server:call(Pid, Req)
end.
```
- Use `{active, once}`/`{active, N}` on sockets so the kernel buffers and TCP applies backpressure.
- Libraries for admission control: `jobs`, `sidejob`, `fuse` (circuit breaker); logger has built-in overload protection.
- Timeouts everywhere: every call has a deadline; propagate it downstream.
- Monitor queue lengths and scheduler utilisation and alert before saturation.

## Gotchas
- Retrying on timeout without jitter amplifies overload.

## Self-check
Flood a slow server with casts versus calls and compare memory growth.
