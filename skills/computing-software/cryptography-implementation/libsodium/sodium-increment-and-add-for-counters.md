---
id: computing-software.cryptography-implementation.libsodium.sodium-increment-and-add-for-counters
name: sodium-increment-and-add-for-counters
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, sodium-increment, sodium-add, sodium-compare, libsodium, nonce-counter, replay-window, constant-time]
level: practitioner
status: docs-checked
description: "Use sodium_increment, sodium_add, sodium_sub, sodium_compare and sodium_is_zero for constant-time little-endian nonce counters and replay windows."
sources: ["https://doc.libsodium.org/helpers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sodium_increment and friends for counters

All of these treat buffers as **little-endian** unsigned integers and run in constant time for a given length.

| Function | Purpose |
|---|---|
| `sodium_increment(n, len)` | n += 1 (the docs describe it as constant time and suited to nonces; the number wraps) |
| `sodium_add(a, b, len)` | a = (a + b) mod 2^(8 len) |
| `sodium_sub(a, b, len)` | a = (a - b) mod 2^(8 len) (since libsodium 1.0.17) |
| `sodium_compare(a, b, len)` | -1, 0, 1 like memcmp but numeric little-endian and constant time |
| `sodium_is_zero(n, len)` | 1 if all bytes are zero, else 0 (since 1.0.16) |

## Nonce counter
```c
unsigned char nonce[crypto_aead_chacha20poly1305_ietf_NPUBBYTES];
sodium_memzero(nonce, sizeof nonce);
nonce[sizeof nonce - 1] = sender_id;        /* top byte partitions senders */
for (each message) {
    encrypt(..., nonce, key);
    sodium_increment(nonce, sizeof nonce - 1);    /* increment only the lower bytes */
    if (sodium_is_zero(nonce, sizeof nonce - 1)) abort();   /* wrapped: rekey */
}
```

## Replay window on the receiver
Keep the highest accepted nonce; reject anything `sodium_compare(received, highest, len) <= 0` for strictly ordered
transports, or keep a bitmap for a sliding window on reordering transports. The docs say `sodium_compare` can be used with nonces to prevent replay attacks.

## Gotchas
- Big-endian counters from other protocols do not match: incrementing with `sodium_increment` changes the first
  byte, not the last. Convert or implement big-endian increment yourself.
- Wrap-around is silent; check for it or bound the message count.
- Do not use these for secret-dependent lengths; constant time holds per length.

## Verify
- [ ] Unit test: increment from 0xFF..FF wraps to zero and is detected.
- [ ] Receiver rejects a replayed nonce.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed in the helpers page: little-endian handling and constant time for a given length for increment, add, sub and compare and is_zero, the (a + b) mod 2^(8*len) and (a - b) mod 2^(8*len) definitions, sodium_sub since 1.0.17, sodium_is_zero since 1.0.16, sodium_compare return values and use against replay. The page anchors in the old sources are replaced with the helpers page.

Method: documentation only; no commands were run.
