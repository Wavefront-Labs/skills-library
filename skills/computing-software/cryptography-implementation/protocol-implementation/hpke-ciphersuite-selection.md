---
id: computing-software.cryptography-implementation.protocol-implementation.hpke-ciphersuite-selection
name: hpke-ciphersuite-selection
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, hpke, hpke-ciphersuite, dhkem, x25519, p-256, ml-kem, x-wing, aes-128-gcm, chacha20-poly1305, rfc9180]
level: advanced
status: docs-checked
description: "Pick an HPKE KEM/KDF/AEAD suite from the RFC 9180 registries: DHKEM curve choice, HKDF hash, AEAD choice, and the export-only AEAD id."
sources: ["https://www.rfc-editor.org/rfc/rfc9180#section-7"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HPKE ciphersuite selection

An HPKE suite is (KEM id, KDF id, AEAD id) from the HPKE registries (RFC 9180 section 7; the IANA registry is the live list). Both
sides must use the same triple; protocols usually fix one or negotiate from
a short list.

## KEM

| KEM | id | Notes |
|---|---|---|
| DHKEM(X25519, HKDF-SHA256) | 0x0020 | 32-byte enc and public key |
| DHKEM(P-256, HKDF-SHA256) | 0x0010 | 65-byte enc and public key |
| DHKEM(P-384, HKDF-SHA384) | 0x0011 | 97-byte enc |
| DHKEM(P-521, HKDF-SHA512) | 0x0012 | 133-byte enc |
| DHKEM(X448, HKDF-SHA512) | 0x0021 | 56-byte enc |

Post-quantum and hybrid KEMs are defined outside RFC 9180; check the live
registry for their ids rather than assuming them.

## KDF

HKDF-SHA256 (0x0001), HKDF-SHA384 (0x0002), HKDF-SHA512 (0x0003). Match the KDF
to the KEM's hash (SHA256 for X25519 and P-256, SHA384 for P-384, SHA512 for
P-521 and X448).

## AEAD

| AEAD | id | Pick when |
|---|---|---|
| AES-128-GCM | 0x0001 | 16-byte key |
| AES-256-GCM | 0x0002 | 32-byte key |
| ChaCha20Poly1305 | 0x0003 | 32-byte key |
| Export-only | 0xFFFF | You only need `Export()` secrets, no Seal/Open |

All three AEADs use a 12-byte nonce and 16-byte tag.

## Rules

- Do not negotiate suites that the peer controls without an allowlist.
- Encode the suite triple in your message header or key config so you can
  migrate (crypto agility) without breaking old ciphertexts.
- In a regulated environment, check which curves your compliance regime allows before choosing.

## Verify

- [ ] Suite ids appear in the key config / header, not implied.
- [ ] Library supports the exact ids (check registry numbers, not names).
- [ ] RFC 9180 Appendix A vectors pass for the chosen triple.

## Checked

2026-11-01: RFC 9180 section 7 tables read. Confirmed: KEM ids, enc lengths, KDF ids, AEAD ids, key/nonce/tag sizes, export-only id. Removed: post-quantum and hybrid ids, ECH/MLS/OHTTP suite claims, FIPS, CNSA and hardware-selection advice.
Method: documentation only; no commands were run.
