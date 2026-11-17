---
id: computing-software.software-engineering.rust.slice-patterns-and-binding-modes
name: slice-patterns-and-binding-modes
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-pattern-matching, rust-slice-patterns, slice-patterns, at-bindings, binding-modes, match-ergonomics]
level: practitioner
status: docs-checked
description: "Match on slices and arrays with rest patterns, @ bindings, ranges and guards, and understand default binding modes."
sources:
  - https://doc.rust-lang.org/reference/patterns.html
  - https://doc.rust-lang.org/book/ch19-03-pattern-syntax.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Slice patterns and binding modes

**Goal:** destructure sequences without index arithmetic.

```rust
fn describe(v: &[i32]) -> String {
    match v {
        [] => "empty".into(),
        [x] => format!("one: {x}"),
        [first, .., last] if first == last => format!("bookends {first}"),
        [first, rest @ ..] => format!("{first} then {} more", rest.len()),
    }
}
```

Rules from the Rust Reference:
- Slice patterns match both fixed-size arrays and dynamically sized slices.
- The rest pattern `..` matches zero or more elements not matched already. It may be used in tuple, tuple struct and slice patterns and may appear **only once** in each. In a slice pattern it can also be the subpattern of an identifier pattern (`rest @ ..`).
- A slice pattern matching an **array** is irrefutable when each element pattern is irrefutable. Matching a **slice**, it is irrefutable only in the form with a single `..` rest pattern or an identifier pattern with `..` as its subpattern.
- A range-from pattern (`1..`) cannot be used as a top-level subpattern inside a slice pattern: `[1.., _]` is invalid.
- `IdentifierPattern → ref? mut? IDENTIFIER ( @ PatternNoTopAlt )?`: the `@` operator (Book) binds a value to a name while testing it against a subpattern, for example `id @ 3..=7`.
- A match guard is an extra `if` condition after the pattern that must also hold; the compiler does not use it for exhaustiveness checking.

## Binding modes (match ergonomics)
Matching a reference with a non-reference pattern automatically dereferences it and changes the default binding mode. The default mode starts as "move"; matching a `&` reference sets mode `ref`; matching a `&mut` sets `ref mut` unless the mode is already `ref`. A binding without `ref`, `ref mut` or `mut` uses the default mode. Explicit `ref`/`ref mut`/`mut` on a binding, and reference patterns, are only accepted when the default mode is "move" (in edition 2024; earlier editions were more permissive).

## Gotchas
- The first matching arm wins.
- A guard on an arm means that arm does not count toward exhaustiveness; keep a catch-all.

## Checked
2026-11-03. Confirmed against the Rust Reference "Patterns" (rest pattern, slice patterns and refutability, identifier patterns, binding modes, range restriction) and The Rust Book "Pattern Syntax" (`@` bindings, match guards). Removed: the argv-parsing example, `let ... else`, `matches!`, `split_first`, `as_bytes` and string advice, clippy `match_ref_pats`, the "unreachable patterns warn" and move-out claims.
Method: documentation only; no commands were run.
