---
id: computing-software.cryptography-implementation.applied-cryptography.chacha20-nonce-and-block-counter-layout
name: chacha20-nonce-and-block-counter-layout
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, chacha20-counter, chacha20, rfc-8439, stream-cipher, nonce, block-counter]
level: advanced
status: verified
description: "Lay out the ChaCha20 state correctly per RFC 8439 2.3-2.4: 96-bit nonce with 32-bit counter versus original 64/64 split, initial counter values and the 256 GiB limit."
sources: ["https://www.rfc-editor.org/rfc/rfc8439", "https://doc.libsodium.org/advanced/stream_ciphers/chacha20"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ChaCha20 nonce and block counter layout

## State (RFC 8439 2.3)
16 little-endian 32-bit words: 4 constants (`expand 32-byte k`), 8 key words, then:
- IETF variant: word 12 = 32-bit block counter, words 13-15 = 96-bit nonce.
- Original (DJB) variant: words 12-13 = 64-bit counter, words 14-15 = 64-bit nonce.

The two are not interchangeable. libsodium exposes both (`crypto_stream_chacha20` 64-bit nonce,
`crypto_stream_chacha20_ietf` 96-bit nonce; counters are uint64 and uint32); Go `chacha20.NewUnauthenticatedCipher` accepts only
12-byte (IETF) and 24-byte (XChaCha20) nonces and rejects 8 (run), so it cannot read original-variant data.

## Counter rules
- Each block is 64 bytes; the 32-bit IETF counter caps one nonce at 2^32 x 64 bytes = 256 GiB. Libraries
  error or wrap; wrapping repeats keystream. Go x/crypto panics with `chacha20: counter overflow` (run).
- ChaCha20-Poly1305 (RFC 8439 2.8) uses counter 0 to derive the Poly1305 one-time key and starts encryption at
  counter 1. Standalone ChaCha20 test vectors in 2.4.2 start at counter 1 too.
- Seeking: to start at byte offset `o`, set counter to `o / 64` and discard `o % 64` bytes of the first block.

## Nonce rules
- Never reuse (key, nonce). With a 96-bit nonce, random nonces are fine for about 2^32 messages per key; use a
  counter nonce or XChaCha20 (192-bit nonce) for more.
- Raw ChaCha20 has no integrity; use the AEAD unless a higher layer authenticates.

## Verify
- [ ] Reproduce RFC 8439 2.4.2 vector (pyca `ChaCha20` takes a 16-byte nonce = 4-byte little-endian counter + 12-byte nonce; reproduced here) (key 00..1f, nonce `000000000000004a00000000`, counter 1).
- [ ] Interop test with the peer library confirms variant (IETF vs original) and initial counter.
