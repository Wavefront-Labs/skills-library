---
id: computing-software.cryptography-implementation.crypto-libraries.rust-crypto-crates-ring-and-rustcrypto
name: rust-crypto-crates-ring-and-rustcrypto
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, rustls, rustcrypto, ring, aes-gcm-crate, chacha20poly1305-crate, rust, aead-trait, zeroize]
level: advanced
status: docs-checked
description: "Pick Rust crypto crates: ring or aws-lc-rs versus the RustCrypto AEAD crates, the aead trait types, nonce uniqueness, and ring's LessSafeKey versus SealingKey."
sources: ["https://docs.rs/ring/latest/ring/aead/index.html", "https://github.com/RustCrypto/AEADs", "https://docs.rs/aead/latest/aead/", "https://github.com/aws/aws-lc-rs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rust crypto crates: ring, aws-lc-rs and RustCrypto

| Crate family | What the docs say | Trade-offs to check |
|---|---|---|
| `ring` | `ring::aead` offers `UnboundKey`, `SealingKey`/`OpeningKey` driven by a `NonceSequence`, and `LessSafeKey` | smaller algorithm set than a general library; you own nonce uniqueness with `LessSafeKey` |
| `aws-lc-rs` | strives to be API-compatible with `ring` (v0.16); uses `aws-lc-sys` or `aws-lc-fips-sys` | C and assembly build dependencies (rustls docs mention cmake) |
| RustCrypto AEADs (`aes-gcm`, `chacha20poly1305`, `aes-gcm-siv`, `aes-siv`, `ccm`, `eax`, `ocb3` ...) | pure Rust; functionality expressed through traits of the `aead` crate | evaluate performance and audit status for your target yourself |

I could not read a primary source for third-party audit claims (the NCC Group report page redirected to its
research index), so no audit status is asserted here. Check each crate's own security policy and RustSec.

## RustCrypto AEAD (the `aead` crate)

The `aead` crate provides an abstract interface for AEAD ciphers: traits `AeadCore`, `AeadInOut` (the legacy
in-place trait is deprecated), `KeyInit`, `Generate`, plus `Payload` (message and AAD), `Nonce` ("single-use value
for ensuring ciphertexts are unique"), `Tag` and an opaque `Error`. Cipher implementations are in the
RustCrypto/AEADs repository; `chacha20poly1305` provides (X)ChaCha20Poly1305. Trait names change between
`aead` releases, so copy code samples from the version you depend on rather than from memory.

## ring AEAD

Per the `ring::aead` docs, `LessSafeKey` is for situations where `OpeningKey`/`SealingKey` and a `NonceSequence`
cannot reasonably be used. Prefer `SealingKey` with a `NonceSequence` that cannot repeat; with `LessSafeKey` you
own nonce uniqueness. Keys start as `UnboundKey::new(&AES_256_GCM, key_bytes)`.

## Choosing

- TLS: rustls with the provider that suits you (see the rustls skill); aws-lc-rs and ring are both supported.
- FIPS: aws-lc-rs via `aws-lc-fips-sys`; see the AWS-LC FIPS skill for status.
- Embedded, `no_std` or WASM needs: check each RustCrypto crate's documentation.
- Run `cargo audit` and read RustSec advisories before adopting any crate.

## Verify

- [ ] `cargo audit` clean; crates are maintained versions.
- [ ] Nonce strategy fits the AEAD (counters via a `NonceSequence`, or random only within the algorithm's limits).
- [ ] Known-answer or Wycheproof-style vectors pass for custom wrappers.

## Checked

2026-10-28. Confirmed against the ring `aead` docs page, the RustCrypto/AEADs repository README, the `aead` crate
docs and the aws-lc-rs README: ring key types, RustCrypto crate list and trait-based design, `Payload`, `Nonce`,
`Error`, aws-lc-rs ring compatibility and FFI crates. Removed (not on these pages or source unreadable): NCC Group
audit claim, `no_std` and zeroize claims, `ed25519-dalek` and other crates, `OsRng` and `generate_*` code, the
`rust-crypto` and `sodiumoxide` status remarks, and the ML-KEM, FIPS-feature and build-tool details for aws-lc-rs.
The Rust code samples were removed rather than run.
Method: documentation only; no commands were run.
