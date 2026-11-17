---
id: computing-software.cryptography-implementation.crypto-libraries.rustls-crypto-provider-selection
name: rustls-crypto-provider-selection
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, rustls-crypto-provider, rustls, rust, aws-lc-rs, ring, fips, cryptoprovider, tls]
level: practitioner
status: docs-checked
description: "Pick and install a rustls CryptoProvider: aws-lc-rs default, ring, FIPS feature, installing a process-level default, and verifying FIPS status at runtime."
sources: ["https://docs.rs/rustls/latest/rustls/crypto/struct.CryptoProvider.html", "https://docs.rs/rustls/latest/rustls/manual/_06_fips/index.html", "https://docs.rs/rustls/latest/rustls/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rustls CryptoProvider selection

rustls 0.23+ separates the TLS state machine from the cryptography, supplied by a `CryptoProvider`.

## Providers
| Provider | Cargo feature | Notes |
|---|---|---|
| aws-lc-rs | `aws_lc_rs` (default) | Built in; has build-time dependencies such as cmake |
| aws-lc-rs FIPS | `fips` | Makes the aws-lc-rs provider use FIPS140-3-approved cryptography |
| ring | `ring` | Built in, optional |
| Third-party | e.g. `rustls-openssl`, `rustls-rustcrypto`, `rustls-symcrypt` | Listed in the rustls crate docs; check maturity |

`default-features = false` removes the implicit aws-lc-rs dependency; the `custom-provider` feature disables implicit
use of the built-in providers, forcing the application to install one. The `prefer-post-quantum` feature (default)
puts X25519MLKEM768 first for the aws-lc-rs provider.

## Installing
```rust
// once at startup, before building any config
rustls::crypto::aws_lc_rs::default_provider()
    .install_default()
    .expect("crypto provider already installed");
```
Applications should call `CryptoProvider::install_default()` early in `main`; libraries use `ClientConfig::builder()`
and rely on the default. Or pick per config with `ClientConfig::builder_with_provider()` /
`ServerConfig::builder_with_provider()`. When more than one provider feature is enabled across the dependency tree,
install one explicitly.

## FIPS
```toml
rustls = { version = "0.23", features = ["fips"] }
```
```rust
rustls::crypto::default_fips_provider()
    .install_default()
    .expect("default provider already set elsewhere");
assert!(client_config.fips());   // ClientConfig::fips() / ServerConfig::fips()
```
`CryptoProvider::fips()` covers only the cryptographic parts; prefer the config-level `fips()`, which also takes
NIST's protocol-level recommendations into account.

## Verify
- [ ] Only one provider is active, or the provider is installed explicitly.
- [ ] `ClientConfig::fips()` / `ServerConfig::fips()` is true in FIPS deployments.

## Checked
2026-11-01. Confirmed against the rustls crate docs, the CryptoProvider page and the manual `_06_fips` page: built-in
providers and their features, `install_default`, `builder_with_provider`, the `fips` feature, `default_fips_provider`,
`fips()` on configs, `custom-provider`, `prefer-post-quantum`, cmake as a build dependency of aws-lc-rs. Removed
unconfirmed claims: the exact panic message, Go as a FIPS build requirement, and performance and algorithm-count
comparisons between providers.
Method: documentation only; no commands were run.
