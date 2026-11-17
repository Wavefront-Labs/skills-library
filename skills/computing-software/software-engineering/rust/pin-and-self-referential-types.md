---
id: computing-software.software-engineering.rust.pin-and-self-referential-types
name: pin-and-self-referential-types
category: computing-software
field: software-engineering
product: rust
tags: [rust, ownership, pin, self-referential, unpin, pin-project, futures, box-pin, pin-macro, ouroboros]
level: advanced
status: docs-checked
description: "Understand Pin and Unpin in Rust, pin futures with Box::pin and pin!, project pinned fields with pin-project, and avoid self-referential structs."
sources: ["https://doc.rust-lang.org/std/pin/index.html", "https://rust-lang.github.io/async-book/part-reference/pinning.html", "https://docs.rs/pin-project/latest/pin_project/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pin and self-referential types

**Goal:** get past "`X` cannot be unpinned" errors in async code, and avoid needing
self-referential structs in the first place.

## Why Pin exists
A struct holding a pointer into itself breaks if moved (the pointer dangles). Async
fns compile to such state machines (a borrow held across `.await` points into the
future's own storage). `Pin<P>` promises the pointee will not move again until dropped,
so those futures are safe to poll.
- `Unpin` (auto trait) = moving is fine even when pinned. Almost all normal types are Unpin.
- Futures from `async` blocks can borrow from themselves across `.await`, so they are treated as address-sensitive and `poll` takes `Pin<&mut Self>`.

## Pinning in practice
```rust
let fut = Box::pin(do_work());                 // heap pin: Pin<Box<dyn Future>>, movable handle
let fut = std::pin::pin!(do_work());           // stack pin (Rust 1.68+), Pin<&mut _>
tokio::select! { _ = &mut fut => {}, _ = sleep(d) => {} }   // poll by reference in a loop
```
- Polling the same future in a `loop { select! }` needs it pinned outside the loop and
  referenced (`&mut fut`), otherwise each iteration creates a new future.
- Storing heterogeneous futures: `Vec<Pin<Box<dyn Future<Output = T> + Send>>>`.
- `.boxed()` from `futures::FutureExt` is shorthand for `Box::pin`.
- Recursion in async fns requires boxing (`Box::pin(async move { recurse().await })`).

## Writing a manual Future or Stream
Field access through `Pin<&mut Self>` requires projection. Use `pin-project` (or
`pin-project-lite`), never hand-rolled unsafe:
```rust
#[pin_project]
struct Timed<F> { #[pin] inner: F, started: Instant }
impl<F: Future> Future for Timed<F> {
    type Output = (F::Output, Duration);
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        let this = self.project();
        this.inner.poll(cx).map(|o| (o, this.started.elapsed()))
    }
}
```

## Self-referential structs: avoid
Instead of a struct holding `data: String` and `slice: &str` into it:
- store indices/ranges (`Range<usize>`) and slice on access;
- split ownership: owner struct plus a borrowing view struct with a lifetime;
- use cheap shared handles such as `Arc` or `bytes::Bytes::slice`.
Crates like `ouroboros`/`self_cell` exist for genuine needs (parsers over owned buffers).

## Verify
- [ ] No `unsafe` `Pin::new_unchecked` / `get_unchecked_mut` in application code.
- [ ] Futures reused across `select!` iterations are pinned once outside the loop.

## Checked

2026-10-25. Checked against the std `pin` module docs, the Async Book pinning chapter (`Unpin` is an auto trait; `pin!(...)` for futures used by reference, e.g. with `select!`; `Future::poll` takes `Pin<&mut Self>`), Rust 1.68 release notes (`std::pin::pin!` stabilised), pin-project README (`#[pin_project]`, `self.project()`), futures-rs (`FutureExt::boxed`), and the existence of `bytes::Bytes::slice`, `self_cell` and `ouroboros`. Softened the async-block `Unpin` statement to what the Async Book supports.

Method: documentation only; no commands were run.
