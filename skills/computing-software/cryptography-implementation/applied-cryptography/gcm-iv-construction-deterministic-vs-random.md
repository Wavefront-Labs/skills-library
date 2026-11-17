---
id: computing-software.cryptography-implementation.applied-cryptography.gcm-iv-construction-deterministic-vs-random
name: gcm-iv-construction-deterministic-vs-random
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, gcm-nonce-construction, aes-gcm, gcm-iv, sp-800-38d, nonce, deterministic-iv, random-iv, invocation-counter]
level: advanced
status: docs-checked
description: "Choose and implement AES-GCM IVs: deterministic fixed-field plus counter construction (RFC 5116, RFC 8446) versus random IVs, and why the exact limits come from SP 800-38D."
sources: ["https://www.rfc-editor.org/rfc/rfc5116", "https://www.rfc-editor.org/rfc/rfc8446", "https://csrc.nist.gov/pubs/sp/800/38/d/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GCM IV construction: deterministic versus random

The IV (nonce) must be distinct for every encryption under one key (RFC 5116 3.1). The two construction families
differ only in how you guarantee that. For the exact invocation limits of each, read SP 800-38D section 8 itself
(the NIST page is an abstract only and the PDF was not readable in this review, so no limits are quoted here).

## Deterministic construction
RFC 5116 3.2 recommends a nonce of a Fixed field followed by a Counter field, with lengths constant for a key.
```
96-bit nonce = Fixed (identifies the device) || Counter
```
- RFC 5116 asks implementations to support 12-octet nonces with a 4-octet counter; a wider counter and shorter
  fixed field is another valid split. At most 2^(8*C) nonces fit in a C-octet counter and 2^(8*F) devices in an
  F-octet fixed field.
- The counter should start at zero and increase monotonically; skipped values are allowed.
- Different devices sharing a key must use distinct Fixed fields.
- Across reboots the counter must be checkpointed in non-volatile storage; store a value several steps ahead
  (RFC 5116 3.1 example: store 100, use 1 to 99, store 200 meanwhile) so a crash never repeats a nonce.
- TLS 1.3 per-record nonce = static IV XOR the 64-bit record sequence number padded to the left with zeros to the
  IV length (RFC 8446 5.3); the sequence number resets only when the key changes.

## Random construction
IV = random bytes from an approved random generator. There is no state to persist, so it suits distributed
writers, but the number of invocations per key must stay far below the birthday bound for the nonce size. Take the
exact ceiling from SP 800-38D and rotate the key by invocation count before it.

## Choosing
| Situation | Use |
|---|---|
| Single writer with durable storage or a protocol sequence number | Deterministic |
| Many writers, stateless services | Random, plus key rotation by count, or per-object keys |
| Many writers and you cannot count | An algorithm built for it; RFC 5116 says an application that cannot guarantee unique nonces must use a randomized or stateful algorithm |

## Gotchas
- RFC 5116 says applications should use 12-octet nonces for interoperability; keep GCM IVs at exactly 12 bytes.
- A timestamp is not a counter (clock jumps, two messages in one tick).
- Many problems with nonce reuse can be avoided by changing keys when coordination is difficult (RFC 5116 3.1).

## Verify
- [ ] Restart test: counter continues above the last persisted value.
- [ ] Random-IV deployments count invocations per key and rotate before the SP 800-38D limit.
- [ ] IV length is exactly 12 bytes everywhere.

## Checked
Date: 2026-10-31. Confirmed in RFC 5116 3, 3.1 and 3.2 (nonce uniqueness, 12-octet recommendation, Fixed and Counter
format, distinct Fixed fields, checkpointing example, key change advice) and RFC 8446 5.3 (TLS nonce). Removed
because SP 800-38D could not be read (abstract page only, PDF unreadable): the 2^32 random-IV limit, the 2^64
deterministic limit, the 8.2.1 and 8.2.2 section attributions, the FIPS 140-3 IG C.H and OpenSSL FIPS statements,
and the AES-GCM-SIV and XChaCha20 alternatives.
Method: documentation only; no commands were run.
