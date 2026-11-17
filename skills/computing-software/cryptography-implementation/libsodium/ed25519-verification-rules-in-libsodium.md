---
id: computing-software.cryptography-implementation.libsodium.ed25519-verification-rules-in-libsodium
name: ed25519-verification-rules-in-libsodium
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, crypto-sign-verify-detached, ed25519, signature-verification, libsodium, malleability]
level: advanced
status: docs-checked
description: "Know how libsodium crypto_sign_verify_detached checks Ed25519: canonical S, small-order and non-canonical key rejection, cofactorless equation, and interop effects."
sources: ["https://doc.libsodium.org/public-key_cryptography/public-key_signatures", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_sign/ed25519/ref10/open.c"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ed25519 verification rules in libsodium

`crypto_sign_verify_detached(sig, m, mlen, pk)` returns 0 on success, -1 otherwise.

## What libsodium rejects
- Non-canonical S: the top bits of `sig[63]` are tested and, if set, S must pass `sc25519_is_canonical` (S < L); this prevents signature malleability.
- Non-canonical encodings of the public key A, small-order A, an A that fails to decode, and a small-order or undecodable R.
- The final test computes `R - ([S]B - [k]A)` and accepts when the result has small order, so a mixed-order difference is tolerated; it is not a plain byte comparison of a recomputed R.
- Building with `ED25519_COMPAT` replaces the canonical-S and canonical-A checks with a simple `sig[63] & 224` test.

The checks follow `crypto_sign/ed25519/ref10/open.c` on the current master; behaviour can differ between libsodium versions and from other libraries, so test rather than assume.

## Why it matters
- Consensus systems need every node to agree on validity; different rules split the network. Use
  one library and version everywhere.
- Malleability: if S non-canonical forms were accepted, the same message could have multiple valid signatures;
  do not use signatures as unique IDs regardless.

## Practice
- Pin libsodium version in consensus or audit-critical code.
- Build your own edge-case vectors (non-canonical S, small-order A and R) to document behaviour.
- Always use the detached or `crypto_sign_open` return value; never parse a signature yourself.

## Verify
- [ ] Edge-case vectors produce the same accept/reject decisions as the other implementations in your system.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed against open.c: canonical-S test, canonical and small-order checks on A, small-order check on R, final small-order check on the difference, ED25519_COMPAT branch. The earlier cofactorless-equation claim was wrong. Removed unconfirmed references to Go, dalek, ZIP-215, Wycheproof and other vector sets.

Method: documentation only; no commands were run.
