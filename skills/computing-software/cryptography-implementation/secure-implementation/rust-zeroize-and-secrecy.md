---
id: computing-software.cryptography-implementation.secure-implementation.rust-zeroize-and-secrecy
name: rust-zeroize-and-secrecy
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, secure-memory, zeroization, zeroize-crate, secrecy-crate, rust, zeroizing, drop, debug-redaction]
level: advanced
status: docs-checked
description: "Wipe secrets in Rust with zeroize and secrecy: derive(Zeroize, ZeroizeOnDrop), Zeroizing<T>, SecretBox, avoiding copies via moves/realloc, and Debug redaction."
sources: ["https://docs.rs/zeroize/latest/zeroize/", "https://docs.rs/secrecy/latest/secrecy/", "https://github.com/RustCrypto/utils/tree/master/zeroize"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rust zeroize and secrecy

Rust frees memory without clearing it, and the optimiser removes "dead"
writes before a drop. `zeroize` performs volatile writes plus a compiler fence
so the wipe is not optimised away; `secrecy` wraps values so they are wiped on
drop and not printed by accident.

## zeroize

```rust
use zeroize::{Zeroize, ZeroizeOnDrop, Zeroizing};

#[derive(Zeroize, ZeroizeOnDrop)]
struct SessionKeys { tx: [u8; 32], rx: [u8; 32] }

let mut pw = String::from("hunter2");
pw.zeroize();                                  // clears contents (and truncates)

let key = Zeroizing::new([0u8; 32]);           // wiped when `key` drops
let buf: Zeroizing<Vec<u8>> = Zeroizing::new(read_secret()?);
```

Check each crypto dependency's documentation for a `zeroize` feature and enable it.

## secrecy

```rust
use secrecy::{ExposeSecret, SecretBox, SecretString};
let api_key: SecretString = SecretString::from(std::env::var("API_KEY")?);
client.auth(api_key.expose_secret());          // explicit, greppable access
println!("{:?}", api_key);                     // Debug does not print the secret
let k: SecretBox<[u8; 32]> = SecretBox::new(Box::new(load_key()));
```

With the `serde` feature, `SecretBox<T>` can be deserialised (clean up the unparsed input); it is not
`Serialize` unless `T` implements `SerializableSecret`. `secrecy` does not lock memory (no mlock/mprotect).

## Copies you still have to avoid

- **Moves copy bytes**: the zeroize docs recommend keeping secrets on the heap
  to reduce copies from Rust move semantics, though stack spilling may still
  leave temporary copies; `Pin` can stop stack data moving.
- **Vec/String growth** reallocates and leaves the old buffer unwiped. Zeroize
  clears the whole capacity but cannot remove earlier copies, so allocate the
  final capacity up front.
- **Swap/core dumps**: zeroize and secrecy do not lock pages; combine with
  mlock and disabled core dumps for high-value keys.

## Checked

2026-10-31. Confirmed in docs.rs zeroize (write_volatile plus memory fences, Zeroize for Vec/String truncates and zeroes capacity, ZeroizeOnDrop marker, Zeroizing wrapper, heap/Pin and reallocation notes) and docs.rs secrecy 0.10.3 (SecretBox, SecretString, ExposeSecret, serde and SerializableSecret, no mlock). Removed: RustCrypto type list, redaction string, 0.10 rename note, hex/format claims, mlock crate names.

Method: documentation only; no commands were run.

## Verify

- [ ] Secret-holding types derive `ZeroizeOnDrop` or are wrapped in `Zeroizing`/`SecretBox`.
- [ ] `Debug` output of config/key structs shows redaction (test with `format!("{:?}")`).
