---
id: computing-software.cryptography-implementation.libsodium.sodium-pad-iso7816-padding
name: sodium-pad-iso7816-padding
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, sodium-helpers, sodium-pad, sodium-unpad, iso-7816-4, length-hiding, bucket-padding, traffic-analysis]
level: practitioner
status: docs-checked
description: "Hide message lengths with sodium_pad/sodium_unpad (ISO/IEC 7816-4 padding) before encryption: block size choice, buffer sizing, unpad error handling."
sources: ["https://doc.libsodium.org/helpers/padding", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/sodium/utils.c", "https://github.com/pyca/pynacl/blob/main/src/nacl/bindings/__init__.py", "https://github.com/jedisct1/libsodium.js"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sodium_pad: ISO/IEC 7816-4 padding

Most modern constructions disclose message lengths (the ciphertext is the same length or a constant number of bytes longer); the docs introduce this API in libsodium 1.0.14 for cases such as interactive remote shells. `sodium_pad` pads a buffer up to a multiple of a
block size using ISO/IEC 7816-4 (one 0x80 byte, then zeros) so that messages
in the same bucket have the same ciphertext length. Pad before encrypting,
unpad after decrypting.

```c
#define BLOCK 256
unsigned char buf[MAX_MSG + BLOCK];      /* room for padding */
memcpy(buf, msg, msglen);
size_t padded_len;
if (sodium_pad(&padded_len, buf, msglen, BLOCK, sizeof buf) != 0) { /* buffer too small */ }
/* encrypt buf[0..padded_len) */

/* after decrypt into buf, length dec_len: */
size_t unpadded_len;
if (sodium_unpad(&unpadded_len, buf, dec_len, BLOCK) != 0) { /* malformed */ }
```

## Notes

- Always adds at least one byte (the source computes the padded length as the next multiple strictly above the message length): a message that is already a multiple of
  the block size grows by a full block. Size the buffer as `msglen + block`.
- The docs say `sodium_pad` and `sodium_unpad` try to minimise side channels for a given `length & <block size mask>` value, and that applications may still leak the unpadded length through other side channels.
- Unpad only data that already passed AEAD verification; then a padding
  error means a bug (or a sender bug), not an attack signal. Return the same
  generic failure anyway.
- Block size is the leak granularity: a 256-byte block hides lengths within 256-byte
  buckets, and fixed blocks still reveal roughly how large a message is. `sodium_pad` returns -1 when the block size is 0 or when the padded length would exceed `max_buflen`.
- The docs advise against padding to hide the length of a password; hash it instead.
- PyNaCl exposes `sodium_pad` and `sodium_unpad` in `nacl.bindings`; libsodium.js has `sodium.pad(buf, blocksize)` and `sodium.unpad`.

## Verify

- [ ] Messages of length 0, block-1, block and block+1 round-trip.
- [ ] Ciphertexts of two different messages in the same bucket have equal length.
- [ ] Unpad happens after AEAD verification.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: sodium_pad and sodium_unpad signatures, ISO/IEC 7816-4 algorithm, -1 returns, introduced in 1.0.14, padding before encryption and removal after decryption, side-channel statement, password advice (docs); utils.c showing at least one padding byte; PyNaCl bindings exporting sodium_pad and sodium_unpad; libsodium.js pad and unpad. The earlier claim that PyNaCl lacks a wrapper was wrong. Removed unconfirmed block-size and Padme suggestions.

Method: documentation only; no commands were run.
