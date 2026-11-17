---
id: computing-software.cryptography-implementation.applied-cryptography.replacing-ad-hoc-ecies
name: replacing-ad-hoc-ecies
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, hybrid-encryption, ecies, hpke, sealed-box, legacy-migration, ephemeral-key, kdf, code-audit]
level: advanced
status: docs-checked
description: "Audit and replace hand-built ECIES (ephemeral ECDH + KDF + cipher) with HPKE or sealed boxes: the common flaws to look for and a migration path for stored data."
sources: ["https://www.secg.org/sec1-v2.pdf", "https://datatracker.ietf.org/doc/html/rfc9180", "https://doc.libsodium.org/public-key_cryptography/sealed_boxes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replacing ad-hoc ECIES

"ECIES" (described in SEC 1) is a family of schemes, not one algorithm:
ephemeral ECDH, a KDF, a cipher and a MAC, with options for each. HPKE
(RFC 9180) provides a subset of the functions of such schemes, specified
clearly enough to be implemented interoperably, so it is the replacement; libsodium
`crypto_box_seal` is a simpler one for the libsodium ecosystem.

## Audit checklist for existing ECIES code

| Flaw | Why it matters |
|---|---|
| Raw shared x-coordinate used as AES key | No KDF; non-uniform key, no context binding |
| KDF input omits the ephemeral public key | Weakens binding of the derived key to this message |
| AES-CBC without MAC, or MAC-then-encrypt | Padding oracles |
| AES-CTR/GCM with a fixed IV and per-message ephemeral key | Safe only if the ephemeral key is truly fresh every time; dangerous if cached |
| Reused "ephemeral" key for performance | Same key and IV twice: catastrophic for GCM/CTR |
| No point validation of the ephemeral key on decrypt (NIST curves) | Invalid-curve attacks on recipient key; RFC 9180 requires validating the ephemeral public key |
| Non-constant-time MAC compare | Forgery via timing |
| Ambiguous serialization (no lengths, compressed vs uncompressed mix) | Parsing bugs, interop failures |

## Migration

1. Choose: HPKE base mode with DHKEM(X25519)/HKDF-SHA256/AES-128-GCM (or P-256
   for FIPS), or `crypto_box_seal` if already on libsodium.
2. Add a version byte to the ciphertext format. Old format: no byte or 0x00;
   new: 0x01 + suite id.
3. Recipients can keep their existing EC key pairs if the curve matches the new
   KEM (P-256 key pair -> DHKEM(P-256)); X25519 keys work with DHKEM(X25519).
4. Decrypt old format with the legacy code path (read-only), encrypt only with
   HPKE. Re-encrypt stored data in batch if the legacy scheme had a real flaw.
5. Delete legacy decrypt once inventory is zero.

## Verify

- [ ] Audit table filled for the legacy implementation; flaws documented.
- [ ] New writes are HPKE/sealed-box with a version byte.
- [ ] Legacy decrypt path has tests from captured real ciphertexts.
- [ ] HPKE RFC 9180 vectors pass.

## Checked

- 2026-11-01. Confirmed: RFC 9180 purpose (interoperable subset of earlier schemes), DHKEM(P-256, HKDF-SHA256) id 0x0010 and DHKEM(X25519, HKDF-SHA256) id 0x0020, AES-128-GCM id 0x0001, mandatory public key validation and test vectors (Appendix A); libsodium documents `crypto_box_seal` and `crypto_box_seal_open`.
- Removed as unconfirmed: SEC 1 section number and its KDF-input recommendation, claim that no two ECIES implementations interoperate.
- The audit table rows are review heuristics, not cited figures.

Method: documentation only; no commands were run.
