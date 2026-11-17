---
id: computing-software.software-engineering.rust.secret-handling-with-zeroize-and-secrecy
name: secret-handling-with-zeroize-and-secrecy
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-security, rust-zeroize, zeroize, secrecy, secrets, memory-wipe]
level: practitioner
status: docs-checked
description: "Keep secrets from lingering or leaking in Rust: zeroize and ZeroizeOnDrop, Zeroizing wrappers, secrecy SecretString and ExposeSecret, serde limits."
sources:
  - https://docs.rs/zeroize
  - https://docs.rs/secrecy/latest/secrecy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Secret handling with zeroize and secrecy

**Goal:** reduce exposure of keys and passwords in memory, logs and errors (defence in depth, not a guarantee).

```rust
use zeroize::{Zeroize, ZeroizeOnDrop, Zeroizing};
use secrecy::{SecretString, ExposeSecret};

#[derive(Zeroize, ZeroizeOnDrop)]
struct SessionKey([u8; 32]);                  // zeroed when dropped

let pw: SecretString = std::env::var("DB_PASSWORD")?.into();
connect(pw.expose_secret());                  // explicit, easy-to-audit access

let mut buf = read_key();
use_key(&buf);
buf.zeroize();                                // volatile writes the compiler cannot optimise away

let tmp = Zeroizing::new([0u8; 5]);           // wrapper that zeroizes its contents on drop
```

- `Zeroize` writes a placeholder (typically zero) over a value's memory using `write_volatile` and memory fences, so it will not be optimised away. It is implemented for core scalar types, slices, arrays and, with the `alloc` feature (default), `Vec` and `String`.
- `Zeroize` derive needs the `zeroize_derive` feature. Types that always hold secrets should use `ZeroizeOnDrop` (a marker trait: derive it, or provide a `Drop` that zeroizes) instead of exposing a public `zeroize()` that could leave them in an invalid state. `#[zeroize(skip)]` omits a field.
- `Zeroizing<Z>` derefs to `Z` and zeroizes it on drop.
- `secrecy`: `SecretBox` and aliases `SecretString` and `SecretSlice` make secret access explicit through `ExposeSecret` and `ExposeSecretMut`, avoid accidental leakage through debug logging, and wipe on drop using zeroize. With the `serde` feature a `SecretBox<T>` can be deserialized, but it is not `Serialize` unless `T` implements the `SerializableSecret` marker trait. Cloning needs the `CloneableSecret` marker.
- `secrecy` does not provide `mlock` or `mprotect` style protection; `zeroize` does not clear registers either.

## Gotchas
- `Vec`, `String` and `CString` zeroize their whole backing capacity but cannot erase copies left by earlier reallocation; allocate them at the right capacity up front and avoid growth.
- Prefer storing sensitive data on the heap to limit move-created copies, but stack spilling can still leave temporary copies; `Pin` can stop moves of stack data.
- Zeroizing does not defend against microarchitectural leaks such as Spectre or Meltdown.
- `#[derive(Debug)]` on a struct with a plain secret field leaks it; wrap fields in a secret type.

## Verify
A test asserting that `format!("{:?}", cfg)` does not contain the secret.

## Checked
Method: docs-checked 2026-11-09 against docs.rs pages for zeroize (read in full except the last section) and secrecy (read in full). Dropped unconfirmed claims about the exact Debug output text, subtle::ConstantTimeEq, mlock crates, prctl, core-dump limits and secret handling via command-line arguments or environment variables.
