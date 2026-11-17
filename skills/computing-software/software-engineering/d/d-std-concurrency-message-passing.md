---
id: computing-software.software-engineering.d.d-std-concurrency-message-passing
name: d-std-concurrency-message-passing
category: computing-software
field: software-engineering
product: d
tags: [d-std-concurrency-message-passing, concurrency-parallelism, std-concurrency, spawn, send, receive, tid, ownertid, receivetimeout, message-passing, actor, d]
level: practitioner
status: docs-checked
description: "Use actor-style message passing: spawn threads, send/receive typed messages, ownerTid, receiveTimeout, linkTo, OwnerTerminated handling and immutable/shared sharing rules."
sources:
  - https://dlang.org/phobos/std_concurrency.html
  - https://dlang.org/phobos/core_thread_threadbase.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std.concurrency: spawn, send, receive and Tid

Goal: share nothing, pass messages.

```d
import std.concurrency, std.stdio;
void worker() {
    for (bool run = true; run; )
        receive((int n) { ownerTid.send(n * 2); },
                (string s) { writeln(s); },
                (OwnerTerminated e) { run = false; });
}
auto tid = spawn(&worker);
tid.send(21);
writeln(receiveOnly!int());   // 42
```
- `spawn(&fn, args)`: arguments must not have unshared aliasing, so each is `shared`, `immutable` or free of pointer indirection; the same applies to values passed with `send`.
- `receive`, `receiveTimeout`, `receiveOnly!T`, `prioritySend`, `setMaxMailboxSize`, `thisTid`, `ownerTid`, `register` / `locate` / `unregister`.
- `spawnLinked` makes the parent receive `LinkTerminated` when the child ends; a child can handle `OwnerTerminated`.
- `Generator` provides fiber-based lazy sequences.

Gotchas:
- Sending a `char[]` (mutable aliasing) fails to compile; send `immutable` data or copies.

Verify: run the example; terminate the owner and see the worker exit.

## Checked

2026-11-03. Confirmed against: std.concurrency reference page (spawn, send, receive, Tid functions, message types, Generator) and core.thread.threadbase (`thread_joinAll`).

Removed because the pages read did not confirm it: 'tid.send(true) ack' lifecycle advice, `link` (the function is `spawnLinked`), the 'daemonised worker keeps the process alive' gotcha.

Method: documentation only; no commands were run.
