---
id: computing-software.software-engineering.rust.implementing-iterators-and-adaptors
name: implementing-iterators-and-adaptors
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-iterators, iterator-adaptors, intoiterator, iterator-trait, collect, lazy-iterators, extension-traits, itertools, size-hint, rust-iterator-collect]
level: practitioner
status: verified
description: "Write Rust iterators: implementing Iterator and IntoIterator for your types, chaining adaptors, collect targets, returning impl Iterator and extension-trait adaptors."
sources: ["https://doc.rust-lang.org/book/ch13-02-iterators.html", "https://doc.rust-lang.org/std/iter/index.html", "https://doc.rust-lang.org/std/iter/trait.IntoIterator.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Implementing iterators and adaptors

**Goal:** expose your collections and streams as idiomatic iterators so callers get the
full adaptor toolbox with zero-cost loops.

## Implement Iterator
```rust
struct Fib { a: u64, b: u64 }
impl Iterator for Fib {
    type Item = u64;
    fn next(&mut self) -> Option<u64> {
        let r = self.a;
        (self.a, self.b) = (self.b, self.a.checked_add(self.b)?);   // stop on overflow
        Some(r)
    }
}
let evens: Vec<u64> = Fib { a: 0, b: 1 }.filter(|x| x % 2 == 0).take(10).collect();
```
Only `next` is required. Override `size_hint` when you know the length (helps `collect`
preallocate); implement `ExactSizeIterator`/`DoubleEndedIterator`/`FusedIterator` when true.

## IntoIterator for your collection (all three forms)
```rust
impl<'a> IntoIterator for &'a Inventory {
    type Item = &'a Item;
    type IntoIter = std::slice::Iter<'a, Item>;
    fn into_iter(self) -> Self::IntoIter { self.items.iter() }
}
// also `impl IntoIterator for Inventory` (owned) and for `&'a mut Inventory`
```
Then `for item in &inventory {}` works. Add `iter()`/`iter_mut()` methods by convention.

## Returning iterators
```rust
fn active(&self) -> impl Iterator<Item = &User> + '_ {
    self.users.iter().filter(|u| u.active)
}
```
No allocation, lazy. Use `Box<dyn Iterator<Item = T> + '_>` only when branches return
different iterator types (or `either::Either`).

## Adaptors to know
`map, filter, filter_map, flat_map, take_while, skip, step_by, zip, enumerate, chain,
peekable, scan, windows/chunks (slices), fold, try_fold, any/all, position, min_by_key,
sum, product, rev`. `collect` into `Vec`, `HashMap` (from tuples), `String`,
`Result<Vec<_>, E>` (stops at first error) or `Option<Vec<_>>`.
The `itertools` crate adds `chunk_by` (`group_by` is its deprecated old name), `sorted`, `dedup`, `tuple_windows`, `join`.

## Custom adaptors via extension trait
```rust
trait EveryNth: Iterator + Sized { fn every(self, n: usize) -> std::iter::StepBy<Self> { self.step_by(n) } }
impl<I: Iterator> EveryNth for I {}
```

## Gotchas
- Iterators are lazy: `v.iter().map(f);` without a consumer does nothing (compiler warns `unused_must_use`).
- Borrowing: an iterator over `&self.items` borrows self; you can't mutate self inside the loop.
- `collect::<Vec<_>>()` just to call `.len()` or iterate again wastes allocation.

## Verify
- [ ] `for x in &collection` and `.iter().map(...)` compile for your type.
- [ ] Benchmark iterator vs manual loop shows parity (it usually does in release builds).

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Ran: `Fib` with `checked_add(...)?` (first ten evens 0, 2, 8, 34, ..., 196418; the iterator yields 92 terms before the overflow stop), `IntoIterator` for `&Inventory`, `Inventory` and `&mut Inventory` (for loops over all three), `-> impl Iterator<Item = &User> + '_`, the `EveryNth` extension trait on `0..10` (0, 3, 6, 9), collect into `Result<Vec<_>, _>` (stops at first error), `Option<Vec<_>>` (None), `HashMap`, `String`, `windows`, `scan`, `try_fold` with `checked_add`, `position`, `peekable`, `flat_map`.
- itertools 0.14: `chunk_by`, `sorted().dedup()`, `tuple_windows::<(_, _)>()` and `join(", ")` ran; `group_by` warns "deprecated: Use .chunk_by() instead".
