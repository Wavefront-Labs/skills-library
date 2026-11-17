---
id: computing-software.cryptography-implementation.applied-cryptography.kem-combiners-for-hybrid-key-exchange
name: kem-combiners-for-hybrid-key-exchange
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, kem-combiner, hybrid-kem, ml-kem, x25519, x-wing, sp-800-227, sp-800-56c, post-quantum, key-derivation]
level: advanced
status: docs-checked
description: "Combine classical and ML-KEM shared secrets safely: TLS concatenation, X-Wing, SP 800-227 combiner rules, what to hash into the combiner and why."
sources: ["https://csrc.nist.gov/pubs/sp/800/227/final", "https://datatracker.ietf.org/doc/draft-connolly-cfrg-xwing-kem/", "https://datatracker.ietf.org/doc/draft-ietf-tls-ecdhe-mlkem/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KEM combiners for hybrid key exchange

A hybrid combines a classical secret (X25519/ECDH) with a post-quantum one (ML-KEM) so the result is secure if
either component holds. The combiner is where hybrids go wrong.

## Patterns in use
- **TLS 1.3 hybrids (X25519MLKEM768):** the shared secret is the concatenation of the ML-KEM secret then the X25519
  secret (64 bytes), fed into the TLS 1.3 key schedule. The draft says its security analysis relies on the TLS 1.3
  message transcript. The ECDHE-first order is used for SecP256r1MLKEM768 and SecP384r1MLKEM1024.
- **X-Wing (ML-KEM-768 + X25519):**
  `ss = SHA3-256(ss_M || ss_X || ct_X || pk_X || XWingLabel)` with a fixed 6-byte ASCII label. It includes the X25519
  ciphertext and public key but not the ML-KEM ones.
- **SP 800-227 section 4.6.2:** a key combiner takes at least two shared secrets and may also take ciphertexts,
  encapsulation keys, parameter sets or other context; it can be built from an SP 800-56C key-derivation method
  or an SP 800-133 combination method.

## Rules for a custom combiner
1. Use a KDF or an approved combiner over all component secrets.
2. Consider including ciphertexts, ephemeral public keys and the recipient's public key unless the protocol transcript
   already binds them (X-Wing includes the X25519 ones).
3. Add a domain-separation label naming the exact combination.
4. Fixed-length encodings for every input so concatenation is unambiguous (SP 800-227 warns that variable-length
   concatenation can give colliding inputs).
5. For FIPS validation, check the module's security policy for hybrid support.

## Gotchas
- Reordering components between peers silently produces different keys; specify order in the protocol.
- Don't invent a combiner if X-Wing or a standard TLS/HPKE hybrid suite fits.

## Verify
- [ ] Known-answer vectors from the X-Wing draft or TLS hybrid draft pass.
- [ ] Changing either component's ciphertext changes the derived key.

## Checked
2026-11-01. Confirmed in the IETF TLS ECDHE-MLKEM draft (shared-secret concatenation order and 64-byte size,
transcript reliance, ECDHE-first order for the P-256/P-384 groups), the X-Wing draft (SHA3-256 combiner inputs and
6-byte label) and the SP 800-227 PDF (section 4.6.2 combiners and concatenation warning). Removed: the claim that
non-binding ciphertexts outside the hash allow re-encapsulation, the FixedInfo-must-include-ciphertexts requirement and
the approved-component-first rule for generic FIPS use (not confirmed).
Method: documentation only; no commands were run.
