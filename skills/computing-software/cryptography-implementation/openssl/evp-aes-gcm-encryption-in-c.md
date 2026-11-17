---
id: computing-software.cryptography-implementation.openssl.evp-aes-gcm-encryption-in-c
name: evp-aes-gcm-encryption-in-c
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, evp-cipher-gcm, openssl-evp, aes-gcm, aead, c]
level: advanced
status: docs-checked
description: "Encrypt and decrypt with AES-GCM through OpenSSL EVP_CIPHER in C: IV length control, AAD calls, getting and setting the tag, and checking EVP_DecryptFinal_ex."
sources: ["https://docs.openssl.org/3.0/man3/EVP_EncryptInit/", "https://wiki.openssl.org/index.php/EVP_Authenticated_Encryption_and_Decryption"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EVP AES-GCM encryption in C

## Encrypt
```c
EVP_CIPHER_CTX *c = EVP_CIPHER_CTX_new();
EVP_EncryptInit_ex2(c, EVP_aes_256_gcm(), NULL, NULL, NULL);
EVP_CIPHER_CTX_ctrl(c, EVP_CTRL_GCM_SET_IVLEN, 12, NULL);   /* 12 is default; set explicitly */
EVP_EncryptInit_ex2(c, NULL, key, iv, NULL);
EVP_EncryptUpdate(c, NULL, &n, aad, aad_len);              /* AAD: out == NULL */
EVP_EncryptUpdate(c, ct, &n, pt, pt_len);  ct_len = n;
EVP_EncryptFinal_ex(c, ct + ct_len, &n);   ct_len += n;
EVP_CIPHER_CTX_ctrl(c, EVP_CTRL_GCM_GET_TAG, 16, tag);
EVP_CIPHER_CTX_free(c);
```

## Decrypt
```c
EVP_DecryptInit_ex2(c, EVP_aes_256_gcm(), key, iv, NULL);
EVP_DecryptUpdate(c, NULL, &n, aad, aad_len);
EVP_DecryptUpdate(c, pt, &n, ct, ct_len);
EVP_CIPHER_CTX_ctrl(c, EVP_CTRL_GCM_SET_TAG, 16, tag);     /* before Final */
if (EVP_DecryptFinal_ex(c, pt + n, &m) <= 0) { OPENSSL_cleanse(pt, ct_len); /* reject */ }
```

## Rules
- Plaintext from `DecryptUpdate` is unauthenticated until `DecryptFinal_ex` returns 1; do not release it before.
- Always check return values of every call; 3.0 can fail at init (for example when the algorithm cannot be fetched from a provider).
- Never reuse an IV with the same key. The default AES-GCM IV length is 12 bytes (96 bits); for IV construction and
  message-count limits follow NIST SP 800-38D.
- Tag length 16; reject truncated tags supplied by the peer (check `tag_len == 16` yourself).
- OpenSSL 3: `EVP_CIPHER_fetch(libctx, "AES-256-GCM", props)` for provider-aware code; params
  `OSSL_CIPHER_PARAM_AEAD_TAG` replace ctrls.

## Verify
- [ ] NIST GCM test vectors pass; modified tag/AAD/ciphertext all fail at Final.

## Checked

2026-10-31. Confirmed against the OpenSSL 3.0 EVP_EncryptInit page (return values of the Init/Update/Final calls, AAD via `out == NULL`, default GCM IV length 12, `EVP_CTRL_AEAD_GET_TAG`/`SET_TAG` mapping to the `tag` parameter `OSSL_CIPHER_PARAM_AEAD_TAG`, failed `EVP_DecryptFinal_ex` means the output MUST NOT be used), the OpenSSL wiki "EVP Authenticated Encryption and Decryption" (`EVP_CTRL_GCM_SET_IVLEN`, `EVP_CTRL_GCM_GET_TAG`, `EVP_CTRL_GCM_SET_TAG` with tag size 16, tag set before Final) and EVP_CIPHER-AES (`AES-256-GCM` name).
Removed: the "n == 0 for GCM" remark and the 2^32-messages IV rule (SP 800-38D was not fetched).
Method: documentation only; no commands were run.
