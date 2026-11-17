---
id: computing-software.cryptography-implementation.libsodium.secretbox-easy-and-detached
name: secretbox-easy-and-detached
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, secretbox, crypto-secretbox, secretbox-detached, crypto-secretbox-easy, xsalsa20-poly1305, nonce, nacl-compat]
level: practitioner
status: docs-checked
description: "Use crypto_secretbox_easy and crypto_secretbox_detached: XSalsa20-Poly1305 sizes, random nonces, output layout (MAC first), in-place use, and when to prefer the AEAD API."
sources: ["https://doc.libsodium.org/secret-key_cryptography/secretbox", "https://nacl.cr.yp.to/secretbox.html", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/include/sodium/crypto_secretbox_xsalsa20poly1305.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_secretbox: easy and detached

`crypto_secretbox` is NaCl's secret-key authenticated encryption:
XSalsa20 stream cipher + Poly1305 MAC, 32-byte key, 24-byte nonce, 16-byte
MAC. It has no additional-data input; use the AEAD API if you need one.

## Easy (combined) mode

```c
unsigned char key[crypto_secretbox_KEYBYTES], nonce[crypto_secretbox_NONCEBYTES];
crypto_secretbox_keygen(key);
randombytes_buf(nonce, sizeof nonce);
unsigned char c[crypto_secretbox_MACBYTES + mlen];
crypto_secretbox_easy(c, m, mlen, nonce, key);          /* c = MAC(16) || ciphertext */
unsigned char out[mlen];
if (crypto_secretbox_open_easy(out, c, sizeof c, nonce, key) != 0) { /* forged */ }
```

Note the layout: libsodium's easy format puts the **MAC before** the
ciphertext (the docs: the tag is written to `c`, immediately followed by the encrypted message; unlike the AEAD API, which appends the tag).
Hand-rolled interop code can get this wrong. Store the nonce followed by `c`.

## Detached mode

```c
unsigned char mac[crypto_secretbox_MACBYTES];
crypto_secretbox_detached(c, mac, m, mlen, nonce, key);    /* c is mlen bytes */
if (crypto_secretbox_open_detached(m, c, mac, mlen, nonce, key) != 0) { /* forged */ }
```

Use when the MAC travels in a separate field. Both `_easy` and `_detached` forms allow `c` and `m` to overlap, so in-place operation is possible (the easy form needs `crypto_secretbox_MACBYTES` extra bytes to prepend the tag).

## Rules

- The docs say the easiest way to make a nonce is `randombytes_buf()`; it must never be reused with the same key.
- `crypto_secretbox_open_easy` returns -1 if verification fails and 0 on success; use the output only on success.
- Messages are assumed independent: with random nonces there is no way to detect a replayed or reordered message (secretbox docs).
- The original NaCl API (`crypto_secretbox`, which needs 32 bytes of zero padding before the message) is supported but not recommended; the `_easy` and `_detached` APIs are faster and need no padding or pointer arithmetic.
- Choose `crypto_aead_xchacha20poly1305_ietf_*` instead when you need
  associated data, or for IETF-standard constructions; choose
  `crypto_secretstream_*` for streams.

## Verify

- [ ] Ciphertext length = message length + 16 (easy) and nonce stored alongside.
- [ ] Tampering any byte of nonce, MAC or ciphertext fails open.
- [ ] Interop peers agree on MAC-first layout.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: XSalsa20 plus Poly1305 (docs), 32-byte key, 24-byte nonce and 16-byte MAC (header), MAC written before the ciphertext in easy mode, detached layout, overlapping buffers allowed, return values, original NaCl API note, randombytes_buf nonces. Removed the unconfirmed claim that overlap is only allowed at the same address and a statement about unspecified output.

Method: documentation only; no commands were run.
