---
id: computing-software.software-engineering.v-lang.v-select-statement
name: v-select-statement
category: computing-software
field: software-engineering
product: v-lang
tags: [v-select-statement, concurrency-basics, select, channel-select, timeout, multiplex, else-branch, v-lang]
level: advanced
status: docs-checked
description: "Use select with channel receives, sends, a timeout branch or else to watch several channels at once without noticeable CPU load."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
  - https://docs.vlang.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# select on multiple channels

Goal: wait on several channel operations at the same time. The docs say `select` monitors channels
without noticeable CPU load; it looks like `match`: a list of transfers with a branch each.

```v
import time

select {
    a := <-ch1 { println('got ${a}') }     // receive into a new variable
    b = <-ch2 { println('got ${b}') }      // receive into a predeclared variable
    ch3 <- c { println('sent') }           // send
    500 * time.millisecond { println('timeout') }
}
```
- A duration expression is the optional timeout branch, run when no channel became ready in time.
  Without it, `select` waits for an unlimited time.
- `else { ... }` proceeds immediately when no channel is ready. `else` and a timeout are mutually exclusive.
- In statement form, `else` also runs when every channel operation is unavailable because the channels are closed.
  To drain buffered values from a closed channel, use a plain receive with `or {}` instead of `select ... else`.
- `select` can be used as a `bool` expression that is `false` if all channels are closed (the docs mark this example `wip`).
- Receive branches support fixed-array payloads (including aliases) with GCC and Clang.

Gotchas:
- No timeout and no `else` means an unready `select` waits indefinitely.

Verify: a producer that sleeps 5 ms before sending, with a 500 ms timeout branch, takes the receive branch; shorten the
timeout below the delay and the timeout branch runs.

## Checked

Read the Channel Select section of the V documentation (doc/docs.md from the vlang/v repository, the source of docs.vlang.io). Removed claims the page does not state: a `done` channel cancellation idiom, "a closed channel receive case fires immediately", worker-loop and ticker uses, and "syntax changed across releases". The tags previously contained spaces and were fixed.

Method: docs-only read of cited pages, 2026-11-08
