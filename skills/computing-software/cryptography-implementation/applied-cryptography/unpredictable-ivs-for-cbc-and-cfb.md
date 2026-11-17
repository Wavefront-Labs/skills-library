---
id: computing-software.cryptography-implementation.applied-cryptography.unpredictable-ivs-for-cbc-and-cfb
name: unpredictable-ivs-for-cbc-and-cfb
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, iv-unpredictability, cbc, cfb, initialization-vector, sp-800-38a, beast]
level: practitioner
status: docs-checked
description: "Generate unpredictable IVs for CBC and CFB per SP 800-38A Appendix C: random IVs or encrypted nonces, never counters, timestamps or the previous ciphertext block."
sources: ["https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unpredictable IVs for CBC and CFB

CBC and CFB need IVs that an attacker cannot predict before the plaintext is chosen. SP 800-38A: for any given
plaintext it must not be possible to predict the IV that will be associated with it in advance of generating the IV.
Uniqueness alone is not enough.

## Approved ways (SP 800-38A Appendix C)
1. Apply the forward cipher function, under the same key used for encrypting the plaintext, to a nonce: a data
   block unique to each execution of the encryption operation (for example a counter or message number).
   `IV = AES_K(nonce)`. The nonce must never repeat under that key.
2. Generate a random data block with a FIPS-approved random number generator, one per message.
   ```python
   iv = os.urandom(16)                 # per message, stored in front of the ciphertext
   ```
The IV need not be secret and may be transmitted with the ciphertext.

## Never use as the IV
- A counter, sequence number, timestamp or message number directly (it must go through the forward cipher first).
- The last ciphertext block of the previous message (chained IVs): the attacker sees it before choosing the next
  plaintext.
- A constant or all-zero IV.

## OFB and CTR differ
OFB needs the IV to be a nonce unique to each execution, not unpredictable; reuse can compromise confidentiality of
the messages. CTR needs unique counter blocks across all messages under a key.

## Review checklist
- [ ] Search the code for static IV constants and zero-filled IV buffers.
- [ ] IV generated per message inside the encrypt function, not per process or per key.
- [ ] Prefer replacing CBC/CFB with an AEAD when the format can change.

## Checked
2026-11-01. Confirmed in SP 800-38A section 6 and Appendix C (unpredictable IV for CBC and CFB; the two methods;
IV need not be secret; OFB needs a unique nonce, not an unpredictable IV; CTR counter uniqueness). Removed: the
TLS 1.0/BEAST description, the named OpenSSL, Java and grep patterns, and the hash-of-plaintext claim, none of
which the cited standard states.
Method: documentation only; no commands were run.
