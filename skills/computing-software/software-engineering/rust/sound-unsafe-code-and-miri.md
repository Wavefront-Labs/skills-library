---
id: computing-software.software-engineering.rust.sound-unsafe-code-and-miri
name: sound-unsafe-code-and-miri
category: computing-software
field: software-engineering
product: rust
tags: [rust, unsafe-rust, unsafe-code, miri, undefined-behavior, safety-invariants, sanitizers, rust-unsafe-ffi, rust-safety-comments, rust-maybeuninit]
level: practitioner
status: docs-checked
description: "Write sound unsafe Rust: safety contracts and SAFETY comments, encapsulating invariants behind safe APIs, common UB sources, and checking with Miri and sanitizers."
sources:
  - https://doc.rust-lang.org/nomicon/
  - https://doc.rust-lang.org/reference/behavior-considered-undefined.html
  - https://github.com/rust-lang/miri
  - https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Writing sound unsafe code and checking it with Miri

**Goal:** the few `unsafe` blocks you need are justified, minimal, encapsulated, and tested for undefined behaviour.

## 1. What unsafe unlocks
Dereferencing raw pointers, calling `unsafe fn` (including FFI), accessing mutable statics, implementing `unsafe trait`s (`Send`, `Sync`), accessing union fields. Everything else (borrow checking, types) still applies.

## 2. Soundness = safe callers cannot cause UB
```rust
pub struct Buf { ptr: NonNull<u8>, len: usize, cap: usize }   // invariant: len <= cap, ptr valid for cap bytes

impl Buf {
    pub fn get(&self, i: usize) -> Option<u8> {
        if i < self.len {
            // SAFETY: i < len <= cap and ptr is valid for cap initialised bytes (invariant upheld by all constructors/mutators).
            Some(unsafe { *self.ptr.as_ptr().add(i) })
        } else { None }
    }

    /// # Safety
    /// `i` must be less than `self.len()`.
    pub unsafe fn get_unchecked(&self, i: usize) -> u8 {
        // SAFETY: caller guarantees i < len.
        unsafe { *self.ptr.as_ptr().add(i) }
    }
}
```
- Every `unsafe {}` gets a `// SAFETY:` comment stating why preconditions hold; every `unsafe fn` gets a `# Safety` doc section.
- Fields that carry invariants must be private: any safe code in the module can break them, so the **module** is the unit of soundness.
- Lints: `#![deny(unsafe_op_in_unsafe_fn)]` (warns by default in edition 2024), `clippy::undocumented_unsafe_blocks`, `#![forbid(unsafe_code)]` in crates that need none.

## 3. Common UB sources
- Creating a reference (`&`/`&mut`) to unaligned, null, dangling or uninitialised memory, even if never read. Use raw pointers and `addr_of!`/`&raw const` for fields of packed structs or partially initialised data.
- Aliasing: two live `&mut` to the same data, or mutating through a pointer while a `&` exists (Stacked/Tree Borrows rules).
- Reading uninitialised memory as an integer; use `MaybeUninit<T>`.
- Invalid values: a `bool` that is not 0/1, an enum with an invalid discriminant, a `char` outside Unicode scalar range, null in a reference.
- Data races; wrong `unsafe impl Send/Sync`.
- `std::mem::transmute` between types with different layouts; prefer `from_ne_bytes` or a crate that checks the conversion.

## 4. Miri
```bash
rustup +nightly component add miri
cargo +nightly miri test
MIRIFLAGS="-Zmiri-tree-borrows" cargo +nightly miri test     # alternative aliasing model
cargo +nightly miri test -- --skip slow_                      # Miri is much slower than native; skip heavy tests
```
Miri interprets MIR and detects out-of-bounds access, use-after-free, invalid values, alignment errors, data races (aliasing checks via Stacked Borrows or Tree Borrows are experimental) and leaks. It has no access to most platform APIs or FFI. Run it in CI on the crates that contain unsafe code.

## 5. Sanitizers and fuzzing
`RUSTFLAGS="-Zsanitizer=address" cargo +nightly test -Zbuild-std --target x86_64-unknown-linux-gnu` (ASan; also thread, memory; the unstable book notes `--target` and `build-std` may be needed). Combine with `cargo fuzz` for parsers that use unsafe.

## Gotchas
- "It works in tests" means nothing for UB; optimisations may break it in another build or compiler version.
- `unsafe impl Send` for a type containing `Rc` or raw pointers to thread-local data is a classic bug.
- Panics inside unsafe code can leave invariants broken (exception safety); use guards that restore state on drop.
- Before writing unsafe, check for a safe standard API or an existing crate that already encapsulates the operation.

## Verify
- `cargo +nightly miri test` passes for the crate with unsafe code, a search for `unsafe` shows it confined to the intended modules, and each block carries a SAFETY comment (clippy lint enforced).

## Checked

2026-10-25. Checked against the Rust Reference (behavior considered undefined), the Miri README (checks performed, `rustup +nightly component add miri`, `MIRIFLAGS`, `-Zmiri-tree-borrows`, no FFI or most platform APIs), the Rust 2024 edition guide (`unsafe_op_in_unsafe_fn` warns by default), the Clippy source (`undocumented_unsafe_blocks`, restriction group), the unstable book sanitizer page (`-Zsanitizer=address`, `--target`, `build-std`) and the reference note on `&raw const`. Corrected the edition 2024 lint level and the sanitizer command; removed unconfirmed claims (Miri speed factor, `cargo geiger`, crate recommendations).

Method: documentation only; no commands were run.
