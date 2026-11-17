---
id: computing-software.cryptography-implementation.applied-cryptography.key-commitment-and-partitioning-oracles
name: key-commitment-and-partitioning-oracles
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, aead, key-commitment, committing-aead, invisible-salamanders, partitioning-oracle, aes-gcm, chacha20-poly1305]
level: advanced
status: draft
description: "Add key commitment where AES-GCM or ChaCha20-Poly1305 is not enough: invisible salamanders, partitioning oracles, and the HKDF commitment construction."
sources: ["https://eprint.iacr.org/2019/016", "https://eprint.iacr.org/2020/1491", "https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/concepts.html#key-commitment"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Key commitment and partitioning-oracle defence

GCM, ChaCha20-Poly1305 and XSalsa20-Poly1305 are not key-committing: an
attacker can build one ciphertext that decrypts validly under two (or many)
different keys to different plaintexts.

- **Invisible salamanders** (Dodis et al. 2018): an abusive attachment is
  reported under one key while the recipient sees another, defeating message
  franking in Facebook Messenger.
- **Partitioning oracles** (Len, Grubbs, Ristenpart 2021): a ciphertext valid
  under thousands of candidate keys lets an attacker test many password-
  derived keys per query (shown against Shadowsocks and early OPAQUE
  designs).

## When you need commitment

- Keys are derived from passwords or low-entropy secrets and the server
  reveals decrypt success or failure.
- Multiple recipients get different keys for the same ciphertext (group
  messaging, multi-recipient envelopes).
- Moderation or abuse reporting relies on "what was decrypted".
- Any envelope format where an attacker can choose which key gets used.

## Construction (derive and check a commitment)

```python
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, hmac
import hmac as std_hmac

def split(root: bytes, nonce: bytes):
    okm = HKDF(hashes.SHA256(), 64, salt=nonce, info=b"app v1 enc+commit").derive(root)
    return okm[:32], okm[32:]        # enc_key, commitment (32 bytes)

# encrypt: store commitment in the header next to the nonce
# decrypt: recompute, compare in constant time BEFORE decrypting
enc_key, commit = split(root, nonce)
if not std_hmac.compare_digest(commit, header_commit):
    raise InvalidCiphertext()
```

A 256-bit commitment from a collision-resistant KDF gives 128-bit commitment
security. Alternatives: the "padding fix" (prepend and check an all-zero
block, Albertini et al.), CTX, or a library that does it for you, e.g. the
AWS Encryption SDK `REQUIRE_ENCRYPT_REQUIRE_DECRYPT` commitment policy.

## Pitfalls

- Checking the commitment after decryption, or with `==`, reintroduces the
  oracle or a timing leak.
- Version the format; old non-committing ciphertexts need a migration path.

## Verify

- [ ] Commitment is checked in constant time before any plaintext is used.
- [ ] Error responses do not distinguish commitment failure from tag failure.
- [ ] Password-derived-key paths are rate limited regardless.
