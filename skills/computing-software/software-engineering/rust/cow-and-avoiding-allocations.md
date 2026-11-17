---
id: computing-software.software-engineering.rust.cow-and-avoiding-allocations
name: cow-and-avoiding-allocations
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-collections-strings, rust-cow, cow, borrowed-owned, allocations]
level: practitioner
status: docs-checked
description: "Use Cow<str> and Cow<[T]> to return borrowed data when unchanged and clone only on modification, with to_mut, into_owned and is_borrowed."
sources:
  - https://doc.rust-lang.org/std/borrow/enum.Cow.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cow and avoiding allocations

**Goal:** APIs that sometimes need to modify input but usually do not.

`Cow` is a clone-on-write smart pointer: it can enclose and give immutable access to borrowed data, and clones the data lazily when mutation or ownership is required. It implements `Deref`, so non-mutating methods can be called directly on the enclosed data.

```rust
use std::borrow::Cow;
fn normalise(s: &str) -> Cow<'_, str> {
    if s.contains('\t') {
        Cow::Owned(s.replace('\t', "    "))      // allocate only when needed
    } else {
        Cow::Borrowed(s)
    }
}
let out = normalise("plain");
assert!(matches!(out, Cow::Borrowed(_)));
let owned: String = out.into_owned();
let mut c = Cow::Borrowed("foo");
c.to_mut().make_ascii_uppercase();               // clones into Cow::Owned("FOO")
```

- `to_mut(&mut self)` returns a mutable reference to an owned value, cloning if necessary.
- `into_owned(self)` on `Borrowed` returns a clone; on `Owned` it moves the data out without cloning.
- `is_borrowed()` is true if `to_mut` would require additional work; `is_owned()` is true if `to_mut` would be a no-op.
- For reference-counted data, `Rc::make_mut` and `Arc::make_mut` give clone-on-write too.

## Checked
2026-11-03. Confirmed against the `std::borrow::Cow` page (clone-on-write description, `Deref`, `to_mut`, `into_owned` clone/move behaviour, `is_borrowed`/`is_owned`, `make_mut` note, examples). Removed: `Cow<'static, str>` field and error-message advice, the "3 words" size claim, `#[serde(borrow)]`, `Arc<str>` comparison, `from_utf8_lossy` mention, pointer-equality test.
Method: documentation only; no commands were run.
