---
id: computing-software.software-engineering.rust.ownership-and-borrowing
name: ownership-and-borrowing
category: computing-software
field: software-engineering
product: rust
tags: [rust, ownership, borrowing, borrow-checker, lifetimes, references, move-semantics, clone, copy, rc, arc, refcell, mutex, cow, interior-mutability, nll, e0502, e0499, e0382, e0597, smart-pointers, clippy, iterators, entry-api, rust-ownership, rust-borrowck-errors, rust-lifetimes, rust-interior-mutability]
level: practitioner
status: docs-checked
description: "Work with the Rust borrow checker instead of against it: ownership and move rules, shared vs mutable borrows, lifetime elision, restructuring patterns, and when Rc/Arc/RefCell/Cow are right."
sources:
  - https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html
  - https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html
  - https://doc.rust-lang.org/nomicon/ownership.html
  - https://rust-lang.github.io/api-guidelines/
  - https://doc.rust-lang.org/error_codes/E0382.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Ownership and borrowing — design data flow the borrow checker accepts

**Goal:** read a borrow-checker error, know which of a handful of restructurings fixes
it, and reach for `clone`, `Rc`, `RefCell` or lifetimes deliberately rather than by trial.

## 1. The rules, compactly
- Each value has exactly one owner; when the owner goes out of scope it is dropped.
- Assignment / passing by value **moves** (non-`Copy` types); the source is unusable
  afterwards (E0382 "use of moved value").
- At any point: **either** any number of `&T` **or** exactly one `&mut T` (E0499, E0502).
- References must not outlive the referent (E0597 "does not live long enough").
- Borrows end at their **last use** (non-lexical lifetimes), not at the closing brace.

## 2. API signatures decide most fights
| Parameter | Meaning | Prefer when |
|---|---|---|
| `&str`, `&[T]`, `&T` | read-only borrow | you only read |
| `&mut T` | exclusive borrow | you modify in place |
| `String`, `Vec<T>`, `T` | take ownership | you store it or consume it |
| `impl AsRef<str>` / `impl Into<String>` | flexible input | public APIs |
Take `&str`, not `&String`; `&[T]`, not `&Vec<T>` (clippy `ptr_arg`). Return owned
values from constructors; return references only when tied to `&self`.

## 3. Fixing the common errors
**E0502: mutable borrow while immutably borrowed**
```rust
let first = &v[0];
v.push(4);            // error: v borrowed by `first`
println!("{first}");
```
Fix: copy out the value (`let first = v[0];`), reorder so the borrow's last use comes
first, or index again after mutation.

**Mutating a map entry you looked up:** use the entry API instead of get-then-insert:
`*counts.entry(word).or_insert(0) += 1;`

**Borrowing two fields of `self`:** methods borrow all of `self`; borrow fields
directly (`let (a, b) = (&mut self.a, &self.b);`) or split into a helper taking the
fields. Two elements of one slice: `split_at_mut` / `get_disjoint_mut` (stable since
Rust 1.86).

**Moving out of a `&mut` / Option field:** `std::mem::take(&mut self.buf)`,
`mem::replace`, or `self.opt.take()`.

**Iterating while mutating the collection:** collect the changes, then apply; or
`retain`/`retain_mut`; or iterate indices.

## 4. Lifetimes
- Elision covers most cases: one input reference → output gets its lifetime; `&self`
  methods → output tied to `self`.
- Write `fn longest<'a>(x: &'a str, y: &'a str) -> &'a str` only when the output could
  come from multiple inputs.
- Struct holding a reference (`struct Parser<'a> { src: &'a str }`) is fine for short-
  lived views; for long-lived state store owned data — lifetime parameters propagate
  to every user.
- `'static` bound (e.g. `thread::spawn`, `tokio::spawn`) means "owns all its data", not
  "lives forever": `move` the data in, or use `std::thread::scope` to borrow from the stack.

## 5. Shared ownership and interior mutability
| Need | Single-thread | Multi-thread |
|---|---|---|
| Several owners | `Rc<T>` | `Arc<T>` |
| Mutate through shared ref | `Cell<T>` (Copy), `RefCell<T>` | `Mutex<T>`, `RwLock<T>`, atomics |
| Borrow-or-own | `Cow<'a, T>` | `Cow` |
| Back-pointer (parent) | `Weak<T>` | `Weak<T>` |
`RefCell` moves the borrow check to runtime: a double `borrow_mut()` panics. Graphs and
doubly-linked structures: prefer an arena / `Vec` with indices (or `slotmap`) over
`Rc<RefCell<…>>` webs.

## 6. When `clone()` is the right answer
Cloning a small `String` or an `Arc` in non-hot code is fine and often clearer than
lifetime gymnastics. Measure before contorting a design; `Arc::clone(&x)` signals a
cheap refcount bump.

## Gotchas
- `Rc` cycles leak (no cycle collector); break them with `Weak`.
- Holding a `MutexGuard` or `RefCell` borrow across `.await` or a long call: deadlocks /
  panics, and `std::sync::MutexGuard` isn't `Send`, so the future won't spawn.
- Temporaries in `match`/`if let` scrutinees live to the end of the statement (edition
  2024 shortened this for `if let` — know your edition).
- `for x in vec` consumes the vec; `for x in &vec` borrows it.
- `.iter().map(...)` closures capturing `&mut` of the same collection never compile —
  restructure, don't fight.

## Verify
- [ ] Function signatures take borrowed slices/strs unless they need ownership.
- [ ] No `Rc<RefCell<_>>` where an index/arena or plain ownership would do.
- [ ] `cargo clippy -- -D warnings` passes (`ptr_arg`, `needless_lifetimes`; `redundant_clone` is a nursery lint — enable it explicitly).
- [ ] No lock guard or `RefCell` borrow held across `.await`.
- [ ] Any `Rc`/`Arc` back-references use `Weak`.
- [ ] You can explain each explicit lifetime parameter that remains.

## Checked

2026-10-25. Checked against the Rust release notes (`get_disjoint_mut` stabilised in 1.86; `if let` temporary scope change in edition 2024), the Clippy lint sources (`ptr_arg` style, `needless_lifetimes` complexity, `redundant_clone` nursery), the error index (E0382, E0499, E0502, E0597 exist with the described meanings), and the std `RefCell` documentation (borrow methods panic when already borrowed). Replaced prose-title entries in `sources` with real URLs.

Method: documentation only; no commands were run.
