---
id: computing-software.software-engineering.rust.declarative-macros-macro-rules
name: declarative-macros-macro-rules
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-testing, macro-rules, declarative-macros, metaprogramming, hygiene, repetition]
level: practitioner
status: verified
description: "Write macro_rules! macros: fragment specifiers, repetition, tt-munching, hygiene and $crate paths, exporting, debugging expansion, and when to use functions instead."
sources:
  - https://doc.rust-lang.org/book/ch20-05-macros.html
  - https://doc.rust-lang.org/reference/macros-by-example.html
  - https://veykril.github.io/tlborm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declarative macros (macro_rules!)

**Goal:** remove repetitive boilerplate with macros that are readable, hygienic and produce good errors.

## 1. Shape
```rust
macro_rules! hashmap {
    () => { ::std::collections::HashMap::new() };
    ($($k:expr => $v:expr),+ $(,)?) => {{
        let mut m = ::std::collections::HashMap::new();
        $( m.insert($k, $v); )+
        m
    }};
}
let m = hashmap!{ "a" => 1, "b" => 2, };
```
Arms are tried top to bottom; the first match wins. `$(,)?` accepts a trailing comma.

## 2. Fragment specifiers
`expr`, `ident`, `ty`, `pat` (`pat_param` for pre-2021 behaviour), `path`, `stmt`, `block`, `item`, `literal`, `lifetime`, `meta`, `vis`, `tt` (any single token tree). Captured fragments (other than `tt`, `ident`, `lifetime`) become opaque: they cannot be re-matched against literal tokens later.

Follow-set restrictions: after `$e:expr` only `=>`, `,` or `;` may follow, so design separators accordingly.

## 3. Generating items
```rust
macro_rules! newtype_id {
    ($($(#[$m:meta])* $vis:vis $name:ident),* $(,)?) => {$(
        $(#[$m])*
        #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
        $vis struct $name(pub u64);
        impl ::core::fmt::Display for $name {
            fn fmt(&self, f: &mut ::core::fmt::Formatter<'_>) -> ::core::fmt::Result { write!(f, "{}", self.0) }
        }
    )*};
}
newtype_id!(pub UserId, pub OrderId);
```

## 4. Hygiene and paths
- Local variables created inside a macro do not clash with the caller's (hygiene), but items (functions, structs) and `ident` arguments are not hygienic in the same way.
- In exported macros, refer to your crate's items via `$crate::path::Item`, and to std via `::core::`/`::std::` absolute paths, so they work wherever invoked.
```rust
#[macro_export]           // exported at the crate root: `acme::hashmap!`
macro_rules! ensure {
    ($cond:expr, $err:expr) => { if !$cond { return ::core::result::Result::Err($crate::Error::from($err)); } };
}
```
Within a crate, macros are textually scoped (must be defined before use) unless brought in with `use` after `#[macro_export]`.

## 5. Recursion and tt-munching
Process input token by token by recursing on the remainder (`$($rest:tt)*`); watch `recursion_limit` (128 default) and compile times.

## 6. Debugging
```bash
cargo expand path::to::module      # cargo-expand shows the expanded code
```
`compile_error!("message")` in a fallback arm gives users a clear error for unsupported input.

## When not to use macro_rules
- A generic function or trait does the job: prefer it (better errors, IDE support).
- You need to inspect struct fields or generate code from types (derive): use a procedural macro (`syn` + `quote`).

## Gotchas
- Macros that expand to multiple statements used in expression position need a `{{ ... }}` block.
- Evaluating `$e` twice in the expansion duplicates side effects; bind once with `let`.
- Error spans point into the macro; add matcher arms for common mistakes.

## Verify
- `cargo expand` output is what you intend, `trybuild` UI tests cover compile errors for misuse, and the macro works when invoked from another crate (tests in `tests/`).

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Ran `hashmap!` (empty arm, trailing comma), `newtype_id!` with `$vis` and `$(#[$m:meta])*` (Display output `1 2`), an `ensure!` macro using `::core::result::Result::Err`, a tt-muncher `count!(a b c d)` (4), and `twice!({ println!("once"); 2 })` printing once (bound with `let`, so the side effect is not duplicated).
- Compile-fail: `($e:expr foo)` is rejected: "`$e:expr` is followed by `foo`, which is not allowed for `expr` fragments ... allowed there are: `=>`, `,` or `;`". A 140-token `count!` fails with "recursion limit reached while expanding `count!`" and the help `#![recursion_limit = "256"]`; the Reference limits page says "The default in rustc is 128".
- `cargo expand` and `trybuild` are named as tools only (not run).
