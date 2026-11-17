---
id: computing-software.cryptography-implementation.applied-cryptography.aead-usage-limits-per-key
name: aead-usage-limits-per-key
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, aead-usage-limits, aead, aes-gcm, chacha20-poly1305, aes-ccm, quic, tls-1-3, key-update, integrity-limit, confidentiality-limit]
level: advanced
status: docs-checked
description: "Apply confidentiality and integrity limits for AES-GCM, ChaCha20-Poly1305 and AES-CCM per the CFRG aead-limits analysis and TLS/QUIC rekey rules."
sources: ["https://datatracker.ietf.org/doc/draft-irtf-cfrg-aead-limits/", "https://www.rfc-editor.org/rfc/rfc9001#section-6.6", "https://www.rfc-editor.org/rfc/rfc8446#section-5.5"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AEAD usage limits per key

**Goal:** know both limits every AEAD key has, the confidentiality limit (how many messages you may encrypt) and the
integrity limit (how many forged messages you may try to decrypt), and wire them into rekeying.

## Published limits (QUIC, RFC 9001 section 6.6, derived from the CFRG analysis)
| AEAD | Confidentiality limit (packets encrypted) | Integrity limit (failed decryptions) |
|---|---|---|
| AEAD_AES_128_GCM / 256_GCM | 2^23 packets (for full-size TLS 1.3 records, RFC 8446 section 5.5 gives 2^24.5) | 2^52 |
| AEAD_CHACHA20_POLY1305 | greater than the number of possible packets (2^62), so disregarded | 2^36 |
| AEAD_AES_128_CCM | 2^21.5 | 2^21.5 |

RFC 9001 appendix B derives these for a 2^-57 attacker advantage target, with packets up to 2^16 bytes for the GCM
confidentiality figure. Endpoints that limit packet size may use higher limits; the CFRG draft gives the formulas so you
can compute limits for your own message size and target.

## Implementation
- Track `encrypted_count` per key and `failed_decrypt_count` per connection (QUIC counts failures across all keys).
- When `encrypted_count` nears the confidentiality limit, rekey (TLS 1.3 KeyUpdate, QUIC key phase change, or a new
  data key from your KMS).
- When `failed_decrypt_count` exceeds the integrity limit, tear down the connection or session; QUIC requires closing
  it with error AEAD_LIMIT_REACHED. TLS closes the connection on the first record that fails authentication.

## Gotchas
- ChaCha20-Poly1305's integrity limit (2^36) is lower than GCM's (2^52); endpoints that keep processing forgeries
  forever are the risk, not the encrypting side.
- Failed decryptions must be counted even when you drop the packet silently.
- Message-size assumptions: the published limits assume a maximum packet size, so a protocol that permits much larger
  messages must recompute them from the CFRG formulas.

## Verify
- [ ] Counters for both limits are exported as metrics per key.
- [ ] A fuzz test that sends random forgeries triggers the integrity-limit teardown.
- [ ] Rekey is exercised in tests, not only in production.

## Checked

2026-10-31. Confirmed in RFC 9001 section 6.6 and appendix B: GCM confidentiality 2^23 and integrity 2^52,
ChaCha20-Poly1305 confidentiality above 2^62 and integrity 2^36, AES-128-CCM 2^21.5 for both, the 2^-57 target,
AEAD_LIMIT_REACHED, and that QUIC counts failures across all keys of a connection. Confirmed in RFC 8446 section 5.5:
2^24.5 full-size records for AES-GCM. The CFRG draft is cited for its formulas. Removed: the advice on 256-bit keys for
multi-user security and the 16 MiB / 16 KiB figures (unconfirmed), and the per-key wording of the integrity count.
Method: documentation only; no commands were run.
