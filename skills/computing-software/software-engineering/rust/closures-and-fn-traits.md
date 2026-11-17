---
id: computing-software.software-engineering.rust.closures-and-fn-traits
name: closures-and-fn-traits
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-closures, fn-traits, fnmut, fnonce, move-closures, capture-modes, callbacks, boxed-closures, rust-iterators-closures, rust-closure-capture]
level: practitioner
status: verified
description: "Understand Rust closure capture (borrow, mutable borrow, move), the Fn/FnMut/FnOnce hierarchy, accepting and storing closures, and move closures for threads."
sources: ["https://doc.rust-lang.org/book/ch13-01-closures.html", "https://doc.rust-lang.org/reference/types/closure.html", "https://doc.rust-lang.org/std/ops/trait.Fn.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Closures and the Fn traits

**Goal:** accept, store and return closures with the least restrictive bound, and fix
"closure may outlive the current function" errors.

## Capture modes
A closure captures each variable in the weakest way its body needs:
- read only -> shared borrow -> closure implements `Fn`
- mutates -> mutable borrow -> `FnMut`
- moves a captured value out (e.g. drops or returns it) -> `FnOnce`
`move` forces capture by value (moving or copying) but does NOT change which Fn trait is
implemented; that depends on what the body does.

Hierarchy: every `Fn` is also `FnMut` and `FnOnce`; every `FnMut` is `FnOnce`.

## Accepting closures: ask for the weakest you can
```rust
fn retry<F, T, E>(mut op: F, times: u32) -> Result<T, E>
where F: FnMut() -> Result<T, E> { ... }        // called repeatedly, may mutate: FnMut

fn on_shutdown(f: impl FnOnce() + Send + 'static) { ... }   // called once: FnOnce (accepts the most closures)
fn sort_by_key<K: Ord>(v: &mut [T], key: impl Fn(&T) -> K)   // called many times, shared: Fn
```
Rule: `FnOnce` if called once, `FnMut` if called many times sequentially, `Fn` if
called concurrently or through `&`.

## Storing closures
```rust
struct Button { on_click: Box<dyn FnMut() + Send> }       // heterogeneous, heap
struct Cache<F: Fn(u64) -> u64> { compute: F }            // generic, zero-cost
```
Function pointers `fn(u64) -> u64` accept non-capturing closures and plain functions.

## Threads, tasks and 'static
```rust
let name = String::from("worker");
std::thread::spawn(move || println!("{name}"));   // without move: E0373 may outlive borrowed value
```
Clone `Arc`s BEFORE the move closure to keep a handle:
`let s = state.clone(); spawn(move || s.update());`
`std::thread::scope` allows borrowing non-'static data in threads without move.

## Returning closures
```rust
fn adder(n: i32) -> impl Fn(i32) -> i32 { move |x| x + n }
```
`move` is required because `n` would be a dangling borrow otherwise.

## Gotchas
- Two closures never have the same type, even if identical; use `Box<dyn Fn>` or a generic to store mixed ones.
- Calling an `FnMut` stored in a struct field needs `(self.f)()` with `&mut self`.
- Edition 2021 captures disjoint fields (`self.a` only), reducing borrow conflicts.

## Verify
- [ ] APIs accept `FnOnce`/`FnMut` where possible, not `Fn` by default.
- [ ] No `.clone()` of large data just to satisfy a closure that could borrow (or use scoped threads).

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Ran every block: `retry` with FnMut (3rd call succeeded), `FnOnce` + Send + 'static, `sort_by_key` with `impl Fn`, `Box<dyn FnMut() + Send>` counter (click 1, click 2), generic `Cache<F: Fn>`, `adder` returning `impl Fn`, `(self.f)()` through a `&mut self` method, `fn` pointer accepting a non-capturing closure, `thread::spawn(move ...)`, `Arc` cloned before move, and `thread::scope` borrowing a Vec.
- Compile-fail cases: spawning without `move` gives E0373 "closure may outlive the current function"; two identical closures in one Vec give E0308 "expected closure, found a different closure"; a `move` closure that calls `drop(s)` passed to `impl Fn()` gives E0507 "cannot move out of `s`, a captured variable in an `Fn` closure", while `move |x| x + k` is still `Fn` (called through `impl Fn`), so `move` does not change the trait.
- Edition 2021+ disjoint capture: a closure pushing to `s.b` while `&s.a` was live compiled.
