---
id: computing-software.cryptography-implementation.applied-cryptography.choosing-elliptic-curves
name: choosing-elliptic-curves
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, curve-selection, elliptic-curves, p-256, p-384, x25519, ed25519, x448, secp256k1, brainpool, fips-186-5]
level: practitioner
status: draft
description: "Choose between P-256, P-384, P-521, X25519/Ed25519, X448, secp256k1 and Brainpool by compliance, interop, implementation safety and performance."
sources: ["https://csrc.nist.gov/pubs/sp/800/186/final", "https://www.rfc-editor.org/rfc/rfc7748", "https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Technische-Richtlinien/TR-nach-Thema-sortiert/tr02102/tr02102_node.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing elliptic curves

## Quick table
| Curve | Strength | Best for | Notes |
|---|---|---|---|
| X25519 | ~128 | Key agreement in new protocols | Any 32-byte string is a valid public key; constant-time ladders are standard; check the all-zero output. Approved in SP 800-186. |
| Ed25519 | ~128 | Signatures in new systems | Deterministic, fast; FIPS 186-5 approved. Not accepted for WebPKI server certificates. |
| P-256 | 128 | WebPKI certificates, FIPS, hardware (TPM, Secure Enclave, smart cards, HSMs) | Requires public key validation for ECDH; use deterministic or hedged ECDSA. |
| P-384 | 192 | CNSA 1.0, government | Slower; default for some government profiles. |
| P-521 | 256 | Rarely needed | Uncommon in hardware; poor interop in some stacks. |
| X448 / Ed448 | ~224 | Higher margin with Curve448 benefits | Less library and hardware support. |
| secp256k1 | 128 | Bitcoin/Ethereum ecosystems only | Not NIST-approved; avoid elsewhere. |
| brainpoolP256r1/384r1 | 128/192 | German/EU government, some smart cards (BSI TR-02102) | Slower; removed from TLS 1.3 default lists. |

## Decision rules
1. Hardware or compliance dictates the curve? Use that (usually P-256 or P-384).
2. Public WebPKI certificate? P-256 ECDSA (or RSA). Ed25519 certs are not accepted by browsers.
3. Greenfield protocol where you control both ends? X25519 for key agreement, Ed25519 for signatures.
4. Post-quantum planning? Pair the classical curve with ML-KEM (hybrid), do not upgrade to bigger curves for
   quantum reasons.

## Gotchas
- Do not convert one key between Ed25519 and X25519 for two purposes unless the protocol specifies it
  (libsodium conversion is for specific designs).
- ECDSA on P-256 with SHA-512 truncates the hash; it is fine but must match on both ends.
- Brainpool curves have no efficient constant-time implementations in some libraries.

## Verify
- [ ] Each protocol has one documented curve choice and the reason.
- [ ] Interop matrix tested with the actual peers (HSM, mobile, browsers).
