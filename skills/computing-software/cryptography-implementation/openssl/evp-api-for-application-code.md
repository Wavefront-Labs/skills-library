---
id: computing-software.cryptography-implementation.openssl.evp-api-for-application-code
name: evp-api-for-application-code
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, evp, libcrypto, openssl-3, providers, evp-encryptinit, evp-cipherctx, error-checking, deprecated-api, legacy-provider, fips-provider, c-api]
level: sme
status: docs-checked
description: "Call OpenSSL's EVP API correctly from C: the init/update/final lifecycle, checking every return value, OpenSSL 3 provider selection, and deprecated low-level APIs to avoid."
sources: ["https://docs.openssl.org/3.0/man3/EVP_EncryptInit/", "https://docs.openssl.org/3.0/man7/provider/", "https://docs.openssl.org/3.0/man7/migration_guide/", "https://wiki.openssl.org/index.php/EVP"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSSL's EVP API for application code

The existing `certificates-csrs-and-tls-testing` skill covers the OpenSSL
CLI; this is the C API surface for applications that link `libcrypto`
directly rather than shelling out. A missed error check here can silently
produce unauthenticated or wrong ciphertext instead of a shell command that
visibly fails.

## Always use EVP, never the algorithm-specific low-level API

OpenSSL exposes a high-level **EVP** interface (`EVP_EncryptInit_ex2`,
`EVP_CIPHER_CTX`, etc.; algorithm-agnostic) and older **algorithm-specific
low-level functions** (direct `AES_encrypt`, raw `SHA256_*` calls). The
low-level functions are deprecated as of OpenSSL 3.0, and the migration guide
tells applications to use the high-level EVP APIs instead. Use EVP for new
code; code that calls the low-level API directly is a flag to migrate it, not
a pattern to extend.

## The EVP lifecycle, and why every return value matters

```c
EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
if (!EVP_EncryptInit_ex2(ctx, EVP_aes_256_gcm(), key, iv, NULL)) { /* handle */ }
if (!EVP_EncryptUpdate(ctx, out, &outlen, in, inlen))            { /* handle */ }
if (!EVP_EncryptFinal_ex(ctx, out + outlen, &finallen))          { /* handle */ }
if (!EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_GET_TAG, 16, tag))   { /* handle */ }
EVP_CIPHER_CTX_free(ctx);
```

`EVP_EncryptInit_ex2`, `EVP_EncryptUpdate` and `EVP_EncryptFinal_ex` return 1
for success and 0 for failure; `EVP_DecryptFinal_ex` returns 0 if the decrypt
failed and 1 for success. OpenSSL's C API does not throw or abort: a skipped
check just carries on with whatever is in the buffers. Treat every EVP call as
fallible and check every one.

For AEAD modes: get the tag with `EVP_CIPHER_CTX_ctrl(..., EVP_CTRL_AEAD_GET_TAG, ...)`
on encrypt and set it with `EVP_CTRL_AEAD_SET_TAG` *before*
`EVP_DecryptFinal_ex` on decrypt. For a fetched cipher these ctrls map to the
`tag` parameter (`OSSL_CIPHER_PARAM_AEAD_TAG`). The EVP_EncryptInit page says
the return value of `EVP_DecryptFinal_ex` indicates whether authentication
succeeded, and that if it does not indicate success the output data MUST NOT be
used because it is corrupted. That return value is the authentication check.

## OpenSSL 3's provider architecture changes how algorithms resolve

OpenSSL 3.0 introduced **providers**: pluggable implementations of
algorithms. OpenSSL ships the `default`, `base`, `fips`, `legacy` and `null`
providers (provider(7)). Practical implications for application code:
- Convenience calls such as `EVP_aes_256_gcm()` only supply a name; the
  implementation is fetched from a provider at use, which is slower than
  prefetching with `EVP_CIPHER_fetch` (migration guide, crypto(7)). If you
  need FIPS-validated code paths, load the `fips` provider explicitly and
  select it with a property query such as `fips=yes`; do not assume a named
  cipher function gets you there. See
  `computing-software.cryptography-implementation.crypto-libraries.dependency-and-cve-hygiene`
  for the broader FIPS-build caveat.
- Some legacy algorithms (MD2, MD4, RC4, DES, Blowfish and others listed in
  the migration guide) moved to the `legacy` provider and are unavailable
  unless you load it explicitly. Prefer migrating off the legacy algorithm
  to loading the legacy provider.

## Verify

- [ ] Every `EVP_*` call's return value is checked; no silent-continue
      paths on a skipped check.
- [ ] AEAD tag set/get calls happen in the correct order relative to
      `Init`/`Update`/`Final`, and `EVP_DecryptFinal_ex`'s return value is
      the authentication gate, checked and enforced.
- [ ] No direct calls to deprecated low-level algorithm-specific functions
      in new code.
- [ ] If FIPS validation is required, the FIPS provider is explicitly
      loaded and selected.
- [ ] Any reliance on a legacy-provider algorithm is a deliberate, reviewed
      decision.

## Checked

2026-10-31. Confirmed against the OpenSSL 3.0 man pages EVP_EncryptInit (return values of Init/Update/Final, `EVP_CTRL_AEAD_GET_TAG`/`SET_TAG` mapping to the `tag` parameter, Final return as the authentication result), provider(7) (default, base, fips, legacy, null) and the migration guide (low-level deprecation, legacy-provider algorithm list, performance cost of implicit fetch).
Removed: the claim that MD5 moved to the legacy provider (the guide lists MD2, MD4 and MDC2, not MD5), the claim that low-level calls bypass FIPS or hardware acceleration, "on older code paths skips authentication", the `NULL` from `EVP_get_cipherbyname` claim, and the "single most common bug" assertion, none of which the pages support.
Method: documentation only; no commands were run.
