---
id: computing-software.cryptography-implementation.crypto-libraries.rustls-client-and-server-config
name: rustls-client-and-server-config
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, rustls, rustls-config, rust, tls-1-3, webpki-roots, rustls-platform-verifier, crypto-provider, client-certificates]
level: advanced
status: docs-checked
description: "Configure rustls: choose a crypto provider (aws-lc-rs or ring), install the default, FIPS and post-quantum features, and platform verifier versus bundled roots."
sources: ["https://docs.rs/rustls/latest/rustls/", "https://docs.rs/rustls-platform-verifier/latest/rustls_platform_verifier/", "https://github.com/rustls/rustls/blob/main/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rustls ClientConfig and ServerConfig

rustls implements TLS 1.2 and TLS 1.3 for clients and servers. Most configuration mistakes are about trust roots
and the crypto provider.

## Crypto provider

Since rustls 0.22 you can choose the provider of cryptographic primitives. Per the rustls crate docs:
- `aws_lc_rs` (enabled by default): depends on the `aws-lc-rs` crate, which has extra build-time dependencies
  such as cmake. Use `rustls::crypto::aws_lc_rs::default_provider().install_default()` to make it the default
  `CryptoProvider`, or pass it explicitly when making a `ClientConfig` or `ServerConfig`.
- `ring`: depends on the `ring` crate; use `rustls::crypto::ring::default_provider().install_default()`.
- `fips`: FIPS 140-3-approved cryptography via aws-lc-rs; it also changes the default for
  `ServerConfig::require_ems` and `ClientConfig::require_ems`.
- `prefer-post-quantum` (enabled by default): prioritises X25519MLKEM768 key exchange in the aws-lc-rs-backed
  provider by changing the order of `DEFAULT_KX_GROUPS`.
- `custom-provider`: disables the implicit built-in providers, so the application must install one.
- `default-features = false` removes the implicit dependency on aws-lc-rs.

The current README says that for rustls versions prior to 0.24 both providers shipped inside the rustls crate and
Cargo features selected one; from 0.24 they are separate crates (`rustls-aws-lc-rs`, `rustls-ring`). The rustls team
recommends `rustls-aws-lc-rs`, noting it is harder to build on some platforms but has the complete feature set,
including post-quantum algorithms, while `rustls-ring` is easier to build with a more limited feature set. Check
which rustls version you depend on before copying provider code.

```rust
rustls::crypto::aws_lc_rs::default_provider().install_default().expect("provider");   // rustls 0.23-style
```

## Trust roots

- `rustls-platform-verifier` verifies certificates with the operating system's certificate facilities: Windows
  (Windows API), macOS 10.14+ and iOS (Security.framework), all with revocation support (OCSP and CRLs). On Linux it
  uses the system CA bundle or user-provided certs through webpki, with no revocation support, and WASM uses webpki
  roots. It avoids loading and parsing every platform CA.
- A bundled root set (webpki roots) is the fallback for containers without CA certificates; the rustls docs show
  `with_root_certificates(root_store)` on the config builder.
- Disabling verification needs a custom verifier through the `dangerous()` API; treat any such code as a review
  blocker outside tests. (The exact client, server, ALPN, client-auth, rotation and ticket APIs were not verified
  here; read the rustls docs for your version.)

## Verify

- [ ] Exactly one crypto provider is installed or passed explicitly; startup works in every build feature combination.
- [ ] A connection to a host with an untrusted certificate fails; real hosts succeed in containers (roots present).
- [ ] No `dangerous()` verifier in production code paths.

## Checked

2026-10-28. Confirmed against the rustls crate documentation, the rustls README and the rustls-platform-verifier
documentation: TLS 1.2/1.3, provider choice since 0.22, feature descriptions (`aws_lc_rs`, `ring`, `fips`,
`prefer-post-quantum`, `custom-provider`), `install_default`, 0.24 provider split, platform verifier behaviour per
OS. Removed (not verified on these pages): the list of removed legacy TLS features, the panic-on-two-providers
claim, the client and server code samples (`with_platform_verifier`, ALPN, `with_single_cert`, mTLS verifier,
`ResolvesServerCert`, tickets), and the badssl.com check. The Rust code was not compiled or run.
Method: documentation only; no commands were run.
