---
id: computing-software.software-engineering.rust.non-exhaustive-and-evolving-public-enums
name: non-exhaustive-and-evolving-public-enums
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-patterns-design, rust-non-exhaustive, non-exhaustive, semver, enums, structs, api-evolution]
level: practitioner
status: docs-checked
description: "Use #[non_exhaustive] on enums, structs and variants to allow adding members later, and the construction and matching limits it imposes outside the crate."
sources:
  - https://doc.rust-lang.org/reference/attributes/type_system.html#the-non_exhaustive-attribute
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# #[non_exhaustive] and evolving public types

**Goal:** be able to add variants and fields to public types later.

The Rust Reference: `non_exhaustive` indicates that a type or variant may have more fields or variants added in the future. It can be applied to structs, enums and enum variants, takes no inputs, and has **no effect within the defining crate**.

```rust
#[non_exhaustive]
pub struct Config { pub window_width: u16, pub window_height: u16 }

#[non_exhaustive]
pub enum Error { Message(String), Other }

pub enum Message {
    #[non_exhaustive] Send { from: u32, to: u32, contents: String },
    #[non_exhaustive] Quit,
}
```

Outside the defining crate:
- **Construction:** non-exhaustive structs and variants cannot be built with a struct expression (including functional update syntax). The implicit constant of a unit-like struct and the constructor function of a tuple struct are limited to `pub(crate)` visibility. Enum instances can be constructed (provide a constructor function for a struct).
- **Matching:** matching a non-exhaustive struct or variant needs a struct pattern that includes `..`; for a non-exhaustive enum, matching on variants does not count toward exhaustiveness, so a wildcard arm (`_ =>`) is required.
- **Casts:** numeric casts (`as`) are not allowed on enums that contain any non-exhaustive variant.
- Non-exhaustive types are always considered inhabited in downstream crates.

Use it for error enums and option/config structs you expect to grow, not for closed sets where exhaustive matching helps users.

## Checked
2026-11-03. Confirmed against the Rust Reference "Type system attributes" page, section "The non_exhaustive attribute" (allowed positions, same-crate behaviour, construction, matching, cast and inhabitedness rules). Removed: the `Duration`/`Config::new` example, the Rust 1.78 semver claim, `cargo semver-checks` commands, the clippy `wildcard_enum_match_arm` remark, and the claims that adding or removing the attribute is (in)compatible, which that page does not state.
Method: documentation only; no commands were run.
