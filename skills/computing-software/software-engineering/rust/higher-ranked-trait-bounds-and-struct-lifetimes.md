---
id: computing-software.software-engineering.rust.higher-ranked-trait-bounds-and-struct-lifetimes
name: higher-ranked-trait-bounds-and-struct-lifetimes
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-ownership, rust-hrtb, hrtb, for-lifetime, struct-lifetimes]
level: advanced
status: docs-checked
description: "Write structs that hold references with lifetime parameters and closures bounded by for<'a>, and understand when higher-ranked trait bounds are needed."
sources:
  - https://doc.rust-lang.org/nomicon/hrtb.html
  - https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Struct lifetimes and higher-ranked trait bounds

**Goal:** hold borrowed data in structs, and accept callbacks that work for every borrow lifetime.

## Struct lifetimes
A struct can hold references, but then every reference in the definition needs a lifetime annotation. The generic lifetime parameter is declared in angle brackets after the struct name (like a generic type). The annotation means an instance cannot outlive the reference it holds.

```rust
struct ImportantExcerpt<'a> {
    part: &'a str,
}
```

In an `impl` block the lifetime parameter after `impl` and its use after the type name are required; references in method signatures may be tied to the struct's lifetimes or independent, and the lifetime elision rules often make annotations unnecessary (for `&self` methods the return type gets the lifetime of `&self`).

## Higher-ranked trait bounds
The Rustonomicon's example: a struct `Closure<F>` with `func: F` where `F: Fn(&(u8, u16)) -> &u8`. The lifetime of the argument cannot be named at the bound, because it only exists inside the method body and is not fixed (`call` works for any lifetime `&self` has). The desugaring uses a higher-rank trait bound, readable as "for all choices of `'a`":

```rust
impl<F> Closure<F>
    where for<'a> F: Fn(&'a (u8, u16)) -> &'a u8,
{
    fn call(&self) -> &u8 { (self.func)(&self.data) }
}
// equivalently: where F: for<'a> Fn(&'a (u8, u16)) -> &'a u8
```

The Nomicon notes there are not many places outside the `Fn` traits where HRTBs are met, and the `Fn(...)` sugar covers the common cases, so you rarely write `for<'a>` by hand.

## Gotchas
- Before specifying `'static` to satisfy an error message, check whether the reference really lives for the whole program; usually the error stems from a dangling reference or lifetime mismatch, and the fix is to correct that.
- "does not live long enough" (E0597) means the borrowed value is dropped while a reference to it is still in use.

## Checked
2026-11-03. Confirmed against the Rust Book "Validating References with Lifetimes" (struct definitions, `impl` lifetime syntax, elision, `'static` advice, E0597) and the Rustonomicon "Higher-Rank Trait Bounds". Removed: the `Parser<'src>` word-splitting example and its claims about returning `&'src str`, the explicit-`for<'a>` list (`IntoIterator`, `dyn`), self-referential struct and `ouroboros` advice, and the verification tip.
Method: documentation only; no commands were run.
