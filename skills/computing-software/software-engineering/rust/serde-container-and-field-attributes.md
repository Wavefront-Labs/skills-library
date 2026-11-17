---
id: computing-software.software-engineering.rust.serde-container-and-field-attributes
name: serde-container-and-field-attributes
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-serde-data, rust-serde-attributes, serde, attributes, rename, default, skip, flatten]
level: practitioner
status: docs-checked
description: "Control JSON and other formats with serde attributes: rename_all, default, skip_serializing_if, flatten, deny_unknown_fields, alias and with."
sources:
  - https://serde.rs/attributes.html
  - https://serde.rs/container-attrs.html
  - https://serde.rs/field-attrs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# serde container and field attributes

**Goal:** map Rust types to an external wire format you do not control.

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct User {
    user_id: u64,                                   // "userId"
    #[serde(default)]
    roles: Vec<String>,                             // missing -> empty
    #[serde(skip_serializing_if = "Option::is_none")]
    nickname: Option<String>,
    #[serde(alias = "mail", rename = "email")]
    email_address: String,
    #[serde(flatten)]
    extra: std::collections::HashMap<String, serde_json::Value>, // collects remaining keys
    #[serde(with = "duration_secs")]                // your module with serialize and deserialize fns
    timeout: std::time::Duration,
    #[serde(skip)]
    cache: Option<String>,
}
```

Other useful ones: `#[serde(default = "path::fn")]` for non-`Default` defaults; `serialize_with` / `deserialize_with` for single-direction customisation; `#[serde(bound = "T: Display")]` to fix wrong inferred bounds; `rename(serialize = "a", deserialize = "b")`; `transparent` for newtypes (`struct Id(u64)` serialises as the number).

## Gotchas
- `flatten` is not supported together with `deny_unknown_fields`, on either the outer struct or the flattened field.
- `rename_all` on an enum renames its variants; use `rename_all_fields` to rename the fields of its struct variants.
- Without `deny_unknown_fields`, unknown fields are ignored for self-describing formats like JSON, so typos in config files go unnoticed. Add `#[serde(deny_unknown_fields)]` on structs that do not use `flatten`.

## Verify
Round-trip tests: `assert_eq!(serde_json::from_str::<User>(&serde_json::to_string(&u)?)?, u)` plus a golden JSON string from the real producer.

## Checked
2026-11-08. Read the serde.rs attributes, container-attrs and field-attrs pages in full. Removed the unsupported flatten plus deny_unknown_fields combination from the example.
Method: documentation only; no commands were run.
