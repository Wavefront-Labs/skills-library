---
id: computing-software.software-engineering.rust.custom-serde-serializers-and-deserializers
name: custom-serde-serializers-and-deserializers
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-serde-data, rust-serde-custom, serde, custom-deserialize, visitor, serialize-with]
level: advanced
status: docs-checked
description: "Implement custom serde (de)serialisation with serialize_with, deserialize_with, Visitor and DeserializeFrom patterns for non-standard formats."
sources:
  - https://serde.rs/custom-serialization.html
  - https://serde.rs/impl-deserialize.html
  - https://serde.rs/field-attrs.html
  - https://serde.rs/container-attrs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom serde serializers and deserializers

**Goal:** accept messy real-world input (string-or-number, comma lists, legacy dates) without losing type safety.

Cheapest route first: parse via an intermediate type.

```rust
#[derive(Deserialize)]
#[serde(untagged)]
enum StringOrInt { S(String), I(i64) }

fn de_id<'de, D: serde::Deserializer<'de>>(d: D) -> Result<i64, D::Error> {
    match StringOrInt::deserialize(d)? {
        StringOrInt::I(i) => Ok(i),
        StringOrInt::S(s) => s.parse().map_err(serde::de::Error::custom),
    }
}
#[derive(Deserialize)]
struct Item { #[serde(deserialize_with = "de_id")] id: i64 }
```

`#[serde(try_from = "String", into = "String")]` on a type delegates to `TryFrom`/`From` (`into` also needs the type to be `Clone`; the `TryFrom` error type must implement `Display`), ideal for validated newtypes (`Email`, `NonEmptyString`). For full control implement `Visitor`:

```rust
struct CsvVisitor;
impl<'de> serde::de::Visitor<'de> for CsvVisitor {
    type Value = Vec<String>;
    fn expecting(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result { f.write_str("a comma separated string") }
    fn visit_str<E: serde::de::Error>(self, v: &str) -> Result<Self::Value, E> { Ok(v.split(',').map(str::to_owned).collect()) }
}
// d.deserialize_str(CsvVisitor)
```

## Gotchas
- `untagged` gives no informative error when no variant matches; add `#[serde(expecting = "...")]`, and prefer tagged enums.
- Return `D::Error::custom` with context (field name, expected format) for debuggable errors.
- Validation in `Deserialize` means invalid data never constructs the type; keep invariants there.

## Verify
Table test accepted inputs (`"5"`, `5`, `" 5"`) and rejected ones, asserting on error messages with `to_string()`.

## Checked
2026-11-08. Read the serde.rs custom-serialization, impl-deserialize, field-attrs and container-attrs pages in full. Dropped unread sources.
Method: documentation only; no commands were run.
