---
id: computing-software.software-engineering.v-lang.v-channels
name: v-channels
category: computing-software
field: software-engineering
product: v-lang
tags: [v-channels, concurrency-basics, channel, chan, buffered-channel, close, try-push, send-receive, v-lang]
level: practitioner
status: docs-checked
description: "Create buffered or unbuffered channels with chan T{cap}, send and receive with <-, close them, and use try_push/try_pop sparingly."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
  - https://docs.vlang.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Channels

Goal: pass data between threads safely. The V docs call channels the preferred way to communicate between threads.

- Declare with `chan objtype`: `ch := chan int{}` (unbuffered, "synchronous") or `ch2 := chan f64{cap: 100}`.
  Channels need not be `mut`. The buffer length is a field of the channel object, not part of the type.
- Send `ch <- 42`; receive `x := <-ch`. Pass channels to threads like normal variables (`spawn worker(ch)`).
- A buffered channel takes pushes without blocking until the buffer is full; the next push blocks.
- Close with `ch.close()`. Pushing to a closed channel is a runtime panic (except through `select` and `try_push()`).
  Popping from a closed channel with an empty buffer returns immediately; handle it with `or {}`:
  `x := <-ch or { break }` inside a `for` loop is the recommended way to drain until closed.
- `ch.close(err)` accepts an optional `IError`, so `or {}` or `?` receivers can tell an error end from a normal close.
- A buffered channel can be closed with unread values still in it; they can still be received afterwards.
- Builtins: `ch.try_push(v)` and `ch.try_pop(mut x)` return `.success`, `.not_ready` or `.closed` immediately;
  `ch.len`, `ch.cap`, `ch.closed`.

Gotchas:
- The docs advise against `try_push`/`try_pop`, `.len` and `.closed` in production: code based on them is often racy.
  Do not decide on `.len` or `.closed`; use `or` branches, error propagation or `select`.
- On an unbuffered channel `try_push()` returns `.not_ready` unless a receiver is ready at the same moment.
- `select` is the tool for waiting on several channels (see v-select-statement).

Verify: a producer thread sends 1..5 then closes; the main loop `x := <-ch or { break }` prints five values and ends.

## Checked

Read the Concurrency, Channels, Buffered Channels, Closing Channels and Special Channel Features sections of the V documentation (doc/docs.md in the vlang/v repository, the source of docs.vlang.io, which renders client-side and returned an empty page to the fetch tool). Removed claims the page does not state: `for v in ch {}` iteration, fan-out worker recipe, "pass channels as parameters, not globals", and a general deadlock statement. The tags previously contained spaces and were fixed.

Method: docs-only read of cited pages, 2026-11-08
