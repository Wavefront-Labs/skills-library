---
id: computing-software.cryptography-implementation.crypto-libraries.rust-openssl-and-native-tls-crates
name: rust-openssl-and-native-tls-crates
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, rust-openssl-crate, native-tls, rust, openssl, tls]
level: practitioner
status: draft
description: "Use Rust openssl and native-tls crates: vendored versus system OpenSSL, feature flags, SslConnector configuration, error handling, and when to pick rustls instead."
sources: ["https://docs.rs/openssl/latest/openssl/", "https://docs.rs/native-tls/latest/native_tls/", "https://docs.rs/openssl-sys/latest/openssl_sys/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rust openssl and native-tls crates

## openssl crate
```toml
openssl = { version = "0.10", features = ["vendored"] }   # builds OpenSSL from source (openssl-src)
```
- Without `vendored`, `openssl-sys` links the system OpenSSL found via pkg-config or `OPENSSL_DIR`.
  Cross-compiles and static musl builds usually need `vendored`.
- Vendored builds must be updated for OpenSSL CVEs by bumping `openssl-src`; track `cargo audit`.

```rust
use openssl::ssl::{SslConnector, SslMethod, SslVerifyMode, SslVersion};
let mut b = SslConnector::builder(SslMethod::tls_client())?;
b.set_min_proto_version(Some(SslVersion::TLS1_2))?;
b.set_ca_file("ca.pem")?;
let connector = b.build();                         // verify mode PEER by default
let stream = connector.connect("api.example.com", tcp)?;   // SNI + hostname check
```

## native-tls
Uses SChannel (Windows), Security.framework (macOS/iOS), OpenSSL elsewhere. Small API, platform trust store,
but behaviour differs per platform (TLS 1.3 support, cipher sets, client cert formats as PKCS#12).

## Choosing
- rustls: memory-safe, consistent behaviour, no C toolchain; default for new Rust code.
- openssl crate: when you need OpenSSL-specific features (engines/providers, FIPS provider, legacy algorithms).
- native-tls: when OS trust store integration and OS-managed updates matter more than consistency.

## Pitfalls
- `SslConnector::builder` then `set_verify(SslVerifyMode::NONE)` copied from examples; reject in review.
- reqwest/hyper features pulling both openssl and rustls; check `cargo tree -e features`.

## Verify
- [ ] `cargo tree | grep -E 'openssl|rustls'` shows the intended stack; tests hit a wrong-host server and fail.
