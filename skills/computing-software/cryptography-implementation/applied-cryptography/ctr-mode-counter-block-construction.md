---
id: computing-software.cryptography-implementation.applied-cryptography.ctr-mode-counter-block-construction
name: ctr-mode-counter-block-construction
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, block-cipher-modes, sp-800-38a, ctr-counter-block, counter-mode, aes-ctr, nonce, keystream-reuse, random-access-encryption]
level: advanced
status: verified
description: "Build AES-CTR counter blocks so no block is ever reused: nonce/counter split, overflow limits, library increment semantics, seeking, and adding a MAC."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/a/final", "https://datatracker.ietf.org/doc/html/rfc3686", "https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.modes.CTR"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CTR mode counter block construction

CTR turns AES into a stream cipher: keystream block i = AES(K, T_i), and
ciphertext = plaintext XOR keystream. Security needs every counter block T_i to
be unique across **all** messages under the key (SP 800-38A Appendix B, read). A
repeated block XORs two plaintexts together; there is no recovery.

## Pick a layout

16-byte counter block = nonce || counter. Common layouts:

| Layout | Nonce | Counter | Max per message | Notes |
|---|---|---|---|---|
| RFC 3686 (IPsec) | 4 B nonce + 8 B IV | 4 B, starts at 1 | 2^32 - 1 blocks (68,719,476,720 bytes per RFC 3686) | Counter is per packet |
| GCM-style | 12 B | 4 B | 2^32 blocks | Same limit as GCM |
| 8/8 split | 8 B random | 8 B | effectively unlimited | Random 64-bit nonce collides after ~2^32 messages |
| Full 128-bit random IV, increment whole block | 16 B | shared | | Library behaviour in pyca and OpenSSL (run); check other libraries |

The trap: OpenSSL (`openssl enc -aes-128-ctr`, run on 3.2.3) and pyca
`modes.CTR` (run) increment the **entire 128-bit block** as a big-endian
integer: with IV `...0bffffffff` the second keystream block is AES of `...0c00000000`,
not of the 32-bit-wrapped `...0b00000000`. Other libraries (Java etc.) not checked here. If you put a 12-byte nonce plus 4-byte zero counter and the message
exceeds 2^32 blocks, the carry spills into your nonce and can collide with
another message's range. Enforce the per-message length limit yourself.

## Rules

- Random 96-bit nonce with 32-bit counter: cap messages at 2^32 per key. Per message,
  a 32-bit counter starting at 0 allows 2^32 blocks; GCM starts its counter at 2,
  so its limit is 2^32 - 2 blocks.
- If you need random access (seek into a file), compute the block for offset
  `off` as `nonce || (off // 16)` and discard `off % 16` keystream bytes.
- Never let two writers share a key with independently chosen counters; give
  each a distinct nonce prefix or subkey.
- CTR is malleable: flipping ciphertext bit i flips plaintext bit i. Always add
  a MAC (encrypt-then-MAC) or use GCM, which is CTR plus GHASH.

## Seeking example (pyca)

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
def ctr_at(key, nonce12, offset):
    block = int.from_bytes(nonce12 + b"\0\0\0\0", "big") + offset // 16
    d = Cipher(algorithms.AES(key), modes.CTR(block.to_bytes(16, "big"))).decryptor()
    d.update(b"\0" * (offset % 16))   # skip into the block
    return d
```

The seeking example below was checked: reading 50 bytes at offsets 0, 5, 16, 37 and 200 matches the
continuous keystream.

## Verify

- [ ] Documented layout: nonce bytes, counter bytes, start value, endianness.
- [ ] Per-message length check rejects data that would overflow the counter field.
- [ ] Known-answer test against SP 800-38A F.5 vectors (CTR-AES128.Encrypt; first block with IV f0f1..feff
  gives 874d6191b620e3261bef6864990db6ce, matched in pyca).
- [ ] A MAC or AEAD protects every CTR ciphertext.
