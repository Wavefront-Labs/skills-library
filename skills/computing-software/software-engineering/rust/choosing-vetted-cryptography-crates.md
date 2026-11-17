---
id: computing-software.software-engineering.rust.choosing-vetted-cryptography-crates
name: choosing-vetted-cryptography-crates
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-security, rust-crypto-crates, cryptography, ring, rustcrypto, rustls, aws-lc-rs, libsodium]
level: practitioner
status: docs-checked
description: "Pick maintained Rust crypto crates (rustls, ring, subtle and RustCrypto) for common tasks, using the highest-level API and never rolling your own."
sources:
  - https://github.com/RustCrypto
  - https://docs.rs/ring
  - https://docs.rs/rustls
  - https://rustsec.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing vetted cryptography crates

**Goal:** the right primitive from a maintained crate, used through the highest-level API.

| Need | Use |
|---|---|
| TLS client/server | `rustls`; its default crypto provider is `aws-lc-rs`, and `ring` is selectable with the `ring` crate feature |
| Low-level primitives | `ring` modules: `aead`, `agreement` (ECDH incl. X25519), `digest`, `hkdf`, `hmac`, `pbkdf2`, `rand`, `rsa`, `signature` |
| Constant-time comparison | `subtle` (traits and `Choice` for constant-time code) |
| Everything else (password hashing, other AEADs, other signature schemes) | pick from the RustCrypto organisation crates, then run the selection checks below |

Practical rules:
- Use the highest-level API that does the job: a TLS library for transport, an AEAD interface rather than raw block ciphers.
- `ring::digest` provides SHA-2 and the legacy SHA-1 algorithm; do not use SHA-1 for new security work.
- Do not implement your own padding, protocols or tag comparison; compare secrets with constant-time operations from `subtle`.
- A nonce must never repeat for a given key with an AEAD; design the nonce scheme (counter or random of sufficient size) before choosing the cipher.

Selection checks before adding a crate: recent releases, open advisories on RustSec, whether an independent audit exists (look for it in the crate's own documentation), whether it forbids unsafe code, minimum supported Rust version, and any compliance need (for example a validated module) that restricts the provider choice. When rustls is used, you can pass a custom `crypto::CryptoProvider` to the config builders if the default does not meet a requirement.

## Gotchas
- `ring` has platform-specific feature flags for randomness (for example for wasm or bare-metal targets); read its feature table before targeting those.
- Mixing major versions of the same crypto crate causes trait-mismatch errors; check with `cargo tree -d`.
- This skill is general guidance; regulated systems need a cryptographic review.

## Verify
Check the algorithm's published test vectors against your usage, and run `cargo tree -d` to confirm a single copy of each crypto crate.

## Checked
Read the docs.rs rustls crate page (default provider aws-lc-rs, `ring` feature, `with_crypto_provider`, built-in providers) and the docs.rs ring crate page (module list, SHA-2 and legacy SHA-1, feature flags) plus the subtle crate page (constant-time utilities). Removed because not confirmed on a page read: the specific RustCrypto crate names (chacha20poly1305, aes-gcm, argon2, ed25519-dalek and the rest), the code example, the AES-GCM 2^32 message figure, rand/OsRng advice, FIPS and audit statements about specific crates, and the `age`/`hpke` recommendations. The RustCrypto and RustSec pages were not read.

Method: docs-checked 2026-11-09 against docs.rs rustls, ring and subtle crate pages.
