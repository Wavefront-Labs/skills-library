---
id: computing-software.software-engineering.rust.trait-objects-vs-generics
name: trait-objects-vs-generics
category: computing-software
field: software-engineering
product: rust
tags: [rust, traits, rust-generics, trait-objects, dyn-trait, dyn-compatibility, object-safety, monomorphization, impl-trait, static-dispatch, dynamic-dispatch, rust-traits-generics, rust-trait-bounds, rust-dyn-compat]
level: practitioner
status: verified
description: "Choose between generics (static dispatch), impl Trait and dyn Trait (dynamic dispatch) in Rust, and fix dyn-compatibility (object safety) errors."
sources: ["https://doc.rust-lang.org/book/ch18-02-trait-objects.html", "https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility", "https://doc.rust-lang.org/book/ch10-02-traits.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Trait objects vs generics

**Goal:** pick the dispatch style that fits: zero-cost generics for hot, homogeneous
code; trait objects for heterogeneous collections and plugin boundaries.

## Three forms
```rust
fn render<T: Shape>(s: &T) { ... }          // generic: monomorphized per T, inlinable
fn render(s: &impl Shape) { ... }           // same thing, shorter
fn render(s: &dyn Shape) { ... }            // trait object: one copy, vtable call

let shapes: Vec<Box<dyn Shape>> = vec![Box::new(Circle{..}), Box::new(Square{..})];
fn make() -> impl Iterator<Item = u32> { (0..10).map(|x| x * 2) }   // hidden concrete type
fn make_any(flag: bool) -> Box<dyn Iterator<Item = u32>> { ... }    // different types per branch
```

## Choosing
| Need | Use |
|---|---|
| Max performance, single type per call site | generics / impl Trait |
| Collection of different types | `Vec<Box<dyn Trait>>` |
| Return different concrete types from branches | `Box<dyn Trait>` (or an enum) |
| Reduce compile time / binary size from many instantiations | dyn |
| Closed set of variants you own | an `enum` - often better than both |

## dyn compatibility (formerly "object safety")
A trait can be a `dyn Trait` only if, among other rules:
- no method returns `Self` or takes `Self` by value without `where Self: Sized`;
- no generic methods (`fn visit<V>(&self, v: V)`);
- no associated consts; no `Self: Sized` supertrait.
Error E0038 "the trait cannot be made into an object". Fixes:
```rust
trait Shape {
    fn area(&self) -> f64;
    fn clone_box(&self) -> Box<dyn Shape>;                 // instead of -> Self
    fn scaled(&self, k: f64) -> Self where Self: Sized;    // excluded from the vtable
}
```
Or split the trait: a dyn-compatible core plus an extension trait with the generic methods.

## Trait object details
- `Box<dyn Trait>` defaults to `dyn Trait + 'static`; for borrowed data write
  `Box<dyn Trait + 'a>`.
- Need thread-safety: `Box<dyn Trait + Send + Sync>`.
- Downcasting needs `Any`: `fn as_any(&self) -> &dyn Any`; reaching for it often means
  an enum is the better model.
- Upcasting `&dyn Sub` to `&dyn Super` is stable since Rust 1.86.

## Verify
- [ ] Hot paths use generics; `cargo bloat` / compile time acceptable where generics are wide.
- [ ] Public traits intended for `dyn` use have a test that constructs a `Box<dyn Trait>` (catches accidental incompatibility).

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Ran generics, `&impl Shape`, `&dyn Shape`, `Vec<Box<dyn Shape>>`, `clone_box`, a `where Self: Sized` method called on a concrete type, `-> impl Iterator`, `Box<dyn Iterator>` with different branch types, `&dyn Sub` to `&dyn Sup` upcasting, and `as_any().downcast_ref`.
- Dyn-compatibility rules each failed with E0038: a method returning `Self`, a generic method, an associated const, a `Self: Sized` supertrait. The `where Self: Sized` and `clone_box` fixes compiled.
- Upcasting to supertraits stabilised in 1.86.0 (Rust RELEASES.md: "Stabilize upcasting trait objects to supertraits", fetched).
