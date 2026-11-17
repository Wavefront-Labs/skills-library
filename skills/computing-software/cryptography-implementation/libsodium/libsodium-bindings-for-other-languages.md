---
id: computing-software.cryptography-implementation.libsodium.libsodium-bindings-for-other-languages
name: libsodium-bindings-for-other-languages
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium-bindings, libsodium, rust, java, dotnet, swift]
level: practitioner
status: docs-checked
description: "Pick maintained libsodium bindings beyond C: Rust (libsodium-sys, dryoc alternatives), Go, Java (lazysodium), .NET, Swift; check versions, minimal builds and API mapping."
sources: ["https://doc.libsodium.org/bindings_for_other_languages", "https://github.com/jedisct1/libsodium-sys-stable", "https://github.com/terl/lazysodium-java", "https://github.com/ektrah/nsec", "https://github.com/brndnmtthws/dryoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# libsodium bindings for other languages

## Choosing a binding
| Language | Options |
|---|---|
| Rust | `libsodium-sys-stable` (listed in the libsodium docs), `dryoc` (pure Rust per its repository description, separate project); `sodiumoxide` is deprecated and its repository archived |
| Go | `github.com/jamesruan/sodium` (listed in the libsodium docs) |
| Java/Android | Lazysodium for Java and Lazysodium for Android (both listed) |
| .NET | NSec (libsodium-based), Geralt, `libsodium-core` (listed as maintenance mode) |
| Swift/iOS | swift-sodium |
| Python | PyNaCl, libnacl, PySodium |
| PHP | built in since PHP 7.2 |
| JS | libsodium.js (`libsodium-wrappers`), `sodium-native` (Node) |

## Evaluation checklist
- Bundled libsodium version and how it updates (vendored source vs system library). Check it is recent:
  the docs name 1.0.22 as the latest stable release, HKDF needs 1.0.19, the XOF functions 1.0.21, and SHA-3 and ML-KEM 1.0.22.
- Maintained in the last year, open issues triaged, security policy.
- Exposes the functions you need (e.g. `crypto_secretstream`, `crypto_kx`, AEAD variants). Some bindings omit
  advanced APIs or build libsodium with `--enable-minimal`.
- Zero-copy and secure memory: does it expose `sodium_malloc`/`memzero`, or copy keys into managed heap?
- Calls `sodium_init()` for you (the docs say it is safe to call more than once and from several threads, and that libsodium functions are thread-safe after it returns).

## Interop
Bindings that wrap libsodium use the same primitives, so test cross-binding round trips for every primitive you use. Pure reimplementations such as dryoc must be tested against libsodium output.

## Verify
- [ ] Cross-binding round-trip test in CI for each primitive used.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: the docs list the cited bindings and note PHP 7.2 and later ships support; libsodium 1.0.22 is the latest stable; the --enable-minimal configure option exists; sodium_init is safe to repeat and thread-safe; repository state (GitHub): sodiumoxide archived and deprecated, dryoc, swift-sodium, NSec, libsodium-sys-stable and libsodium.js not archived. Removed unconfirmed claims about Tink, JNA, golang.org/x/crypto and cross-binding examples.

Method: documentation only; no commands were run.
