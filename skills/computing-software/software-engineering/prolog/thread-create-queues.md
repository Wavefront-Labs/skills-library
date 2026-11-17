---
id: computing-software.software-engineering.prolog.thread-create-queues
name: thread-create-queues
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-threads, thread-create-queues, concurrent-maplist]
level: advanced
status: docs-checked
description: "Create threads with thread_create/3, join them, pass messages through queues and use concurrent_maplist and first_solution."
sources:
  - https://github.com/SWI-Prolog/swipl-devel/blob/master/man/threads.plx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threads and queues
```prolog
?- thread_create(work(1), Id, []), thread_join(Id, Status).   % Status = true
?- thread_self(Me), thread_send_message(Me, hello), thread_get_message(M).
?- message_queue_create(Q), thread_send_message(Q, job(1)).
?- concurrent_maplist(square, [1,2,3], L).
?- first_solution(X, [g1(X), g2(X)], []).
```
- `thread_create(:Goal, -Id, +Options)` starts a thread; `thread_self/1` gives the caller's id.
- `thread_join(+Id, -Status)`: Status is `true`, `false`, `exception(Term)` or `exited(Term)`. A thread that is not joined keeps a small exit-status record until it is. Two threads must not join the same thread.
- `thread_send_message/2` and `thread_get_message/1,2` use a thread's own queue or a queue from `message_queue_create/1`.
- `concurrent_maplist/2..4` works like `maplist` with `once` semantics per goal. It uses min(list length, `cpu_count`) threads and has considerable overhead, so it pays only for goals that take long.
- `first_solution(-X, :Goals, +Options)` runs the goals in threads and takes the first solution.
- The flag `threads` tells whether thread support is present.
## Gotchas
- Use a named predicate (as `square` above) as the closure.
- Join every thread you do not detach.
## Self-check
Create 4 workers reading jobs from a queue and check that `thread_join/2` returns `true` for each.

## Checked

2026-11-03. SWI-Prolog manual threads chapter and library(thread) text (threads.plx): thread_create/3, thread_join/2 status values, message queues, concurrent_maplist/2..4 overhead and thread count, first_solution/3, flag `threads`. Removed: the yall lambda example, the "zombie" wording and unconfirmed performance numbers.

Method: documentation only; no commands were run.
