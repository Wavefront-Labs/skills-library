---
id: computing-software.software-engineering.rust.procedural-macros-with-syn-and-quote
name: procedural-macros-with-syn-and-quote
category: computing-software
field: software-engineering
product: rust
tags: [rust, proc-macros, syn, quote, derive-macros, attribute-macros, proc-macro2, trybuild, metaprogramming, rust-macros, rust-derive-macros]
level: advanced
status: docs-checked
description: "Write Rust procedural macros (derive, attribute, function-like) with syn and quote: crate setup, parsing, spans and compile errors, hygiene, and testing with trybuild."
sources: ["https://doc.rust-lang.org/reference/procedural-macros.html", "https://docs.rs/syn/latest/syn/", "https://docs.rs/quote/latest/quote/", "https://github.com/dtolnay/trybuild"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Procedural macros with syn and quote

**Goal:** generate boilerplate at compile time with good error messages, when a declarative
`macro_rules!` macro or a trait with generics is not enough.

## When to use one
- `#[derive(MyTrait)]` implementations from struct/enum shape.
- Attribute macros that rewrite an item (`#[route(GET, "/")]`, `#[tokio::main]`).
- Function-like macros needing real parsing (`sql!(...)`).
Try a trait + generic code or `macro_rules!` first: proc macros cost compile time and readability.

## Crate setup
A proc macro must live in its own crate:
```toml
# my_derive/Cargo.toml
[lib]
proc-macro = true
[dependencies]
syn = { version = "2", features = ["full"] }   # "derive" feature is enough for derives
quote = "1"
proc-macro2 = "1"
```
The main crate re-exports it (`pub use my_derive::MyTrait;`) so users add one dependency.

## A derive macro
```rust
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput, Data, Fields};

#[proc_macro_derive(Describe, attributes(describe))]
pub fn derive_describe(input: TokenStream) -> TokenStream {
    let ast = parse_macro_input!(input as DeriveInput);
    expand(&ast).unwrap_or_else(syn::Error::into_compile_error).into()
}

fn expand(ast: &DeriveInput) -> syn::Result<proc_macro2::TokenStream> {
    let name = &ast.ident;
    let (impl_g, ty_g, where_c) = ast.generics.split_for_impl();
    let Data::Struct(s) = &ast.data else {
        return Err(syn::Error::new_spanned(&ast.ident, "Describe only supports structs"));
    };
    let fields = match &s.fields {
        Fields::Named(f) => f.named.iter().map(|f| f.ident.as_ref().unwrap().to_string()).collect::<Vec<_>>(),
        _ => return Err(syn::Error::new_spanned(&s.fields, "expected named fields")),
    };
    Ok(quote! {
        impl #impl_g ::my_crate::Describe for #name #ty_g #where_c {
            fn fields() -> &'static [&'static str] { &[#(#fields),*] }
        }
    })
}
```
Key points:
- Keep logic in functions returning `syn::Result` and convert errors with `into_compile_error()`;
  never `panic!` (a panic becomes a compiler error without a useful span).
- `Error::new_spanned(node, msg)` points the error at the user's code. Combine several with
  `err.combine(other)`.
- `split_for_impl()` handles generics and where clauses correctly.
- Use absolute paths (`::my_crate::Trait`, `::core::option::Option`) in generated code: proc macros
  are unhygienic for items, so a user's local `Option` would otherwise shadow yours.
- `#(#iter),*` repeats; `format_ident!("get_{}", name)` builds identifiers.

## Attribute parsing
syn 2: `attr.parse_nested_meta(|meta| { if meta.path.is_ident("rename") { let s: LitStr = meta.value()?.parse()?; .. } Ok(()) })`. The `darling` library turns attributes into structs.

## Testing and debugging
- `cargo expand` (cargo-expand) shows generated code.
- `trybuild`: compile-pass and compile-fail tests with expected stderr snapshots:
```rust
#[test] fn ui() { let t = trybuild::TestCases::new(); t.pass("tests/ui/ok.rs"); t.compile_fail("tests/ui/enum.rs"); }
```
- Unit-test `expand` with `proc_macro2` token streams (it runs outside the compiler).

## Compile time
`syn` with `full` is a notable build cost; enable only needed features. Keep proc macros deterministic.

## Verify
- [ ] Misuse produces a spanned compile error, verified by a trybuild compile_fail test.
- [ ] Generated code uses fully qualified paths and works with generic types.
- [ ] `cargo expand` output is readable.

## Checked

2026-10-25. Checked against the Rust Reference (proc-macro crate type, panics become compiler errors, unhygienic output), the syn source and Cargo.toml (default features include `derive`; `full` is separate; `Error::new_spanned`, `into_compile_error`, `combine`, `Generics::split_for_impl`, `Attribute::parse_nested_meta`), the quote source (`format_ident!`) and the trybuild README (`TestCases::new`, `pass`, `compile_fail`). Removed an unconfirmed claim about `deluxe` and a build-time statement the sources do not make.

Method: documentation only; no commands were run.
