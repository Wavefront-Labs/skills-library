---
id: computing-software.software-engineering.rust.serde-enum-representations-and-format-crates
name: serde-enum-representations-and-format-crates
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-serde-data, rust-serde-enums, serde, enums, tagged, internally-tagged, adjacently-tagged, formats]
level: practitioner
status: docs-checked
description: "Choose serde enum representations (external, internal, adjacent, untagged) deliberately and know which variant kinds each supports."
sources:
  - https://serde.rs/enum-representations.html
  - https://serde.rs/container-attrs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Serde enum representations and format crates

**Goal:** stable wire format for sum types, in the format that fits the job.

```rust
#[derive(Serialize, Deserialize)]
enum Ext { Ping, Move { x: i32 } }                    // external: "Ping" | {"Move":{"x":1}}

#[derive(Serialize, Deserialize)]
#[serde(tag = "type")]
enum Int { Ping, Move { x: i32 } }                    // internal: {"type":"Move","x":1}  (no tuple variants)

#[derive(Serialize, Deserialize)]
#[serde(tag = "t", content = "c")]
enum Adj { Ping, Move(i32) }                          // adjacent: {"t":"Move","c":1}

#[derive(Serialize, Deserialize)]
#[serde(untagged)]
enum Un { Num(i64), Text(String) }                    // guesses: first matching variant wins
```

Externally tagged is the default and works across a broad range of text and binary formats because the variant is known before the content is parsed; it handles struct, tuple, newtype and unit variants. Internally tagged puts the tag next to the variant's fields (common in Java libraries). Adjacently tagged keeps tag and content as two fields (common in the Haskell world). Untagged tries each variant in order and the first that deserializes wins.

All representations work in no-std projects, but externally tagged is the only one that works in no-alloc projects. Deserializing internally tagged, adjacently tagged or untagged enums needs serde's `alloc` Cargo feature (on by default).

## Gotchas
- `#[serde(tag = "...")]` on an enum with a tuple variant is a compile-time error; internal tagging works for struct variants, newtype variants holding structs or maps, and unit variants.
- `untagged` gives no informative error when no variant matches; add `#[serde(expecting = "...")]` for a message. In performance-critical code its implementation can be costly: consider a hand-written `Deserialize` or the `serde-untagged` crate.

## Verify
Golden-file tests per variant and a test that an unknown tag errors as designed.

## Checked
2026-11-08. Read the serde.rs enum-representations and container-attrs pages in full. Dropped format-crate claims that were not on those pages.
Method: documentation only; no commands were run.
