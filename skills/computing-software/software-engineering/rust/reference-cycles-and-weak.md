---
id: computing-software.software-engineering.rust.reference-cycles-and-weak
name: reference-cycles-and-weak
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-weak, reference-cycles, rc, arc, memory-leaks, tree-structures, arena, graph, rust-smart-pointers, rust-box-rc-arc]
level: advanced
status: verified
description: "Avoid Rc/Arc reference-cycle leaks in Rust with Weak back-pointers, upgrade/downgrade, and arena or index-based graphs; detect leaks with strong_count."
sources: ["https://doc.rust-lang.org/book/ch15-06-reference-cycles.html", "https://doc.rust-lang.org/std/rc/struct.Weak.html", "https://doc.rust-lang.org/std/sync/struct.Weak.html", "https://doc.rust-lang.org/std/rc/struct.Rc.html#method.new_cyclic"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Reference cycles and Weak

**Goal:** build parent/child links, observers and graphs with shared ownership without leaking
memory through cycles.

## Why cycles leak
`Rc`/`Arc` free the value when the strong count reaches zero. If A holds an `Rc` to B and B holds an
`Rc` to A, neither count reaches zero after external owners drop: memory and their `Drop` side effects
leak forever. This is memory-safe (no UB) and the compiler will not warn.

## Weak for back-pointers
Rule: ownership flows one direction (parent owns children); the reverse link is `Weak`.
```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Node {
    value: i32,
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
}

let parent = Rc::new(Node { value: 1, parent: RefCell::new(Weak::new()), children: RefCell::new(vec![]) });
let child = Rc::new(Node { value: 2, parent: RefCell::new(Weak::new()), children: RefCell::new(vec![]) });
*child.parent.borrow_mut() = Rc::downgrade(&parent);
parent.children.borrow_mut().push(Rc::clone(&child));

if let Some(p) = child.parent.borrow().upgrade() {   // Option<Rc<Node>>: None if parent is gone
    println!("parent = {}", p.value);
}
```
- `Rc::downgrade(&rc)` -> `Weak`; `weak.upgrade()` -> `Option<Rc<T>>`. Always handle `None`.
- `Weak::new()` creates a dangling weak with no allocation (placeholder).
- Threaded: `Arc` + `std::sync::Weak` + `Mutex`/`RwLock` instead of RefCell.
- Self-reference at construction: `Rc::new_cyclic(|weak_self| Node { me: weak_self.clone(), .. })`.

Other typical Weak uses: observer/listener lists (subject holds `Weak` to listeners so they can
drop), caches that should not keep values alive, and callbacks capturing `Weak` self in UI/event code
(`let weak = Rc::downgrade(&this); move || if let Some(this) = weak.upgrade() { .. }`).

## Often better: avoid shared pointers entirely
- **Arena / index graphs:** store nodes in a `Vec<Node>` and link by `usize` index (or
  `slotmap`/`generational-arena` keys to catch stale ids). No Rc, no RefCell, no cycles, cache-friendly.
  `petgraph` for general graphs.
- **Single owner + borrowed traversal:** a tree of `Box`/`Vec` children with parent access passed
  down as `&Node` during recursion.
- **Typed arenas** (`bumpalo`, `typed-arena`) for graphs that live and die together: `&'arena Node`
  references can form cycles safely because the arena frees everything at once.

## Detecting leaks
- Tests: assert `Rc::strong_count(&x) == 1` and `Rc::weak_count` after operations; or count Drop
  calls with a static `AtomicUsize`.
- Run under Miri or Valgrind/heaptrack and check for leaked allocations at exit.

## Verify
- [ ] Every reverse or observer link is `Weak`.
- [ ] Drop-counter test shows all nodes dropped when the root drops.
- [ ] Considered an arena/index design before reaching for `Rc<RefCell<..>>` graphs.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Ran the `Node` tree with `Rc::downgrade` and `parent.upgrade()` (printed `parent = 1`; strong counts 1 and 2, weak count 1); after dropping the root `upgrade()` returned `None`, and a Drop counter showed both nodes dropped (2). A deliberate strong cycle (`a` <-> `b`, strong counts 2 and 2) dropped nothing (counter 0): the leak is silent and the compiler gave no warning. `Rc::new_cyclic` gave a self `Weak` (weak count 1), `Weak::new().upgrade()` is `None`, and `Arc::downgrade(..).upgrade()` returned `Some(5)`.
- `slotmap`, `generational-arena`, `petgraph`, `bumpalo`, `typed-arena` exist on crates.io. Miri/Valgrind/heaptrack leak detection was not run.
