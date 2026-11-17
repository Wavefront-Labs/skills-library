---
id: computing-software.cryptography-implementation.applied-cryptography.eliminating-textbook-rsa
name: eliminating-textbook-rsa
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, textbook-rsa, rsa, rsa-nopadding, raw-rsa, rsa-oaep, rsa-pss, rsa-kem, malleability, cwe-780]
level: practitioner
status: docs-checked
description: "Find and remove raw RSA (RSA_NO_PADDING, pow(m,e,n)) from code: why it is malleable and deterministic, and the OAEP or PSS replacement."
sources: ["https://www.rfc-editor.org/rfc/rfc8017", "https://cwe.mitre.org/data/definitions/780.html", "https://csrc.nist.gov/pubs/sp/800/56/b/r2/final", "https://docs.openssl.org/3.0/man1/openssl-pkeyutl/", "https://www.rfc-editor.org/rfc/rfc9474"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Eliminating textbook RSA

Textbook RSA is `c = m^e mod n` with no padding. It is:
- **Deterministic:** equal plaintexts give equal ciphertexts; small message spaces (yes/no, PINs) are guessed by
  encrypting candidates with the public key.
- **Malleable:** `c * r^e` decrypts to `m * r`; signatures multiply the same way, enabling forgeries.
- **Broken for small m and small e:** with e = 3 and m^3 < n, the cube root of c is m.

## Where it hides
```
rg -n 'RSA_NO_PADDING|rsa_padding_mode:none|pow\([^,]+,\s*e\s*,\s*n\)|PKCS1_v1_5\b'
```
- OpenSSL: `RSA_public_encrypt(..., RSA_NO_PADDING)`, `EVP_PKEY_CTX_set_rsa_padding(ctx, RSA_NO_PADDING)`,
  `openssl pkeyutl -pkeyopt rsa_padding_mode:none`.
- Python: hand-written `pow(m, e, n)`.
- "Signing" by encrypting a hash with the private key without PKCS#1 or PSS encoding.

## Replacements
| Purpose | Use |
|---|---|
| Encrypt a small secret to an RSA key | RSA-OAEP with SHA-256 and MGF1-SHA-256 |
| Transport a key | A key-establishment scheme from SP 800-56B then a KDF, or move to ECDH |
| Sign | RSA-PSS (or PKCS#1 v1.5 signatures where interop requires; they are not broken) |
| Encrypt data | Hybrid: wrap a random AES-GCM key, never RSA over bulk data |

## Legitimate raw RSA uses
Only as a building block inside a vetted construction (RSA-KEM encapsulation of a random full-size integer, blind
signatures per RFC 9474). Keep these inside a reviewed library, not application code.

## Verify
- [ ] Search returns no NoPadding / RSA_NO_PADDING outside reviewed library code.
- [ ] Encrypting the same message twice with the replacement produces different ciphertexts.
- [ ] Signature verification rejects a signature multiplied by r^e.

## Checked
2026-11-01. Confirmed: CWE-780 "Use of RSA Algorithm without OAEP"; RFC 8017 (OAEP, deterministic RSAEP, no known
attacks on RSASSA-PKCS1-v1_5 stated); RFC 9474 (RSA blind signatures); OpenSSL `EVP_PKEY_CTX_ctrl` (RSA_NO_PADDING)
and `openssl-pkeyutl` (`rsa_padding_mode`, `none`, `oaep`) pages. Removed: Java NoPadding transformation strings,
PyCryptodome internals, RSASVE/HPKE naming (not confirmed in fetched sources). Algebraic points (malleability, small
exponent cube root) are standard arithmetic, not source claims.
Method: documentation only; no commands were run.
