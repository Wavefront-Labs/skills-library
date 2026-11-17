---
id: computing-software.software-engineering.rust.attribute-macros-with-proc-macro-attribute
name: attribute-macros-with-proc-macro-attribute
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-macros, rust-attribute-macros, attribute-macro, proc-macro-attribute, syn]
level: advanced
status: docs-checked
description: "Write a Rust attribute macro: the proc_macro_attribute signature and rules, parsing the item with syn, emitting with quote, and reporting spanned errors."
sources:
  - https://doc.rust-lang.org/reference/procedural-macros.html
  - https://docs.rs/syn/latest/syn/
  - https://docs.rs/syn/latest/syn/struct.Error.html
  - https://docs.rs/quote/latest/quote/macro.quote.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Attribute macros

**Goal:** `#[my_attr(args)] fn foo() {}` transforms the item it decorates.

Rules from the Rust Reference:
- Procedural macros must be defined in the root of a crate with crate type `proc-macro`; with Cargo set `proc-macro = true` under `[lib]`. They cannot be used from the crate that defines them.
- `#[proc_macro_attribute]` may be applied once, to a `pub` function of type `fn(TokenStream, TokenStream) -> TokenStream` (`TokenStream` from the `proc_macro` crate) with the Rust ABI, no other qualifiers, located in the crate root. It defines the attribute in the macro namespace with the function's name.
- The **first** `TokenStream` is the delimited token tree following the attribute name, without the outer delimiters (empty if there are none). The **second** is the rest of the item, including its other attributes. The item is **replaced** by the zero or more items in the returned stream.
- Attribute macros can be used on items, items in `extern` blocks, inherent and trait implementations, and trait definitions; not as inner attributes.
- A procedural macro must return syntax, panic, or loop endlessly. Panics become compiler errors; infinite loops hang the compiler. Procedural macros are **unhygienic**: output behaves as if written inline, affected by (and affecting) surrounding items and imports.

```rust
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, ItemFn};

#[proc_macro_attribute]
pub fn my_attr(_args: TokenStream, item: TokenStream) -> TokenStream {
    let f = parse_macro_input!(item as ItemFn);   // syn ItemFn: attrs, vis, sig, block
    quote!(#f).into()                             // quote! output converts with .into()
}
```

`syn` parses the input (`ItemFn` needs syn's `full` feature); `quote!` builds the output and converts to a `TokenStream` with `.into()`.

## Errors
Report errors by emitting a spanned `compile_error!`, which gives a better diagnostic than panicking. `parse_macro_input!` does this automatically when parsing fails; for later errors use `.to_compile_error()` or `.into_compile_error()` on a `syn::Error`. `syn::Error::new_spanned(tokens, message)` spans all the tokens of a syntax tree node and may give better messages on stable Rust than `Error::new`.

## Checked
2026-11-03. Confirmed against the Rust Reference "Procedural macros" (crate rules, attribute signature, argument meaning, replacement behaviour, hygiene, panics), the syn crate page and `syn::Error` / `syn::ItemFn` pages (`parse_macro_input!`, `to_compile_error`, `new_spanned`, `ItemFn.block`, `full` feature listing) and the `quote!` page (`.into()` conversion). Removed: the `timed` closure-wrapping example and its `parse_quote!` body, `proc-macro2` dependency, async/`?` behaviour claims, `trybuild`/`macrotest`/`cargo expand` advice, "proc-macro crates export only macros".
Method: documentation only; no commands were run.
