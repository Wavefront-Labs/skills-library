---
id: computing-software.software-engineering.rust.c-ffi-with-bindgen-and-cbindgen
name: c-ffi-with-bindgen-and-cbindgen
category: computing-software
field: software-engineering
product: rust
tags: [rust, unsafe-rust, ffi, bindgen, cbindgen, c-interop, extern-c, sys-crates, rust-ffi-strings, rust-cdylib]
level: practitioner
status: docs-checked
description: "Call C from Rust with bindgen and -sys crates, expose Rust to C with cbindgen and extern 'C', and handle strings, ownership, callbacks, panics and linking safely."
sources:
  - https://doc.rust-lang.org/nomicon/ffi.html
  - https://rust-lang.github.io/rust-bindgen/
  - https://github.com/mozilla/cbindgen
  - https://doc.rust-lang.org/std/ffi/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# C FFI with bindgen and cbindgen

**Goal:** interoperate with C libraries in both directions without memory-safety bugs at the boundary.

## 1. Calling C: a -sys crate with bindgen
```rust
// build.rs
fn main() {
    println!("cargo::rustc-link-lib=zstd");
    println!("cargo::rerun-if-changed=wrapper.h");
    bindgen::Builder::default()
        .header("wrapper.h")
        .allowlist_function("ZSTD_.*")
        .allowlist_type("ZSTD_.*")
        .parse_callbacks(Box::new(bindgen::CargoCallbacks::new()))
        .generate().expect("bindgen")
        .write_to_file(std::path::PathBuf::from(std::env::var("OUT_DIR").unwrap()).join("bindings.rs"))
        .unwrap();
}
```
```rust
// src/lib.rs
#![allow(non_camel_case_types, non_snake_case, non_upper_case_globals)]
include!(concat!(env!("OUT_DIR"), "/bindings.rs"));
```
Allowlist what you need: with no allowlist rules bindgen generates bindings for everything it parses. Using bindgen as a library in `build.rs` regenerates bindings per target but needs `libclang` for everyone building the crate; the alternative is committing pre-generated bindings, at the cost of maintaining one file per supported target.

## 2. Wrap in a safe API
```rust
pub fn compress(input: &[u8], level: i32) -> Result<Vec<u8>, Error> {
    let bound = unsafe { sys::ZSTD_compressBound(input.len()) };
    let mut out = Vec::with_capacity(bound);
    // SAFETY: out has capacity `bound`; input is valid for input.len() bytes.
    let n = unsafe { sys::ZSTD_compress(out.as_mut_ptr().cast(), bound, input.as_ptr().cast(), input.len(), level) };
    if unsafe { sys::ZSTD_isError(n) } != 0 { return Err(Error::from_code(n)); }
    unsafe { out.set_len(n) };   // SAFETY: C wrote n initialised bytes
    Ok(out)
}
```
Ownership wrappers: a Rust struct holding the C handle with `Drop` calling the C free function.

## 3. Strings
- Rust to C: `let c = CString::new(s)?;` (fails on interior NUL) then `c.as_ptr()`; keep `c` alive for as long as C uses the pointer (`CString::new(s)?.as_ptr()` dangles immediately).
- C to Rust: `unsafe { CStr::from_ptr(p) }.to_str()?` (borrowed; not owned; check for null first). C string literals: `c"hello"` (Rust 1.77).

## 4. Exposing Rust to C
```rust
#[unsafe(no_mangle)]                         // required in edition 2024; accepted in all editions since Rust 1.82
pub extern "C" fn acme_parse(input: *const c_char, out: *mut Order) -> c_int {
    let result = std::panic::catch_unwind(|| { /* ... */ 0 });
    result.unwrap_or(-1)                      // never unwind across the FFI boundary
}
#[repr(C)]
pub struct Order { pub id: u64, pub qty: u32 }
```
```toml
[lib]
crate-type = ["cdylib", "staticlib"]
```
`cbindgen --config cbindgen.toml --crate acme --output include/acme.h` generates the header. Provide matching `acme_*_free` functions: memory allocated by Rust must be freed by Rust.
`extern "C-unwind"` exists for deliberate unwinding; panicking out of plain `extern "C"` aborts (Rust 1.81+).

## 5. Callbacks
Pass `extern "C" fn` pointers plus a `*mut c_void` user-data pointer (`Box::into_raw(Box::new(state))`), reclaim with `Box::from_raw` exactly once.

## Gotchas
- Layout: only `#[repr(C)]` structs/enums have defined layout; Rust enums with data need `#[repr(C, u8)]` or manual tagged unions.
- Integer sizes: use `std::ffi::c_int`/`c_long` (widths differ per platform).
- Thread safety of the C library: mark wrapper types `!Send`/`!Sync` unless documented thread-safe.
- Linking: static vs dynamic (`rustc-link-lib=static=foo`), and bundling vendored sources via the `cc` crate for portability.

## Verify
- Tests exercise the safe wrapper (including error paths) under ASan/Valgrind, the C header compiles in a small C test program linking the cdylib, and no FFI function can panic across the boundary.

## Checked

2026-10-25. Checked against the Rust release notes (RELEASES.md, through 1.99.1), the bindgen book (library usage, allowlisting, requirements), bindgen CHANGELOG, the cbindgen README, the Cargo Book (crate-type values) and the Rust Reference (type layout). Confirmed: C string literals stabilised in 1.77; abort on uncaught panics in `extern "C"` functions from 1.81; `extern "C-unwind"` stable since 1.71; unsafe attributes opt-in stable in 1.82; `CargoCallbacks::new()` constructor; `allowlist_function`/`allowlist_type` and the default of allowlisting everything; `repr(C, u8)` for enums with fields; `cbindgen --config --crate --output`; `cdylib` and `staticlib` crate types. Removed unconfirmed claims about `_Bool` and the Windows width of `long`.

Method: documentation only; no commands were run.
