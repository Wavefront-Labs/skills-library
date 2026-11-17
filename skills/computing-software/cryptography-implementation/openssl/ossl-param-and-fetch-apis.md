---
id: computing-software.cryptography-implementation.openssl.ossl-param-and-fetch-apis
name: ossl-param-and-fetch-apis
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, libssl, ossl-param, evp-fetch, evp-pkey-fromdata, ossl-lib-ctx, property-query, openssl-3, c-api]
level: sme
status: docs-checked
description: "Use OpenSSL 3 OSSL_PARAM arrays and explicit fetching: building and reading params, EVP_PKEY_fromdata/todata, library contexts and property queries like fips=yes."
sources: ["https://docs.openssl.org/3.0/man3/OSSL_PARAM/", "https://docs.openssl.org/3.0/man7/crypto/", "https://docs.openssl.org/3.0/man3/EVP_PKEY_fromdata/", "https://docs.openssl.org/3.0/man3/OSSL_PARAM_BLD/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSSL_PARAM and fetch APIs

OpenSSL 3 replaced per-algorithm structs and ctrl calls with two ideas:
**fetching** an implementation from a provider, and passing settings as
**OSSL_PARAM** arrays (name, type, pointer).

## Fetching

```c
OSSL_LIB_CTX *libctx = NULL;                   /* NULL = default context */
EVP_MD *sha = EVP_MD_fetch(libctx, "SHA2-256", "fips=yes");
EVP_CIPHER *gcm = EVP_CIPHER_fetch(libctx, "AES-256-GCM", NULL);
EVP_MAC *hmac = EVP_MAC_fetch(libctx, "HMAC", NULL);
/* ... use ..., then */
EVP_MD_free(sha); EVP_CIPHER_free(gcm); EVP_MAC_free(hmac);
```

- Explicit fetch is faster than implicit (`EVP_sha256()`) when reused, and lets
  you require properties (`"fips=yes"`, `"provider=default"`).
- Prefetch once at startup and reuse: crypto(7) says an implicit fetch is slower than passing a prefetched object, even with the internal cache.
- Separate `OSSL_LIB_CTX` instances isolate configurations (e.g. a FIPS-only
  context inside a process that also needs legacy algorithms):
  `OSSL_LIB_CTX_load_config(ctx, "fips.cnf")`.

## Passing parameters

```c
OSSL_PARAM params[] = {
    OSSL_PARAM_construct_utf8_string(OSSL_MAC_PARAM_DIGEST, "SHA256", 0),
    OSSL_PARAM_END
};
EVP_MAC_CTX *mctx = EVP_MAC_CTX_new(hmac);
EVP_MAC_init(mctx, key, keylen, params);
```

For dynamic arrays use the builder:

```c
OSSL_PARAM_BLD *b = OSSL_PARAM_BLD_new();
OSSL_PARAM_BLD_push_utf8_string(b, OSSL_PKEY_PARAM_GROUP_NAME, "P-256", 0);
OSSL_PARAM_BLD_push_octet_string(b, OSSL_PKEY_PARAM_PUB_KEY, pub, publen);
OSSL_PARAM *p = OSSL_PARAM_BLD_to_param(b);
EVP_PKEY_CTX *kc = EVP_PKEY_CTX_new_from_name(NULL, "EC", NULL);
EVP_PKEY *pkey = NULL;
EVP_PKEY_fromdata_init(kc);
EVP_PKEY_fromdata(kc, &pkey, EVP_PKEY_PUBLIC_KEY, p);   /* import raw public key */
OSSL_PARAM_free(p); OSSL_PARAM_BLD_free(b);
```

Reading values back: `EVP_PKEY_get_utf8_string_param`,
`EVP_PKEY_get_octet_string_param`, `EVP_PKEY_get_bn_param`, or
`EVP_PKEY_todata` for all.

## Gotchas

- Names are strings; a typo is not a compile error. Use the `OSSL_*_PARAM_*`
  macros, and check return values (the OSSL_PARAM page says keys a setter does not
  recognise are simply ignored, and `EVP_PKEY_fromdata` ignores params that are not
  settable; query the `*_settable_params` functions when in doubt).
- Integer params are coerced between C integer types where the value fits (OSSL_PARAM_int(3) NOTES); use the
  `OSSL_PARAM_construct_*` call for the parameter's documented type.
- Octet-string params point at your buffer; keep it alive until the call returns.
- Validate an imported untrusted public key with `EVP_PKEY_public_check`.

## Verify

- [ ] Fetched objects freed; no fetch in hot loops (profile).
- [ ] Parameter names come from macros; return codes checked.
- [ ] FIPS builds use `fips=yes` property or a FIPS-configured libctx and tests prove non-FIPS algorithms fail.

## Checked

2026-10-31. Confirmed against the OpenSSL 3.0 pages crypto(7) (explicit fetch, prefetch, property queries such as `provider=default`, `SHA2-256` fetch), OSSL_LIB_CTX (`OSSL_LIB_CTX_load_config`), OSSL_PARAM (unknown keys ignored), OSSL_PARAM_int (type coercion), OSSL_PARAM_BLD (`OSSL_PARAM_BLD_push_octet_string`), EVP_PKEY_fromdata, EVP_PKEY_gettable_params (`EVP_PKEY_get_bn_param`, `get_utf8_string_param`, `get_octet_string_param`, `OSSL_PKEY_PARAM_GROUP_NAME`, `OSSL_PKEY_PARAM_PUB_KEY`), EVP_PKEY-EC (`P-256` group), EVP_MAC-HMAC (`OSSL_MAC_PARAM_DIGEST`), EVP_CIPHER-AES (`AES-256-GCM`) and EVP_PKEY_check (`EVP_PKEY_public_check`).
Corrected: integer parameter types are coerced, not exact. Removed: "each fetch walks provider tables" and "`EVP_PKEY_fromdata` does not fully validate" (not stated in the pages).
Method: documentation only; no commands were run.
