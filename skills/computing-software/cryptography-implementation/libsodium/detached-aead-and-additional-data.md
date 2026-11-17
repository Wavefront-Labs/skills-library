---
id: computing-software.cryptography-implementation.libsodium.detached-aead-and-additional-data
name: detached-aead-and-additional-data
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-aead, aead-detached, encrypt-detached, additional-data, in-place-encryption, header-authentication, wire-format]
level: advanced
status: gated
description: "Use libsodium's detached AEAD variants to keep tags separate or encrypt in place, and authenticate headers via additional data without encrypting them."
sources: ["https://doc.libsodium.org/secret-key_cryptography/aead/chacha20-poly1305/xchacha20-poly1305_construction#detached-mode", "https://doc.libsodium.org/secret-key_cryptography/aead", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_aead/chacha20poly1305/aead_chacha20poly1305.c"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detached AEAD and additional data

Every libsodium AEAD has a combined form (`_encrypt`: ciphertext with the tag
appended) and a detached form (`_encrypt_detached`: ciphertext and tag in
separate buffers).

## When detached helps

- **Fixed layouts**: protocol puts the tag in a header field, or stores tags
  in a separate column/index.
- **In-place encryption**: ciphertext has the same length as plaintext, so you
  can encrypt a buffer in place. The libsodium docs state that `c` and `m` may overlap for `crypto_secretbox` and `crypto_box`; for the AEAD functions the docs do not say so (gated: unconfirmed, source is paywalled or blocked), although the ChaCha20-Poly1305 source XORs the keystream into the same pointer.
- **Zero-copy framing**: a network frame where the tag goes after a length
  field you write first.

```c
unsigned char mac[crypto_aead_xchacha20poly1305_ietf_ABYTES];
unsigned long long maclen;
crypto_aead_xchacha20poly1305_ietf_encrypt_detached(buf, mac, &maclen,
        buf, len, hdr, hdrlen, NULL, nonce, key);          /* in place */
if (crypto_aead_xchacha20poly1305_ietf_decrypt_detached(buf, NULL,
        buf, len, mac, hdr, hdrlen, nonce, key) != 0) {
    sodium_memzero(buf, len);                               /* do not use */
}
```

Note: in the ChaCha20-Poly1305 source (`aead_chacha20poly1305.c`), the tag is checked first and, when verification fails and `m` is not NULL, `m` is overwritten with zeros (`memset(m, 0, mlen)`) before returning -1. When decrypting in place that destroys the ciphertext, so keep a copy if you need it for logging (you usually do not). `aead_xchacha20poly1305.c` has the same `memset` on failure.

## Additional data design

AD is authenticated but not encrypted and not included in the output; the
receiver must reconstruct the same bytes.

- Put protocol headers there: version, message type, sequence number, sender
  id, key id. The header travels in clear, and any change makes decryption fail.
- Use an unambiguous encoding: fixed-width fields or length-prefixed. Joining
  strings with separators (`"user:" + id`) can collide.
- AD can be empty (`NULL, 0`), but if you have any context at all, bind it.
- Multi-part AD (several fields) must be serialised the same way on both sides;
  libsodium takes one buffer.

## Verify

- [ ] Detached tag stored/transmitted and checked; no path decrypts without the tag.
- [ ] Header tampering test: change one header byte, decryption fails.
- [ ] AD encoding documented (field order, widths, lengths).
