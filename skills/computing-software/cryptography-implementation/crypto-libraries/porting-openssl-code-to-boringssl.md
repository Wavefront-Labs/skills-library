---
id: computing-software.cryptography-implementation.crypto-libraries.porting-openssl-code-to-boringssl
name: porting-openssl-code-to-boringssl
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, boringssl, boringssl-porting, openssl-compat, evp-aead, aws-lc, c-api, api-stability]
level: advanced
status: docs-checked
description: "Port C/C++ code from OpenSSL to BoringSSL: what PORTING.md says changes, EVP_AEAD instead of EVP_CIPHER for AEADs, ctrl functions, renegotiation, and no API stability."
sources: ["https://boringssl.googlesource.com/boringssl/+/HEAD/PORTING.md", "https://commondatastorage.googleapis.com/chromium-boringssl-docs/headers.html", "https://boringssl.googlesource.com/boringssl/+/HEAD/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Porting OpenSSL code to BoringSSL

BoringSSL is an OpenSSL derivative and is mostly source-compatible for the subset of OpenSSL it retains. PORTING.md
says to see whether the library compiles and, on failure, to read the header documentation and see if the problem
feature can be removed. BoringSSL has **no stable API or ABI**: it must be updated with its consumers, and it is not
suitable as a traditional distribution system library. Chromium statically links the revision it was built against;
Android's internal copy is not exposed by the NDK and must not be used by third-party apps.

## Detecting BoringSSL

- `OPENSSL_VERSION_NUMBER` matches the OpenSSL version BoringSSL targets (it targets OpenSSL 1.1.0 now), and the
  upstream `OPENSSL_NO_*` macros are defined for removed features. Prefer these checks, especially when patching
  third-party code, because such patches also help upstream.
- When BoringSSL-specific code is needed, use `#ifdef OPENSSL_IS_BORINGSSL` (also usable in configure scripts). Do
  not detect BoringSSL by the presence of symbols. Contact the maintainers about missing APIs first.

## Major API changes (from PORTING.md)

- **Integer types**: some APIs use `size_t`; `STACK_OF(T)` indices and lengths are `size_t`.
- **Reference counts**: `CRYPTO_add` with `CRYPTO_LOCK_*` no longer exists; call `FOO_up_ref` (for example
  `EVP_PKEY_up_ref`). Some structs are opaque, so use accessors.
- **Error codes**: error reasons differ and function codes are removed. Grep for `ERR_GET_REASON` and `ERR_GET_FUNC`
  and avoid conditioning on exact reasons.
- **`*_ctrl` functions are removed**: macros such as `SSL_CTX_set_mode` are real functions. Switch callers to the
  function versions, which are type-checked; the document has a CTRL-to-function table.
- **`EVP_PKEY_HMAC` is removed** (use `HMAC_*`); `EVP_PKEY_DSA` is deprecated and signing or verifying with such
  keys does not work.
- **Renegotiation**: peer renegotiation is rejected by default; enable it with `SSL_set_renegotiate_mode`
  (`ssl_renegotiate_once` or `ssl_renegotiate_freely`). It works only as a client in TLS; there is no server-side
  or DTLS renegotiation and `SSL_renegotiate` always fails.
- **`BN_bn2hex`** emits lowercase hex.
- **d2i functions** always allocate a new object and free the previous `*out`; pass NULL for `out`.
- **`OPENSSL_free`** zeroes memory with extra bookkeeping, so memory must be released with the matching function,
  not plain `free`.
- Return values are narrowed to 1 on success and 0 on failure; check every return. Initialisation functions still
  exist but do nothing, and threading callbacks do nothing because the library is thread-safe where the API
  guarantees it.
- Hardware or opaque keys: the ENGINE API is mostly removed; for TLS prefer `SSL_PRIVATE_KEY_METHOD` via
  `SSL[_CTX]_set_private_key_method`, which lets a handshake be suspended during the private operation.

## Use EVP_AEAD for authenticated encryption

```c
EVP_AEAD_CTX ctx;
EVP_AEAD_CTX_init(&ctx, EVP_aead_aes_256_gcm(), key, 32, EVP_AEAD_DEFAULT_TAG_LENGTH, NULL);
size_t out_len;
EVP_AEAD_CTX_seal(&ctx, out, &out_len, sizeof out, nonce, EVP_AEAD_nonce_length(EVP_aead_aes_256_gcm()),
                  pt, pt_len, ad, ad_len);
if (!EVP_AEAD_CTX_open(&ctx, pt, &pt_len, sizeof pt, nonce, EVP_AEAD_nonce_length(EVP_aead_aes_256_gcm()),
                       out, out_len, ad, ad_len)) { /* reject */ }
EVP_AEAD_CTX_cleanup(&ctx);
```

One call seals, with the tag appended. Other AEADs in the header: `EVP_aead_xchacha20_poly1305`,
`EVP_aead_aes_256_gcm_siv`, and the `_randnonce` forms (nonce generated and appended; the nonce argument must be
zero-length; see the EVP_AEAD skill).

## Vendoring

- Pin a commit and update deliberately, with the consumers, because the API is not stable.
- Need a library derived from BoringSSL with FIPS 140-3 validated modules? See the AWS-LC FIPS skill.

## Verify

- [ ] Code compiles without OpenSSL compatibility shims for removed features.
- [ ] AEAD code uses `EVP_AEAD` and checks `open` return values.
- [ ] Vendored commit recorded; update process documented.

## Checked

2026-10-28. Confirmed against BoringSSL PORTING.md and the BoringSSL `aead.h` documentation: compatibility and
stability statements, version and `OPENSSL_IS_BORINGSSL` guidance, integer types, up_ref, error codes, ctrl removal,
HMAC/DSA EVP_PKEY, renegotiation rules, lowercase hex, d2i, `OPENSSL_free`, narrowed return values, no-op
initialisation and threading, `SSL_PRIVATE_KEY_METHOD`, EVP_AEAD functions. Removed (not in PORTING.md or not
verified): removed-ciphers and SSLv3 list, `RAND_add` remark, TLS 1.3 suite configuration and `[A|B]` cipher strings,
`SSL_ERROR_WANT_*` names, build commands, Go and Perl prerequisites, `BORINGSSL_PREFIX`, the AWS-LC stable API
claim. The C code was not compiled or run.
Method: documentation only; no commands were run.
