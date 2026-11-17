---
id: computing-software.cryptography-implementation.openssl.migrating-openssl-111-to-3
name: migrating-openssl-111-to-3
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, libssl, openssl-3-migration, deprecated-api, low-level-api, engines, providers, legacy-provider, openssl-api-compat]
level: advanced
status: docs-checked
description: "Port C code from OpenSSL 1.1.1 to 3.x: deprecated low-level calls to EVP, engines to providers, legacy algorithms, and behaviour changes that break apps."
sources: ["https://docs.openssl.org/3.0/man7/migration_guide/", "https://docs.openssl.org/3.0/man7/openssl_user_macros/", "https://docs.openssl.org/3.0/man7/provider/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating from OpenSSL 1.1.1 to 3.x

The migration guide
(`man 7 migration_guide`) is long; these are the changes that actually stop
builds and break behaviour.

## 1. Build first with deprecation warnings visible

```bash
cc -Werror=deprecated-declarations ...          # find every deprecated call
# temporary escape hatch while porting:
cc -DOPENSSL_API_COMPAT=0x10101000L ...
```

`OPENSSL_API_COMPAT` only selects which deprecated symbols stay visible (see
`openssl_user_macros`); it does not port the code to EVP and providers.

## 2. Replace low-level APIs with EVP

| Deprecated (1.1.1 style) | Replacement |
|---|---|
| `RSA_generate_key_ex`, `RSA_*` | `EVP_PKEY_Q_keygen` or `EVP_RSA_gen`, then `EVP_PKEY_*` ops |
| `EC_KEY_*`, `ECDSA_sign` | `EVP_PKEY` + `EVP_DigestSign*` |
| `AES_encrypt`, `AES_cbc_encrypt` | `EVP_CIPHER_fetch` + `EVP_EncryptInit_ex2` |
| `HMAC_Init_ex`, `HMAC_CTX` | `EVP_MAC_fetch` ("HMAC") with an `OSSL_PARAM` digest, or the one-shot `EVP_Q_mac` |
| `SHA256_Init/Update/Final` | `EVP_DigestInit_ex` / `EVP_Q_digest` |
| `DH_*`, `DH_compute_key` | the `EVP_PKEY` key-exchange API (guide: "Deprecated low-level key exchange functions") |
| `ENGINE_*` | providers (`OSSL_PROVIDER_load`), pkcs11-provider for HSMs |

Functions such as `EVP_PKEY_get1_RSA` that return an internal key must be treated as
read only (guide: "Functions that return an internal key should be treated as read only").

## 3. Algorithms moved to the legacy provider

MD2, MD4, MDC2, RC2, RC4, RC5, DES and DESX, Blowfish, CAST, IDEA, SEED and
Whirlpool moved to the legacy provider, so fetching them fails unless it is loaded.
Load it explicitly only where truly needed (`openssl pkcs12 -legacy` restores the
old PKCS#12 defaults for interoperability):

```c
OSSL_PROVIDER_load(NULL, "legacy"); OSSL_PROVIDER_load(NULL, "default");
```

## 4. Behaviour changes that bite

- Unexpected EOF without close_notify is now an error (`SSL_R_UNEXPECTED_EOF_WHILE_READING`);
  set `SSL_OP_IGNORE_UNEXPECTED_EOF` only if your protocol frames lengths itself.
- The default TLS security level is 1 (80 bits): RSA/DH keys under 1024 bits and
  SHA-1 or MD5 signatures are rejected, so `SSL_CTX_use_certificate` fails for a
  SHA-1 signed leaf. Level 2 (112 bits) also rejects keys under 2048 bits. Check
  the level your build configures; old test certificates fail after the upgrade.
- `SSL_CTX_set_cipher_list` only covers TLS 1.2 and below; use `SSL_CTX_set_ciphersuites` for TLS 1.3.
- Match error reasons with `ERR_GET_REASON` codes (for example `SSL_R_UNEXPECTED_EOF_WHILE_READING`), not strings.
- Fetching algorithms (`EVP_CIPHER_fetch`) per operation is slow; fetch once
  and reuse.

## Verify

- [ ] Build passes with `-Werror=deprecated-declarations` and no `OPENSSL_API_COMPAT`.
- [ ] Test suite passes with only default (and FIPS, if relevant) providers loaded.
- [ ] Integration tests cover EOF handling and legacy file formats.

## Checked

2026-10-31. Confirmed against the OpenSSL 3.0 pages migration_guide (legacy-provider algorithm list, `SSL_OP_IGNORE_UNEXPECTED_EOF`, default security level 1 and SHA-1 rejection, `EVP_PKEY_Q_keygen`/`EVP_RSA_gen`/`EVP_Q_digest`/`EVP_Q_mac`, prefetch advice, `pkcs12 -legacy`), openssl_user_macros (`OPENSSL_API_COMPAT` format), SSL_CTX_set_cipher_list (TLS 1.3 uses `SSL_CTX_set_ciphersuites`), SSL_CTX_set_security_level (level 1 = 80 bits, level 2 = 112 bits), SSL_get_error.
Removed: the end-of-life date, the FIPS-bypass remark, the `RSA_get0_key` row, the cached-copy claim for `EVP_PKEY_get1_RSA`, the `unsupported` error string, and the distro security-level and SHA-1 remarks (the guide says SHA-1 certificates are refused from level 1). Corrected: MD5 is not in the legacy list.
Method: documentation only; no commands were run.
