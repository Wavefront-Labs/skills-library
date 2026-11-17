---
id: computing-software.software-engineering.rust.operator-overloading-and-comparison-traits
name: operator-overloading-and-comparison-traits
category: computing-software
field: software-engineering
product: rust
tags: [rust, std-ops, partialord, partialeq, ord, hash, operator-overloading, eq, comparison]
level: practitioner
status: docs-checked
description: "Overload operators with std::ops (Add, Mul, Index, AddAssign, Neg) and implement PartialEq/Eq/PartialOrd/Ord/Hash consistently, including floats and sort keys."
sources: ["https://doc.rust-lang.org/std/ops/index.html", "https://doc.rust-lang.org/std/cmp/trait.PartialOrd.html", "https://doc.rust-lang.org/std/cmp/trait.Ord.html", "https://doc.rust-lang.org/std/hash/trait.Hash.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operator overloading and comparison traits

**Goal:** numeric-like types that read naturally with operators, and comparison/hash impls that
are consistent so sorting, BTreeMap and HashMap behave.

## std::ops
```rust
use std::ops::{Add, AddAssign, Mul, Neg, Index};

#[derive(Debug, Clone, Copy, PartialEq)]
struct V2 { x: f64, y: f64 }

impl Add for V2 { type Output = V2; fn add(self, o: V2) -> V2 { V2 { x: self.x + o.x, y: self.y + o.y } } }
impl AddAssign for V2 { fn add_assign(&mut self, o: V2) { self.x += o.x; self.y += o.y; } }
impl Mul<f64> for V2 { type Output = V2; fn mul(self, k: f64) -> V2 { V2 { x: self.x * k, y: self.y * k } } }
impl Mul<V2> for f64 { type Output = V2; fn mul(self, v: V2) -> V2 { v * self } } // allowed: V2 is local
impl Neg for V2 { type Output = V2; fn neg(self) -> V2 { V2 { x: -self.x, y: -self.y } } }
```
- Operators take operands **by value**. For non-Copy types (big matrices, BigInt) also implement
  for references: `impl<'a> Add<&'a M> for &'a M` so `&a + &b` does not consume.
- `Index`/`IndexMut` return references; panic on out of range like slices, and offer `get()`.
- Do not overload operators with surprising meaning (`+` for "send"); obey algebra users expect.
- `Deref` is for smart pointers, not for inheritance-like delegation.

## Equality
- `PartialEq`: `==`. `Eq`: marker meaning reflexive (`a == a` always) - floats are PartialEq only
  because `NaN != NaN`.
- Derive when field-wise equality is right. Hand-write for semantic equality (case-insensitive ids)
  and keep `Hash` consistent: **if `a == b` then `hash(a) == hash(b)`**. Violating this breaks
  HashMap lookups silently.

## Ordering
- `PartialOrd::partial_cmp -> Option<Ordering>`; `Ord::cmp -> Ordering` (total order, required by
  `sort`, `BTreeMap`, `max`).
- Derive order is lexicographic by field declaration order, and by variant order for enums. Reorder
  fields or hand-write when that is not the intended order.
- Hand-written: implement `Ord` and make `partial_cmp` return `Some(self.cmp(other))` to stay consistent:
```rust
impl Ord for Task { fn cmp(&self, o: &Self) -> Ordering {
    o.priority.cmp(&self.priority)              // higher priority first
        .then_with(|| self.created.cmp(&o.created))
}}
impl PartialOrd for Task { fn partial_cmp(&self, o: &Self) -> Option<Ordering> { Some(self.cmp(o)) } }
```
- Ord must agree with PartialEq (`cmp == Equal` iff `==`).

## Floats
- Sort floats with `v.sort_by(|a, b| a.total_cmp(b))` (IEEE 754 total order: positive NaN sorts after +inf, negative NaN before -inf) rather
  than `partial_cmp().unwrap()` which panics on NaN.
- For float keys in maps or Ord structs use `ordered-float` (`OrderedFloat`, `NotNan`).

## Sorting helpers
`sort_by_key(|t| (t.group, Reverse(t.score)))`, `sort_unstable_by` (in place, does not allocate),
`std::cmp::Reverse` for descending, `max_by_key`, `binary_search_by`. `sort_by_cached_key` when the
key is expensive.

## Verify
- [ ] Property test: `a == b` implies equal hashes; `cmp` is antisymmetric and transitive.
- [ ] No `partial_cmp(..).unwrap()` on floats.
- [ ] Reference impls exist for heavy non-Copy operand types.

## Checked

2026-10-25. Checked against the std source documentation for `Ord`/`PartialOrd`/`PartialEq`/`Eq` (derive ordering is by field or variant declaration order; `Eq` is reflexive), `Hash` (`k1 == k2 -> hash(k1) == hash(k2)`), `f64::total_cmp` (negative quiet NaN first, positive quiet NaN last), slice sorting docs (`sort_unstable` family is in place and does not allocate; `sort_by_cached_key`), the Rust Reference orphan rules (so `impl Mul<V2> for f64` is allowed) and the ordered-float source (`OrderedFloat`, `NotNan`). Wrong in the draft and fixed: NaN does not always sort last under `total_cmp`; and the hand-written `Ord` text said to derive `PartialOrd`, contradicting the example.

Method: documentation only; no commands were run.
