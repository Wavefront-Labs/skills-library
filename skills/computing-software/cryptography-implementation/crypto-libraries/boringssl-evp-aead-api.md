---
id: computing-software.cryptography-implementation.crypto-libraries.boringssl-evp-aead-api
name: boringssl-evp-aead-api
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, evp-aead-ctx, boringssl, aws-lc, aead, aes-gcm-siv, c]
level: advanced
status: docs-checked
description: "Use BoringSSL and AWS-LC EVP_AEAD: EVP_AEAD_CTX_init, seal and open with explicit nonce, max overhead, AES-GCM-SIV and ChaCha20 variants, and tag length choices."
sources: ["https://commondatastorage.googleapis.com/chromium-boringssl-docs/aead.h.html", "https://github.com/aws/aws-lc/blob/main/include/openssl/aead.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BoringSSL EVP_AEAD API

BoringSSL and AWS-LC provide `EVP_AEAD`, a simpler AEAD interface than `EVP_CIPHER`: one call to seal, one to
open, tag handled internally.

## Usage
```c
#include <openssl/aead.h>
EVP_AEAD_CTX ctx;
if (!EVP_AEAD_CTX_init(&ctx, EVP_aead_aes_256_gcm(), key, 32, EVP_AEAD_DEFAULT_TAG_LENGTH, NULL)) abort();

size_t out_len;
uint8_t out[PT_LEN + EVP_AEAD_MAX_OVERHEAD];
EVP_AEAD_CTX_seal(&ctx, out, &out_len, sizeof out,
                  nonce, EVP_AEAD_nonce_length(EVP_aead_aes_256_gcm()),
                  pt, pt_len, ad, ad_len);

if (!EVP_AEAD_CTX_open(&ctx, pt_out, &pt_len, sizeof pt_out,
                       nonce, EVP_AEAD_nonce_length(EVP_aead_aes_256_gcm()), out, out_len, ad, ad_len)) {
    /* authentication failure: discard */
}
EVP_AEAD_CTX_cleanup(&ctx);
```

## Algorithms
- `EVP_aead_aes_128_gcm`, `_256_gcm`, `EVP_aead_chacha20_poly1305`, `EVP_aead_xchacha20_poly1305`.
- `EVP_aead_aes_256_gcm_siv` (AES-256 in GCM-SIV mode, RFC 8452).
- `EVP_aead_xchacha20_poly1305`: ChaCha20-Poly1305 with an extended nonce that makes random nonces safe.
- `EVP_aead_aes_128_gcm_randnonce` / `EVP_aead_aes_256_gcm_randnonce`: the 12-byte nonce is generated internally and
  appended to the tag, so the "tag" is 12 bytes larger and the nonce argument must be zero-length. Because the
  nonce is random, do not use one key for more than 2^32 seal operations.
- Pass `EVP_AEAD_DEFAULT_TAG_LENGTH` (0) as `tag_len` for the default; truncated tags raise an attacker's chance
  of a forgery.
- Size output buffers as input length plus `EVP_AEAD_max_overhead(aead)` (`EVP_AEAD_MAX_OVERHEAD` is the maximum
  over all AEADs in the header).

## Notes
- The seal and open functions may be called concurrently on the same initialised `EVP_AEAD_CTX`.
- `EVP_AEAD_CTX_seal_scatter`/`open_gather` write the tag to a separate buffer.
- `EVP_AEAD_CTX_init` ignores `impl` (pass NULL), returns 1 on success and 0 on error, and a failed open returns 0.

## Verify
- [ ] Known-answer vectors for your chosen AEAD pass through your wrapper.

## Checked
2026-10-28. Confirmed against the BoringSSL `aead.h` documentation page (the AWS-LC `aead.h` header carries the
same family): `EVP_AEAD_CTX_init` semantics, default and truncated tag lengths, `EVP_AEAD_MAX_OVERHEAD`,
`EVP_AEAD_max_overhead`, nonce length rule, cleanup, concurrency statement, scatter/gather functions, GCM-SIV,
XChaCha20-Poly1305 and `randnonce` behaviour and 2^32 limit. Corrected: the randnonce AEADs append the nonce to
the tag and take a zero-length nonce; the example passed a literal 12 on open. Removed: nonce-misuse wording, TLS 1.3
AEAD note, OpenSSL availability claim and the test-vector path (not on these pages). The C code was not compiled or
run.
Method: documentation only; no commands were run.
