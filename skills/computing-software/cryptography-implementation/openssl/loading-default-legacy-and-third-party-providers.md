---
id: computing-software.cryptography-implementation.openssl.loading-default-legacy-and-third-party-providers
name: loading-default-legacy-and-third-party-providers
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-cnf, providers, provider-loading, legacy-provider, property-query, openssl-3]
level: advanced
status: docs-checked
description: "Load and select OpenSSL 3 providers: default, base, fips, legacy and third-party ones, activation rules, OPENSSL_MODULES, property queries and code-level loading."
sources: ["https://docs.openssl.org/master/man7/provider/", "https://docs.openssl.org/master/man3/OSSL_PROVIDER/", "https://docs.openssl.org/master/man7/property/", "https://docs.openssl.org/master/man7/OSSL_PROVIDER-legacy/", "https://github.com/openssl-projects/pkcs11-provider", "https://github.com/tpm2-software/tpm2-openssl", "https://github.com/open-quantum-safe/oqs-provider"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading default, legacy and third-party providers

In OpenSSL 3 algorithms live in **providers**. A fetch (`EVP_CIPHER_fetch`, `EVP_MD_fetch`, or the
implicit fetch inside `EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), ...)`) searches the loaded
providers that match the property query.

## Built-in providers
| Provider | Contents |
|---|---|
| `default` | all modern algorithms, encoders/decoders |
| `base` | encoders/decoders and store only (pair with `fips`) |
| `fips` | the FIPS-validated subset (separate `fips.so` + `fipsmodule.cnf`) |
| `legacy` | MD2, MD4, MDC2, RC2, RC4, RC5, Blowfish, CAST, DES (single), IDEA, SEED, Whirlpool, old PBKDFs |
| `null` | nothing; used to stop the default provider auto-loading |

## The activation rule that bites everyone
If no provider is explicitly loaded, `default` is available as a fallback. Explicitly loading a provider (config or
code) disables the fallback providers (`OSSL_PROVIDER_try_load` with `retain_fallbacks` nonzero keeps them). Loading only
`legacy` therefore leaves you without AES and SHA-256. Always load `default` alongside:
```
[provider_sect]
default = default_sect
legacy  = legacy_sect
[default_sect]
activate = 1
[legacy_sect]
activate = 1
```
CLI: `openssl pkcs12 -in old.p12 -provider legacy -provider default` (or `-legacy`).

## In code
```c
OSSL_PROVIDER *dflt = OSSL_PROVIDER_load(NULL, "default");
OSSL_PROVIDER *leg  = OSSL_PROVIDER_load(NULL, "legacy");
if (dflt == NULL || leg == NULL) { ERR_print_errors_fp(stderr); exit(1); }
EVP_MD *md4 = EVP_MD_fetch(NULL, "MD4", "provider=legacy");
/* ... */
EVP_MD_free(md4); OSSL_PROVIDER_unload(leg); OSSL_PROVIDER_unload(dflt);
```
- `OSSL_PROVIDER_try_load(ctx, name, 1)` loads while keeping the fallback providers; with `retain_fallbacks` zero a
  successful load disables them, and a failed load leaves them in place.
- Scope legacy algorithms to their own `OSSL_LIB_CTX` (`OSSL_LIB_CTX_new` + load there) so the rest
  of the process can't fetch RC4 or MD4 by accident.

## Third-party providers
- `pkcs11-provider` (HSM/smart card keys via `pkcs11:` URIs), `tpm2-openssl` (TPM keys),
  `oqs-provider` (post-quantum algorithms). Recent OpenSSL releases include ML-KEM and ML-DSA in the default provider
  (see OSSL_PROVIDER-default(7) for your release).
- Module search path: the build-time `MODULESDIR` (`openssl version -m`), overridden by the `OPENSSL_MODULES` environment
  variable or the `-provider-path` option; in config, `module = /path/to/pkcs11.so` inside the provider's section.
- Pass provider-specific settings as keys in its section (e.g. `pkcs11-module-path = ...`).

## Property queries
```
openssl list -cipher-algorithms -propquery provider=default
EVP_CIPHER_fetch(NULL, "AES-256-GCM", "fips=yes")
[algorithm_sect] default_properties = ?provider=pkcs11    # prefer, '?' = optional
```
Use `provider=` to pin and `?` to express preference without breaking when absent.

## Verify
- [ ] `openssl list -providers -verbose` shows exactly the intended providers as `status: active`.
- [ ] Legacy is not active in processes that don't need it.
- [ ] A missing third-party module fails startup loudly rather than silently using software keys.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in OSSL_PROVIDER(3) (fallback providers, `try_load` and `retain_fallbacks`, `OPENSSL_MODULES`), OSSL_PROVIDER-legacy(7) (MD2, MD4, MDC2, WHIRLPOOL, RIPEMD160, Blowfish, CAST, DES, IDEA, RC2, RC4, RC5, SEED, PBKDF1, PVKKDF), OSSL_PROVIDER-base(7), OSSL_PROVIDER-null(7) (supplies no algorithms), property(7) (`?` optional prefix, `fips=yes`, `provider=` clauses) and openssl-version(1) `-m`. Third-party provider repositories exist and are maintained. Removed the unconfirmed 3.5 version claim and the older wording about automatic loading on first use.

Method: documentation only; no commands were run.
