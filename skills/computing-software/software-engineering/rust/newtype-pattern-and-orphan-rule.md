---
id: computing-software.software-engineering.rust.newtype-pattern-and-orphan-rule
name: newtype-pattern-and-orphan-rule
category: computing-software
field: software-engineering
product: rust
tags: [rust, traits, newtype-pattern, orphan-rule, coherence, type-safety, e0117, wrapper-types, nutype, rust-coherence]
level: practitioner
status: docs-checked
description: "Use Rust newtypes for type safety and validated values, and to work around the orphan rule (E0117) when implementing foreign traits for foreign types."
sources: ["https://doc.rust-lang.org/book/ch20-02-advanced-traits.html#using-the-newtype-pattern-to-implement-external-traits-on-external-types", "https://doc.rust-lang.org/reference/items/implementations.html#orphan-rules", "https://rust-lang.github.io/api-guidelines/type-safety.html#c-newtype"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Newtype pattern and the orphan rule

**Goal:** stop mixing up ids/units at compile time, encode validation in types, and
implement external traits on external types legally.

## Newtypes for type safety
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct OrderId(u64);
#[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
pub struct Meters(f64);

fn ship(order: OrderId, customer: CustomerId)   // swapping arguments is now a compile error
```
Zero runtime cost (`#[repr(transparent)]` guarantees identical layout for FFI).

## Validated newtypes ("parse, don't validate")
```rust
pub struct Email(String);              // field private: only constructible via try_new
impl Email {
    pub fn try_new(s: impl Into<String>) -> Result<Self, EmailError> {
        let s = s.into();
        if s.contains('@') { Ok(Email(s)) } else { Err(EmailError) }
    }
    pub fn as_str(&self) -> &str { &self.0 }
}
```
Every `Email` in the program is valid; functions taking `Email` need no re-checks.
With serde, use `#[serde(try_from = "String")]` so deserialisation validates too.
The `nutype` crate generates these with `sanitize(...)` and `validate(...)` attributes.

## Orphan rule (E0117)
You may implement a trait only if the trait is local to your crate or at least one of the types in the impl (with no uncovered type parameter before it) is local. `impl Display for Vec<MyThing>` or `impl serde::Serialize for chrono::X` in your
crate fails. Fix with a newtype:
```rust
pub struct Lines(pub Vec<String>);
impl fmt::Display for Lines {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f, "{}", self.0.join("\n")) }
}
```
(For serde specifically, `#[serde(with = "module")]` on a field avoids a wrapper.)

## Ergonomics
- Forward the traits you need (derive, or implement `Add` for `Meters`).
- `Deref` to the inner type is tempting but leaks the inner API and undoes the safety
  for validated types; prefer explicit accessor methods (API guidelines discourage
  Deref for non-pointers).
- `From<Inner>` for unvalidated newtypes; `TryFrom` for validated ones.

## Verify
- [ ] Passing an `OrderId` where a `CustomerId` is expected fails to compile.
- [ ] Validated newtypes have no public constructor that skips validation (including Deserialize).

## Checked

2026-10-25. Checked against the Rust Reference (orphan rules, `repr(transparent)`), the error index (E0117), the serde attribute documentation (`#[serde(try_from = "FromType")]` container attribute, `#[serde(with = "module")]` field attribute), the nutype README and the Rust API Guidelines (C-DEREF: only smart pointers implement Deref). Tightened the orphan-rule statement; removed the unconfirmed serde_with remark.

Method: documentation only; no commands were run.
