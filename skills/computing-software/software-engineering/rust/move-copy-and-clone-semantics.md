---
id: computing-software.software-engineering.rust.move-copy-and-clone-semantics
name: move-copy-and-clone-semantics
category: computing-software
field: software-engineering
product: rust
tags: [rust, copy-clone, move-semantics, copy-trait, clone-trait, e0382, ownership, derive]
level: practitioner
status: docs-checked
description: "Understand Rust moves, Copy and Clone: what moves, when to derive Copy, cheap vs deep clones, clone_from, and fixing use-after-move (E0382) without cloning blindly."
sources: ["https://doc.rust-lang.org/std/marker/trait.Copy.html", "https://doc.rust-lang.org/std/clone/trait.Clone.html", "https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html", "https://doc.rust-lang.org/error_codes/E0382.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Move, Copy and Clone semantics

**Goal:** predict when a value is moved or copied, choose the right derives for your types, and
clone deliberately rather than to silence the compiler.

## Moves
Assignment, passing by value, and returning all **move**: a bitwise copy of the value, after
which the source is unusable (no destructor runs on it).
```rust
let a = vec![1, 2];
let b = a;            // move
println!("{a:?}");    // E0382: borrow of moved value
```
Moves happen in `for x in v` (consumes v), closures with `move`, `match v { Some(x) => .. }` on a
non-reference (moves out of v unless x is Copy), and method calls taking `self`.

## Copy
A `Copy` type is duplicated instead of moved; the original stays valid. Rules:
- Only types whose all fields are `Copy` can be `Copy`; never types with `Drop`, heap ownership
  (`String`, `Vec`, `Box`), or `&mut T`.
- `#[derive(Clone, Copy)]` together (Copy requires Clone).
- Derive Copy for small plain-data types (`Point { x: f32, y: f32 }`, ids, enums without data).
  Avoid it for large structs (implicit memcpy everywhere) and for types where adding a non-Copy field
  later would be a breaking change in a public API.

## Clone
`clone()` is explicit and may be expensive (deep copy of `Vec<String>`) or cheap:
- `Rc::clone(&rc)` / `Arc::clone(&a)`: increments a counter; write it in that form to signal cheapness.
- `Arc<str>`: a cheap shared clone of an immutable string.
- `x.clone_from(&y)` reuses x's allocation (useful for buffers in loops).
- Implement Clone by hand only when derive is wrong (e.g. a cache field that should reset).

## Fixing E0382 without cloning
1. Borrow instead: `fn len(v: &Vec<T>)` -> better `&[T]`.
2. Reorder: use the value before moving it.
3. Iterate by reference: `for x in &v`.
4. Take the value out of an Option/struct field: `opt.take()`, `std::mem::take(&mut field)`,
   `std::mem::replace`.
5. Share ownership: `Rc`/`Arc` when several owners genuinely need it.
6. Clone when the data is small or a second independent copy is the real semantics. Cloning is not
   a sin; cloning a large Vec in a hot loop is.

## Partial moves
```rust
let p = Person { name, age };
let n = p.name;      // moves only the field; p.age still usable, p as a whole is not
```
Destructuring with `ref`/`ref mut` or matching on `&p` avoids moves.

## Gotchas
- `#[derive(Clone)]` on a generic struct adds a `T: Clone` bound even if T is only in a PhantomData
  or Arc; implement manually to avoid the bound.
- A closure is Copy or Clone if it captures nothing by unique or mutable reference and everything it captures by copy or move is Copy or Clone.
- `.cloned()` / `.copied()` on iterators of references produce owned items.
- Clippy: `clippy::redundant_clone` (nursery group), `clone_on_copy` (complexity), `clone_on_ref_ptr` (restriction)
  for the `Arc::clone` style.

## Verify
- [ ] No `.clone()` added only to satisfy the borrow checker in hot paths (review each).
- [ ] Copy derived only on small plain-data types.
- [ ] Clippy passes with `clone_on_copy` and `redundant_clone`.

## Checked

2026-10-25. Checked against the std `Copy` and `Clone` source documentation (types with `Drop` or `&mut T` cannot be Copy; derive adds `T: Clone` bounds on generic parameters; `clone_from`), the Rust Reference closure types page (when closures are Clone/Copy), the Clippy lint sources (groups of `redundant_clone`, `clone_on_copy`, `clone_on_ref_ptr`) and the error index (E0382). Removed the unconfirmed `Bytes` example; made the closure and Clippy statements exact.

Method: documentation only; no commands were run.
