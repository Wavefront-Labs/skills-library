---
id: computing-software.cryptography-implementation.applied-cryptography.aes-ccm-for-constrained-devices
name: aes-ccm-for-constrained-devices
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, aead, aes-ccm, ccm-star, sp-800-38c, rfc-3610, iot, bluetooth-le, zigbee, openssl]
level: advanced
status: docs-checked
description: "Use AES-CCM correctly on constrained devices: nonce and length-field trade-off, tag sizes, CCM_8 risk, and the OpenSSL EVP call order CCM requires."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/c/upd1/final", "https://www.rfc-editor.org/rfc/rfc3610", "https://docs.openssl.org/3.0/man3/EVP_EncryptInit/#aead-interface", "https://www.rfc-editor.org/rfc/rfc8446"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AES-CCM for constrained devices

CCM (Counter with CBC-MAC) needs only the AES encrypt block, which is why
it suits small devices. It is a two-pass mode: the total message length must
be known before you start (OpenSSL requires it up front).

## Parameters

- **Nonce length n** is `15 - L` bytes, where L is the size of the length
  field. RFC 3610 allows L from 2 to 8, so the nonce is 7 to 13 bytes. The
  message must be shorter than 2^(8L) bytes: a 13-byte nonce (L = 2) limits
  messages to 2^16 - 1 bytes, a 7-byte nonce (L = 8) allows 2^64. Choose
  the longest nonce your message sizes allow.
- **Tag length M** is 4, 6, 8, 10, 12, 14 or 16 bytes (RFC 3610). Use 16.
  `CCM_8` (8-byte tag) is only for links that rate-limit forgery attempts;
  TLS 1.3 defines `TLS_AES_128_CCM_8_SHA256` (RFC 8446, with AEAD_AES_128_CCM_8
  from RFC 6655) but check the current IANA registry before enabling it.
- Nonces must never repeat under one key (RFC 3610: reuse destroys the
  security of the mode); on devices use a persisted message counter plus a
  sender id, not a weak RNG.

## OpenSSL EVP order (CCM is stricter than GCM)

```c
EVP_EncryptInit_ex(ctx, EVP_aes_128_ccm(), NULL, NULL, NULL);
EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_SET_IVLEN, 13, NULL);
EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_SET_TAG, 16, NULL); /* tag length */
EVP_EncryptInit_ex(ctx, NULL, NULL, key, nonce);
EVP_EncryptUpdate(ctx, NULL, &len, NULL, ptlen);           /* total length first */
EVP_EncryptUpdate(ctx, NULL, &len, aad, aadlen);
EVP_EncryptUpdate(ctx, ct, &len, pt, ptlen);
EVP_EncryptFinal_ex(ctx, ct + len, &len);
EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_GET_TAG, 16, tag);
```

OpenSSL documents these defaults for AES-CCM: tag length 12 and nonce length
7 (L = 8), so always set both. `EVP_CTRL_AEAD_SET_IVLEN` must be called before
the nonce is given.

On decrypt, `EVP_CTRL_AEAD_SET_TAG` with the expected tag must be set before
the ciphertext is passed in. Treat any failure from `EVP_DecryptUpdate` as an
authentication failure and discard the output.

## Verify

- [ ] RFC 3610 / SP 800-38C example vectors pass on the target.
- [ ] Nonce uniqueness survives reboot and factory reset (counter persisted).
- [ ] Tag length is 16 unless the protocol fixes it and rate-limits forgeries.

## Checked

2026-10-31. Confirmed: RFC 3610 (tag sizes 4-16 even, L 2 to 8, nonce 15-L
octets, message length below 2^(8L), nonce uniqueness); OpenSSL 3.0
EVP_EncryptInit page (CCM total-length call with NULL buffers, SET_TAG before
decrypting data, defaults of 12 for tag and 7 for nonce); RFC 8446
(TLS_AES_128_CCM_8_SHA256, AEAD_AES_128_CCM_8 defined in RFC 6655). Removed
as unconfirmed: the IANA "not recommended" statement, the TLS 1.2 CCM_8
cipher-suite name, the list of protocols using CCM, the claim of "no Final
check" and "ONE call only" on decrypt, and the mbedTLS, pyca and Java notes.
Method: documentation only; no commands were run.
