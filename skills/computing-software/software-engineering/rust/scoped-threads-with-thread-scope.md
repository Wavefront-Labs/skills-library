---
id: computing-software.software-engineering.rust.scoped-threads-with-thread-scope
name: scoped-threads-with-thread-scope
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-concurrency, rust-scoped-threads, thread-scope, scoped-threads, borrow]
level: practitioner
status: docs-checked
description: "Borrow local data across threads safely with std::thread::scope instead of Arc and 'static closures, including panic behaviour and the scope lifetimes."
sources:
  - https://doc.rust-lang.org/std/thread/fn.scope.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scoped threads

**Goal:** parallelise over borrowed data without `Arc`, `clone` or `'static`.

This is the example from the `std::thread::scope` documentation:

```rust
use std::thread;

let mut a = vec![1, 2, 3];
let mut x = 0;

thread::scope(|s| {
    s.spawn(|| {
        dbg!(&a);                  // we can borrow `a` here
    });
    s.spawn(|| {
        x += a[0] + a[2];          // and mutably borrow `x`, as no other thread uses it
    });
});

// After the scope, we can modify and access our variables again:
a.push(4);
assert_eq!(x, a.len());
```

Unlike non-scoped threads, scoped threads can borrow non-`'static` data, because the scope guarantees all threads are joined at its end. Threads not manually joined are joined automatically before `scope` returns. Rust's borrow rules still apply: two threads cannot both mutably borrow the same variable.

## Lifetimes
Scoped threads involve two lifetimes: `'scope` (the scope itself, during which new threads may be spawned and may still run) and `'env` (whatever the threads borrow). `'env` must outlast the call to `scope`; local variables defined right before the scope can be borrowed. The bound `'env: 'scope` is part of the `Scope` type.

## Gotchas
- If any automatically joined thread panicked, `scope` panics. To handle a thread's panic, join its handle before the end of the scope.
- Joining waits only for the thread's main function to finish; destructors of thread-local variables in those threads might still be running after `scope` returns.
- Use `std::thread::spawn` when a thread must outlive the caller; that needs `'static` data (owned values, `Arc`).

## Checked
2026-11-03. Confirmed against the `std::thread::scope` function page (signature, borrowing non-`'static` data, automatic joins, panic behaviour, thread-local destructor note, the example, the `'scope`/`'env` lifetimes). Removed: the split_at_mut result example, `rayon`/tokio advice, the 2 MiB stack size, `Builder::spawn_scoped`, `move`-shadowing trick and the test/miri commands, none of which were on pages read.
Method: documentation only; no commands were run.
