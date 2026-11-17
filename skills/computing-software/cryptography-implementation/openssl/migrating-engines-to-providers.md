---
id: computing-software.cryptography-implementation.openssl.migrating-engines-to-providers
name: migrating-engines-to-providers
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, openssl-engine, providers, pkcs11-provider, tpm2-openssl, openssl-3-migration, ossl-store, hsm]
level: advanced
status: docs-checked
description: "Replace deprecated OpenSSL ENGINE usage with OpenSSL 3 providers: the -provider option, OSSL_STORE URIs for engine-backed keys, and API replacements."
sources: ["https://docs.openssl.org/3.0/man7/migration_guide/", "https://docs.openssl.org/3.0/man7/provider/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating ENGINEs to providers

All ENGINE functions are deprecated since OpenSSL 3.0; the migration guide says an engine should be rewritten as a provider and applications using engines should use providers.

## Replacements
Check each engine's vendor or project for a provider equivalent; the OpenSSL migration guide only states that providers replace engines.

## Command lines
The `openssl` command takes `-provider name` (and `-provider-path path`) to load a provider. The `-keyform` option accepts `DER`, `PEM` or `P12` on `openssl req`, so engine-backed keys are loaded through `OSSL_STORE` URIs instead.
Engine-backed keys can be loaded via a custom `OSSL_STORE` implementation; `EVP_PKEY` objects created with `ENGINE_load_private_key(3)` are considered legacy and keep working.

## Code
- `ENGINE_load_private_key()` becomes `OSSL_STORE_open(uri, ...)` + `OSSL_STORE_load()`.
- `EVP_PKEY_set1_engine()` and every other `ENGINE_*()` function are deprecated; use providers.

## Gotchas
- Read the provider's own documentation for which other providers (such as `default`) must stay loaded alongside it.

## Verify
- [ ] `openssl list -providers` shows the providers you expect.
- [ ] No `-engine` flags remain anywhere.

## Checked
2026-11-01. Confirmed in the OpenSSL migration guide (ossl-guide-migration) and man pages: ENGINE API deprecated and providers are the replacement, engine-backed keys via OSSL_STORE, `EVP_PKEY_set1_engine()` deprecated, `OSSL_STORE_open`/`OSSL_STORE_load`, `openssl -provider` and `-provider-path`, `-keyform DER|PEM|P12`. Removed: the third-party provider table, the config examples (pkcs11-provider keys not checked), FIPS/new-algorithm claim, property-query advice.
Method: documentation only; no commands were run.
