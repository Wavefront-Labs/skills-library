---
id: computing-software.software-engineering.rust.futures-poll-and-wakers
name: futures-poll-and-wakers
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-async, rust-futures-poll, future, poll, waker, executor]
level: advanced
status: docs-checked
description: "Understand how Rust futures work: the Future trait, Poll, Context and Waker, and write a minimal future and block_on executor to debug hangs."
sources:
  - https://rust-lang.github.io/async-book/02_execution/02_future.html
  - https://doc.rust-lang.org/std/future/trait.Future.html
  - https://doc.rust-lang.org/std/task/struct.Waker.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Futures, poll and wakers

**Goal:** a mental model that explains "my future never completes".

`Future` is `fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>`. Futures are inert: they make progress only when polled. `poll` does not block; if the value is not ready it returns `Poll::Pending` and stores a clone of the `Waker` from the current `Context`, which is woken when the future can progress. Only the waker from the most recent `poll` call should receive the wakeup. A `Pending` without a stored waker that is ever woken means nothing re-polls the task: it hangs. Once a future has finished, do not poll it again.

```rust
struct Countdown(u32);
impl Future for Countdown {
    type Output = &'static str;
    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        if self.0 == 0 { Poll::Ready("liftoff") }
        else { self.0 -= 1; cx.waker().wake_by_ref(); Poll::Pending } // ask to be polled again
    }
}
```

Use `.await` rather than calling `poll` directly. `Pin<&mut Self>` exists because pinned (immovable) futures may hold pointers between their own fields; the async book says pinning is necessary to enable async/await. Chained futures can be composed into allocation-free state machines.

## Gotchas
- `poll` should return quickly and not block; if work may take a while, offload it to a thread pool. Blocking inside a future stalls the executor thread.
- Do not call `poll` in a tight loop; only re-poll after the waker fires.
- Store the latest waker on each poll with `waker.clone_from(cx.waker())`, which skips the clone when `will_wake` is true.
- `wake_by_ref` is preferred over `waker.clone().wake()`.
- Tests that need a `Context` but expect no wakeups can use `Context::from_waker(Waker::noop())`.

## Verify
Poll `Countdown(3)` by hand in a test with a noop-waker `Context` (or any executor) and check it returns `Pending` three times then `Ready("liftoff")`; then remove the `wake_by_ref` call and observe that a real executor never re-polls it.

## Checked
2026-11-09. Confirmed against std `Future` trait docs (poll contract, waker storage, most-recent-waker rule, inert futures, quick return, tight-loop warning), std `Waker` docs (`wake_by_ref`, `clone_from`/`will_wake`, `Waker::noop`) and the async book futures chapter (state machines, Pin rationale). Removed: "lazy" phrasing beyond "inert", drop-cancels-at-await claim, `join!`/`select!` polling claim, `futures::executor::block_on`, `tokio::time::timeout`, `tokio-console`, `RUST_LOG=tokio=trace`. The async book page was read for the sections quoted only.
Method: documentation only; no commands were run.
