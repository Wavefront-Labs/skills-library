---
id: computing-software.software-engineering.crystal.select-statement
name: select-statement
category: computing-software
field: software-engineering
product: crystal
tags: [select-statement, concurrency-fibers, select, timeout, non-blocking, multiplexing, select-when, deadline, crystal]
level: practitioner
status: docs-checked
description: "Wait on several channel operations with select/when, add timeouts with timeout(), and use else for non-blocking."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# select with timeouts and multiple channels

Goal: multiplex channel events.

```crystal
select
when v = a.receive
  puts v
when b.send(1)
  puts "sent"
when timeout(1.second)
  puts "timed out"
end
```
- Each `when` is a select action call: `receive`, `receive?`, `send`, or `timeout(span)` (alone or as `v = ch.receive`); the first ready one runs and the others are cancelled.
- `else` makes it non-blocking: runs immediately if nothing is ready.
- `Channel.select(ops)` and `Channel.non_blocking_select(ops)` take an array of actions built with `ch.receive_select_action`, `ch.receive_select_action?`, `ch.send_select_action(v)` and `timeout_select_action(span)`.
- Timeout pattern: wrap long work in a fiber that sends a result, race with `timeout`.

Gotchas:
- A timed-out fiber keeps running; implement cancellation by a done channel.
- `select` without `else` blocks forever if nothing becomes ready (deadlock).
- A `receive` on a closed channel raises `Channel::ClosedError`; use `receive?` to get nil instead.

Verify: spec with a slow producer expecting the timeout branch.

## Checked

Date 2026-11-03. Confirmed in the language reference select page and the Channel source: select/when/else syntax (else makes it non-blocking), assignment form, timeout(span), receive?, the _select_action naming rule, Channel.select and Channel.non_blocking_select, send_select_action, receive_select_action, receive_select_action? and timeout_select_action. Fixed the real error that said receive? is not allowed in select (the reference uses it) and removed the '(confirm)' hedge.

Method: documentation only; no commands were run.
