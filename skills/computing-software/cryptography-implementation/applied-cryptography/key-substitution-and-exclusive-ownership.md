---
id: computing-software.cryptography-implementation.applied-cryptography.key-substitution-and-exclusive-ownership
name: key-substitution-and-exclusive-ownership
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, key-substitution-attack, exclusive-ownership, dsks, signature-binding, ed25519, ecdsa]
level: sme
status: draft
description: "Defend against key-substitution and exclusive-ownership attacks on signatures (DSKS, malicious keys): bind the public key into signed data and use strict verification."
sources: ["https://eprint.iacr.org/2020/1525", "https://www.rfc-editor.org/rfc/rfc8032", "https://eprint.iacr.org/2019/779"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Key-substitution and exclusive-ownership

## The attacks
- **Destructive exclusive ownership (DEO) / key substitution (DSKS)**: given a signature `s` on `m` under key
  `pk`, an attacker crafts `pk'` such that `s` also verifies on `m` (or a different `m'`) under `pk'`. Classic
  ECDSA and RSA allow it (e.g. choosing a curve generator or modulus).
- **Malicious key**: weak or small-order public keys (Ed25519 low-order points) make many signatures verify.
- Real impact: Let's Encrypt ACME duplicate signature key selection (2015) let an attacker claim domains by
  producing a key that validated an existing signature.

## Defences
- Bind the signer's public key (or its hash) into the signed message. Ed25519 already hashes `A` into
  `H(R || A || M)`; ECDSA and RSA do not, so prepend it at the application layer.
- Use strict verification: reject small-order keys and non-canonical encodings (Ed25519 per ZIP-215 or RFC 8032
  strict rules applied consistently).
- Do not identify signers by "whichever key verifies"; look keys up by identity first, then verify.
- Use key IDs bound to identity in a PKI or transparency log.

## Verify
- [ ] Protocol message signed includes signer identity and key fingerprint.
- [ ] Verifier rejects low-order and non-canonical Ed25519 keys (Wycheproof `eddsa` tests).
