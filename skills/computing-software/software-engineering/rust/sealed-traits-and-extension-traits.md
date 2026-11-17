---
id: computing-software.software-engineering.rust.sealed-traits-and-extension-traits
name: sealed-traits-and-extension-traits
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-patterns-design, rust-sealed-traits, sealed-trait, extension-trait, api-evolution]
level: advanced
status: docs-checked
description: "Prevent downstream implementations of your traits with the sealed trait pattern (C-SEALED) so methods can be added without a breaking change."
sources:
  - https://rust-lang.github.io/api-guidelines/future-proofing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed traits

**Goal:** keep the freedom to add trait methods without breaking users.

Some traits are only meant to be implemented within the crate that defines them. The Rust API Guidelines (C-SEALED) recommend the sealed trait pattern:

```rust
/// This trait is sealed and cannot be implemented for types outside this crate.
pub trait TheTrait: private::Sealed {
    fn user_callable(&self);
    #[doc(hidden)]
    fn private_method(&self);          // not for users to call
}

impl TheTrait for usize { /* ... */ }

mod private {
    pub trait Sealed {}
    impl Sealed for usize {}           // those same types, but no others
}
```

The empty private `Sealed` supertrait cannot be named by downstream crates, so implementations of `Sealed` (and therefore `TheTrait`) exist only in the current crate. You can then add methods to `TheTrait` in a non-breaking release, and change the signature of methods that are not publicly documented. Removing a public method or changing the signature of a public method in a sealed trait are still breaking changes. Document in rustdoc that the trait is sealed and not meant to be implemented outside the crate. API guideline examples: `serde_json::value::Index`, `byteorder::ByteOrder`.

## Checked
2026-11-03. Confirmed against the Rust API Guidelines "Future proofing" page (C-SEALED: pattern, rationale, what stays breaking, rustdoc advice, examples). Removed: the extension-trait section (orphan-rule claim, `StrExt` example, `unstable_name_collisions`, inherent-method precedence), mocking and coherence claims, `cargo public-api` / `cargo semver-checks` and `compile_fail` verification advice, none of which are on pages read.
Method: documentation only; no commands were run.
