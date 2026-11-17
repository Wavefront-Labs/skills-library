---
id: computing-software.software-engineering.rust.returning-closures-and-iterators-with-impl-trait
name: returning-closures-and-iterators-with-impl-trait
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-iterators-closures, rust-return-impl-trait, impl-trait, boxed-closures, return-position]
level: practitioner
status: docs-checked
description: "Return closures and iterators from Rust functions with impl Trait or Box<dyn Fn>, and how return-position impl Trait captures lifetimes."
sources:
  - https://doc.rust-lang.org/book/ch20-04-advanced-functions-and-closures.html
  - https://doc.rust-lang.org/reference/types/impl-trait.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Returning closures and iterators with impl Trait

**Goal:** return unnameable types without boxing when you can.

```rust
fn returns_closure() -> impl Fn(i32) -> i32 {
    |x| x + 1
}
```

Closures are represented by traits, so you cannot return one directly, and each closure has its own distinct type. `impl Trait` in return position gives an abstract return type: the caller may only use the methods declared by the trait. Each possible return value must resolve to the **same concrete type**. This avoids the heap allocation and dynamic dispatch of the older `Box<dyn Fn(i32) -> i32>` form. Returning `impl Iterator` exposes only the `Iterator` bound instead of the complex concrete type of an iterator chain.

If you need several closures with the same signature but different implementations (for example in a `Vec`), the Book says to use trait objects: `Box<dyn Fn(i32) -> i32>`, since two `impl Fn` return values are different types.

`impl Trait` in argument position is syntactic sugar for a generic parameter `<T: Trait>`, except the type is anonymous and the caller cannot name it with a turbofish; switching between the two can be a breaking change for callers. There must be at least one trait bound, at most one `use<..>` bound and at most one opt-out bound such as `?Sized`.

## Captured lifetimes
Return-position `impl Trait` automatically captures all in-scope generic parameters, including type, const and lifetime parameters (edition 2024). Before the 2024 edition, on free functions and on associated functions and methods of inherent impls, lifetime parameters not appearing in the bounds of the return type were not captured automatically. A `use<..>` bound controls the captured set explicitly (`impl Sized + use<'a, T>`): only one such bound is allowed, all in-scope type and const parameters must be listed, and lifetimes in other bounds must be included. Check your crate's edition.

Functions in traits may also return `impl Trait`, which desugars to an anonymous associated type.

## Checked
2026-11-03. Confirmed against The Rust Book "Advanced Functions and Closures" (returning closures, distinct closure types, `Box<dyn Fn>` for several) and the Rust Reference "Impl trait" page (argument/return position, same-concrete-type rule, iterator advice, capture rules, `use<..>` constraints, return in traits). Removed: the `evens` and `iter_either` (itertools `Either`) examples, `make` enum example, RPITIT stabilisation version and object-safety claim, hidden `DoubleEnded`/`ExactSize` remark, the `'static` default of `Box<dyn Fn>`.
Method: documentation only; no commands were run.
